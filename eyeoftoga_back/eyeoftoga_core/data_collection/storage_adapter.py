"""
Session Behavior SDK - Monitoramento REAL de Comportamento
Captura interações reais do usuário em tempo real em toda a tela
"""

from dataclasses import dataclass, field
import pygame
import time
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any
from enum import Enum
from collections import defaultdict
import logging
import pyautogui
from screeninfo import get_monitors
from pynput import mouse, keyboard
from device_info import DeviceEnvironmentSDK
from ip_location import session_id, IPLocationSDK, AuthenticationData, AuthMethod, AuthResult
import os
import cv2
import numpy as np
from deepface import DeepFace

from risk_score import RiskScorer

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Enumeração dos tipos de eventos que podem ser capturados"""
    MOUSE_CLICK = "mouse_click"
    MOUSE_MOVE = "mouse_move"
    KEY_PRESS = "key_press"
    WINDOW_FOCUS = "window_focus"
    SCROLL = "scroll"
    DRAG = "drag"


@dataclass
class RealTimeEvent:
    """Classe para representar um evento em tempo real"""
    event_id: str
    event_type: EventType
    timestamp: datetime
    position: Optional[Dict[str, int]] = None
    key: Optional[str] = None
    button: Optional[str] = None
    scroll_direction: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RealTimeMonitor:
    """Classe principal para monitoramento de eventos em tempo real"""
    
    def __init__(self):
        # Inicialização das variáveis de estado
        self.events: List[RealTimeEvent] = []
        self.is_monitoring = False
        self.monitor_thread = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_position = None
        self.click_count = 0
        self.keypress_count = 0
        self.start_time = None
        
        # Detecção das dimensões da tela
        try:
            self.screen_width, self.screen_height = pyautogui.size()
        except Exception:
            # Fallback para resolução padrão em caso de erro
            self.screen_width, self.screen_height = 1920, 1080

        # Detecção de múltiplos monitores
        self.monitors = []
        try:
            for m in get_monitors():
                self.monitors.append({
                    "x": m.x,
                    "y": m.y,
                    "width": m.width,
                    "height": m.height,
                    "name": str(m.name)
                })
        except Exception:
            # Fallback para monitor único em caso de erro
            self.monitors = [{"width": self.screen_width, "height": self.screen_height, "name": "unknown"}]

        logger.info(f"Tela detectada: {self.screen_width}x{self.screen_height}")
        logger.info(f"Monitores detectados: {len(self.monitors)}")

        # Inicialização segura do pygame para visualização
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((300, 200))
            pygame.display.set_caption("EyeOfToga Monitor")
        except Exception:
            self.screen = None

    def start_monitoring(self):
        """Inicia o monitoramento de eventos de mouse e teclado"""
        if self.is_monitoring:
            logger.warning("Monitoramento já está ativo")
            return
            
        self.is_monitoring = True
        self.start_time = datetime.now()
        
        # Configura os listeners para mouse e teclado
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press
        )
        
        # Inicia os listeners em threads separadas
        self.mouse_listener.start()
        self.keyboard_listener.start()
        logger.info("Monitoramento iniciado - Capturando suas interações em toda a tela...")

    def stop_monitoring(self):
        """Para o monitoramento de eventos"""
        self.is_monitoring = False
        if self.mouse_listener:
            try:
                self.mouse_listener.stop()
            except Exception:
                pass
        if self.keyboard_listener:
            try:
                self.keyboard_listener.stop()
            except Exception:
                pass
        logger.info("Monitoramento parado")

    def _on_mouse_move(self, x, y):
        """Callback para movimento do mouse"""
        if not self.is_monitoring:
            return
            
        current_pos = {"x": x, "y": y}
        # Registra apenas movimentos significativos (mais de 2 pixels)
        if self.last_position and (abs(current_pos["x"] - self.last_position["x"]) > 2 or abs(current_pos["y"] - self.last_position["y"]) > 2):
            self._record_mouse_move(current_pos)
        self.last_position = current_pos

    def _on_mouse_click(self, x, y, button, pressed):
        """Callback para clique do mouse"""
        if not self.is_monitoring or not pressed:
            return
            
        timestamp = datetime.now()
        button_name = str(button).split(".")[-1].lower()
        event_obj = RealTimeEvent(
            event_id=f"event_{len(self.events)}",
            event_type=EventType.MOUSE_CLICK,
            timestamp=timestamp,
            position={"x": x, "y": y},
            button=button_name,
            metadata={"screen_size": {"width": self.screen_width, "height": self.screen_height}, "monitors": self.monitors}
        )
        self.events.append(event_obj)
        self.click_count += 1
        logger.info(f"Clique capturado: {button_name} em ({x}, {y}) - Total: {self.click_count}")

    def _on_mouse_scroll(self, x, y, dx, dy):
        """Callback para scroll do mouse"""
        if not self.is_monitoring:
            return
            
        timestamp = datetime.now()
        event_obj = RealTimeEvent(
            event_id=f"event_{len(self.events)}",
            event_type=EventType.SCROLL,
            timestamp=timestamp,
            position={"x": x, "y": y},
            scroll_direction="up" if dy > 0 else "down",
            metadata={"screen_size": {"width": self.screen_width, "height": self.screen_height}, "monitors": self.monitors}
        )
        self.events.append(event_obj)
        logger.info(f"Scroll capturado: {'up' if dy > 0 else 'down'} em ({x}, {y})")

    def _on_key_press(self, key):
        """Callback para pressionamento de tecla"""
        if not self.is_monitoring:
            return
            
        timestamp = datetime.now()
        try:
            key_name = key.char
        except Exception:
            key_name = str(key).split(".")[-1].lower()
        event_obj = RealTimeEvent(
            event_id=f"event_{len(self.events)}",
            event_type=EventType.KEY_PRESS,
            timestamp=timestamp,
            key=key_name,
            metadata={"screen_size": {"width": self.screen_width, "height": self.screen_height}}
        )
        self.events.append(event_obj)
        self.keypress_count += 1
        logger.info(f"Tecla pressionada: {key_name} - Total: {self.keypress_count}")

    def _record_mouse_move(self, position):
        """Registra um evento de movimento do mouse"""
        timestamp = datetime.now()
        event_obj = RealTimeEvent(
            event_id=f"event_{len(self.events)}",
            event_type=EventType.MOUSE_MOVE,
            timestamp=timestamp,
            position=position,
            metadata={"screen_size": {"width": self.screen_width, "height": self.screen_height}, "monitors": self.monitors}
        )
        self.events.append(event_obj)

    def get_click_and_key_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de cliques e teclas pressionadas"""
        if not self.start_time:
            return {"total_clicks": self.click_count, "total_keypresses": self.keypress_count, "clicks_per_minute": 0.0, "keys_per_minute": 0.0, "session_duration_seconds": 0.0}
            
        duration_seconds = (datetime.now() - self.start_time).total_seconds()
        duration_minutes = duration_seconds / 60
        return {
            "total_clicks": self.click_count, 
            "total_keypresses": self.keypress_count, 
            "clicks_per_minute": self.click_count / duration_minutes if duration_minutes > 0 else 0.0, 
            "keys_per_minute": self.keypress_count / duration_minutes if duration_minutes > 0 else 0.0, 
            "session_duration_seconds": duration_seconds
        }

    def show_live_stats(self):
        """Exibe estatísticas em tempo real no console"""
        if not self.is_monitoring:
            print("❌ Monitoramento não está ativo")
            return
            
        stats = self.get_click_and_key_stats()
        print("\033[H\033[J")  # Limpa o console
        print("\n" + "=" * 50)
        print("📊 ESTATÍSTICAS EM TEMPO REAL")
        print("=" * 50)
        print(f"🖱️  Cliques totais: {stats['total_clicks']}")
        print(f"⌨️  Teclas totais: {stats['total_keypresses']}")
        print(f"⏱️  Duração: {stats['session_duration_seconds']:.1f}s")
        print(f"📈 Cliques/min: {stats['clicks_per_minute']:.1f}")
        print(f"📈 Teclas/min: {stats['keys_per_minute']:.1f}")
        print("=" * 50)

    def get_session_summary(self) -> Dict[str, Any]:
        """Gera um resumo da sessão de monitoramento"""
        if not self.events or self.start_time is None:
            return {
                "status": "no_events", 
                "session_start": None, 
                "session_duration_seconds": 0, 
                "total_events": 0, 
                "event_counts": {}, 
                "events_per_minute": {}, 
                "total_clicks": 0, 
                "total_keypresses": 0, 
                "click_hotspots": [], 
                "activity_level": "Nenhuma", 
                "current_time": datetime.now().isoformat(), 
                "screen_info": {"width": self.screen_width, "height": self.screen_height, "monitors": self.monitors}
            }
            
        duration = (datetime.now() - self.start_time).total_seconds()
        event_counts = defaultdict(int)
        
        # Conta eventos por tipo
        for event in self.events:
            event_counts[event.event_type.value] += 1
            
        # Calcula eventos por minuto
        events_per_minute = {}
        for event_type, count in event_counts.items():
            events_per_minute[event_type] = (count / duration * 60) if duration > 0 else 0
            
        # Identifica hotspots de cliques
        click_positions = [event.position for event in self.events if event.event_type == EventType.MOUSE_CLICK and event.position]
        hotspots = []
        if click_positions:
            region_clicks = defaultdict(int)
            for pos in click_positions:
                region_x = (pos["x"] // 100) * 100
                region_y = (pos["y"] // 100) * 100
                region_clicks[f"{region_x},{region_y}"] += 1
            hotspots = sorted([{"region": region, "clicks": count} for region, count in region_clicks.items()], key=lambda x: x["clicks"], reverse=True)[:5]
            
        return {
            "session_start": self.start_time.isoformat(), 
            "session_duration_seconds": round(duration, 2), 
            "total_events": len(self.events), 
            "event_counts": dict(event_counts), 
            "events_per_minute": {k: round(v, 2) for k, v in events_per_minute.items()}, 
            "total_clicks": self.click_count, 
            "total_keypresses": self.keypress_count, 
            "click_hotspots": hotspots, 
            "activity_level": self._calculate_activity_level(events_per_minute), 
            "current_time": datetime.now().isoformat(), 
            "screen_info": {"width": self.screen_width, "height": self.screen_height, "monitors": self.monitors}
        }

    def _calculate_activity_level(self, events_per_minute: Dict[str, float]) -> str:
        """Calcula o nível de atividade com base nos eventos por minuto"""
        if not events_per_minute:
            return "Nenhuma"
            
        total_epm = sum(events_per_minute.values())
        if total_epm > 100:
            return "Muito Alta"
        elif total_epm > 50:
            return "Alta"
        elif total_epm > 10:
            return "Média"
        elif total_epm > 0:
            return "Baixa"
        else:
            return "Nenhuma"

    def get_click_heatmap(self) -> Dict[str, Any]:
        """Gera mapa de calor dos cliques em toda a tela"""
        clicks = [
            event for event in self.events
            if event.event_type == EventType.MOUSE_CLICK and event.position
        ]

        if not clicks:
            return {"heatmap": [], "total_clicks": 0}

        # Criar grid 10x10 para heatmap baseado na tela inteira
        grid = [[0 for _ in range(10)] for _ in range(10)]

        for click in clicks:
            x_percent = click.position["x"] / self.screen_width
            y_percent = click.position["y"] / self.screen_height

            grid_x = min(9, int(x_percent * 10))
            grid_y = min(9, int(y_percent * 10))

            grid[grid_y][grid_x] += 1

        return {
            "heatmap": grid,
            "total_clicks": len(clicks),
            "screen_dimensions": {"width": self.screen_width, "height": self.screen_height}
        }

    def export_session_data(self, filename: str = None, calculate_risk: bool = False, auth_override: Optional[AuthenticationData] = None, face_verification_result: Optional[Dict[str, Any]] = None):
        """
        Exporta dados da sessão para JSON.

        Params:
            filename: nome do arquivo (opcional)
            calculate_risk: se True, calcula e injeta o risk_score no relatório IP
            auth_override: se passado, será usado como AuthenticationData para cálculo de risco
            face_verification_result: resultado da verificação facial (sucesso/falha e username)
        """
        device = DeviceEnvironmentSDK()
        data_device = device.export_data('json')
        if isinstance(data_device, str):
            try:
                data_device = json.loads(data_device)
            except Exception:
                data_device = {}

        ip_location = IPLocationSDK()
        ip_info = device.get_network_info() or {}
        ip = ip_info.get('public_ip')

        # SOBRESCREVER o IP se auth_override tiver um IP diferente
        if auth_override and auth_override.ip_address and auth_override.ip_address != ip:
            ip = auth_override.ip_address
            ip_info['public_ip'] = ip

        # gerar relatório IP (pode falhar — tratamos)
        try:
            response_ip = ip_location.generate_comprehensive_report(ip, session_id)
            if isinstance(response_ip, str):
                try:
                    response_ip = json.loads(response_ip)
                except Exception:
                    response_ip = {"ip_report": response_ip}
        except Exception as e:
            logger.error(f"Erro ao gerar relatório IP: {e}")
            response_ip = {}

        if not filename:
            filename = f"session_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "metadata": {
                "export_time": datetime.now().isoformat(),
                "session_duration": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
                "total_events": len(self.events),
                "screen_info": {
                    "width": self.screen_width,
                    "height": self.screen_height,
                    "monitors": self.monitors
                }
            },
            "summary": self.get_session_summary(),
            "heatmap": self.get_click_heatmap(),
            "events": [
                {
                    "event_id": event.event_id,
                    "type": event.event_type.value,
                    "timestamp": event.timestamp.isoformat(),
                    "position": event.position,
                    "key": event.key,
                    "button": event.button,
                    "scroll_direction": event.scroll_direction,
                    "metadata": event.metadata
                }
                for event in self.events
            ]
        }

        # Adicionar informações de verificação facial ao export
        if face_verification_result:
            data["face_verification"] = face_verification_result

        # === cálculo de score/injeção (opcional) ===
        if calculate_risk:
            try:
                scorer = RiskScorer()

                # auth_override tem precedência; caso contrário criamos um auth conservador
                if auth_override is not None:
                    auth = auth_override
                else:
                    auth = AuthenticationData()
                    auth.username = "unknown"
                    auth.ip_address = ip
                    auth.auth_method = AuthMethod.PASSWORD
                    auth.auth_result = AuthResult.SUCCESS
                    auth.consecutive_failures = 0

                risk_result = scorer.calcular_score(ip or "0.0.0.0", session_id, data["summary"], auth)

                # garantir estrutura de security_analysis
                response_ip.setdefault("security_analysis", {})
                # atualizar risk_factors e recommendations com merges se existirem
                existing_factors = response_ip["security_analysis"].get("risk_factors", [])
                merged_factors = existing_factors + [f for f in (risk_result.get("risk_factors") or []) if f not in existing_factors]
                response_ip["security_analysis"]["risk_factors"] = merged_factors

                # adicionar risk_score detalhado
                response_ip["security_analysis"]["risk_score"] = risk_result

                # definir risk_level também no security_analysis de topo
                response_ip["security_analysis"]["risk_level"] = risk_result.get("risk_level", response_ip["security_analysis"].get("risk_level", "unknown"))

                # se houver recomendações geradas pelo scorer (opcional), injetar
                if "recommendations" in risk_result:
                    existing_recs = response_ip["security_analysis"].get("recommendations", [])
                    merged_recs = existing_recs + [r for r in (risk_result.get("recommendations") or []) if r not in existing_recs]
                    response_ip["security_analysis"]["recommendations"] = merged_recs

            except Exception as e:
                logger.error(f"Erro durante cálculo de risco: {e}")

        # === juntar tudo e escrever ===
        try:
            data_device.update(data)
            data_device.update(response_ip)
        except Exception:
            # fallback simples caso data_device não seja dict
            exported = {"device": data_device, "data": data, "ip_report": response_ip}
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(exported, f, indent=2, ensure_ascii=False)
            logger.info(f"Dados exportados para {filename}")
            return filename

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_device, f, indent=2, ensure_ascii=False)
        logger.info(f"Dados exportados para {filename}")
        return filename


class FaceVerifier:
    """Classe para verificação facial usando DeepFace e OpenCV"""
    
    def __init__(self):
        self.known_faces = {}
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.faces_directory = "known_faces"
        self.recognition_threshold = 1.0
        self.verified_user = None  # Armazena o nome do usuário verificado

        if not os.path.exists(self.faces_directory):
            os.makedirs(self.faces_directory)

        self.load_known_faces()

    def load_known_faces(self):
        """Carrega faces conhecidas do diretório especificado"""
        logger.info("Carregando faces conhecidas...")
        try:
            for filename in os.listdir(self.faces_directory):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    name = os.path.splitext(filename)[0].rsplit('_', 1)[0]
                    image_path = os.path.join(self.faces_directory, filename)
                    self._add_face_to_memory(name, image_path)
            logger.info(f"Total de {len(self.known_faces)} faces conhecidas carregadas.")
        except Exception as e:
            logger.error(f"Erro ao carregar faces conhecidas: {e}")

    def _add_face_to_memory(self, name, image_path):
        """Adiciona uma face à memória para reconhecimento futuro"""
        try:
            embedding_objs = DeepFace.represent(
                img_path=image_path,
                model_name="VGG-Face",
                enforce_detection=True
            )
            if embedding_objs:
                embedding = embedding_objs[0]["embedding"]
                self.known_faces[name] = {'embedding': embedding}
                logger.info(f"Face de '{name}' adicionada com sucesso à memória.")
                return True
            else:
                logger.warning(f"Nenhuma face detectada em {image_path} para {name}. Não adicionada.")
                return False
        except Exception as e:
            logger.error(f"Erro ao extrair embedding para {name} de {image_path}: {e}")
            return False

    def register_face(self, name):
        """Registra uma nova face usando a webcam"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Não foi possível abrir a câmera.")
            return

        logger.info("Pressione 's' para salvar a imagem quando uma face for detectada.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(100, 100))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('Registro de Face', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s') and len(faces) > 0:
                filename = f"{name}_{int(time.time())}.jpg"
                filepath = os.path.join(self.faces_directory, filename)
                cv2.imwrite(filepath, frame)
                logger.info(f"Imagem salva em: {filepath}")
                self._add_face_to_memory(name, filepath)
                break
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def verify_face(self):
        """Verifica uma face usando a webcam"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Não foi possível abrir a câmera.")
            return False, "Unknown"

        logger.info("Olhe para a câmera para verificação...")

        start_time = time.time()
        verified = False
        verified_name = "Unknown"
        
        while time.time() - start_time < 10:  # Tenta por 10 segundos
            ret, frame = cap.read()
            if not ret:
                break

            results, processed_frame = self.recognize_face_in_frame(frame)
            cv2.imshow('Verificação de Face', processed_frame)

            for result in results:
                if result['name'] != 'Unknown':
                    verified_name = result['name']
                    logger.info(f"Verificação bem-sucedida! Bem-vindo, {verified_name}!")
                    verified = True
                    break

            if verified:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if not verified:
            logger.warning("Verificação falhou. Rosto não reconhecido.")
        else:
            self.verified_user = verified_name  # Armazena o nome do usuário verificado
            
        cap.release()
        cv2.destroyAllWindows()
        return verified, verified_name

    def recognize_face_in_frame(self, frame):
        """Reconhece faces em um frame de vídeo"""
        results = []
        processed_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(100, 100))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]
            recognized_name = "Unknown"

            if self.known_faces:
                try:
                    face_embedding_objs = DeepFace.represent(
                        img_path=face_roi,
                        model_name="VGG-Face",
                        enforce_detection=False
                    )

                    if face_embedding_objs:
                        face_embedding = face_embedding_objs[0]["embedding"]
                        min_distance = float('inf')
                        temp_recognized_name = "Unknown"

                        for name, face_data in self.known_faces.items():
                            known_embedding = face_data['embedding']
                            distance = np.linalg.norm(np.array(face_embedding) - np.array(known_embedding))

                            if distance < min_distance:
                                min_distance = distance
                                temp_recognized_name = name

                        if min_distance < self.recognition_threshold:
                            recognized_name = temp_recognized_name
                except Exception as e:
                    logger.error(f"Erro durante o reconhecimento: {e}")

            color = (0, 255, 0) if recognized_name != "Unknown" else (0, 0, 255)
            cv2.rectangle(processed_frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(processed_frame, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            results.append({'name': recognized_name})

        return results, processed_frame


# ==================== FUNÇÕES DE TESTE ====================

def test_facial_verification_failure():
    """Teste para simular falha na verificação facial"""
    print("🧪 Iniciando teste de falha na verificação facial...")
    
    # Criar monitor para exportar dados
    monitor = RealTimeMonitor()
    
    # Simular falha de verificação facial
    face_verification_result = {
        "status": "failed",
        "reason": "face_not_recognized",
        "username": "Unknown",
        "timestamp": datetime.now().isoformat()
    }
    
    # Exportar dados de falha de verificação facial
    filename = monitor.export_session_data(
        filename="test_facial_verification_failure.json",
        face_verification_result=face_verification_result
    )
    
    print(f"✅ Teste de falha na verificação facial concluído. Dados exportados para: {filename}")
    return filename


def test_risk_score_100():
    """Teste para simular risco máximo (score 100)"""
    print("🧪 Iniciando teste de risco máximo (score 100)...")
    
    # Criar monitor e simular alguns eventos
    monitor = RealTimeMonitor()
    monitor.start_time = datetime.now() - timedelta(minutes=5)  # Simular sessão de 5 minutos
    
    # Simular muitos eventos para aumentar o risco
    for i in range(100):
        event = RealTimeEvent(
            event_id=f"test_event_{i}",
            event_type=EventType.MOUSE_CLICK,
            timestamp=datetime.now(),
            position={"x": i % monitor.screen_width, "y": i % monitor.screen_height},  # Corrigido: monitor.screen_height
            button="left",
            metadata={"screen_size": {"width": monitor.screen_width, "height": monitor.screen_height}}
        )
        monitor.events.append(event)
        monitor.click_count += 1
    
    # IP fora do Brasil (Google DNS)
    foreign_ip = "8.8.8.8"
    
    # Criar autenticação com dados suspeitos
    auth = AuthenticationData()
    auth.username = "hacker_user"
    auth.ip_address = foreign_ip  # IP fora do Brasil
    auth.auth_method = AuthMethod.PASSWORD
    auth.auth_result = AuthResult.SUCCESS
    auth.consecutive_failures = 0
    
    # Resultado de verificação facial (simulado)
    face_verification_result = {
        "status": "success",
        "username": "hacker_user",
        "timestamp": datetime.now().isoformat()
    }
    
    # Forçar cálculo de risco alto
    try:
        # Exportar dados com cálculo de risco
        filename = monitor.export_session_data(
            filename="test_risk_score_100.json",
            calculate_risk=True,
            auth_override=auth,
            face_verification_result=face_verification_result
        )
        
        print(f"✅ Teste de risco máximo concluído. Dados exportados para: {filename}")
        
        # Verificar se o JSON contém os fatores de risco
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Verificar se há fatores de risco no JSON
            risk_factors = []
            if 'security_analysis' in data and 'risk_factors' in data['security_analysis']:
                risk_factors = data['security_analysis']['risk_factors']
                print(f"📋 Fatores de risco encontrados no JSON: {len(risk_factors)}")
                for factor in risk_factors:
                    print(f"   • {factor}")
            else:
                print("❌ Nenhum fator de risco encontrado no JSON")
                
            # Verificar se o IP está configurado como fora do Brasil
            ip_in_json = None
            if 'ip' in data:
                ip_in_json = data['ip']
            elif 'ip_address' in data:
                ip_in_json = data['ip_address']
            elif 'device' in data and 'network_info' in data['device'] and 'public_ip' in data['device']['network_info']:
                ip_in_json = data['device']['network_info']['public_ip']
                
            if ip_in_json == foreign_ip:
                print(f"🌎 IP configurado como fora do Brasil: {ip_in_json}")
            else:
                print(f"❌ IP incorreto. Esperado: {foreign_ip}, Encontrado: {ip_in_json}")
                
        except Exception as e:
            print(f"❌ Erro ao verificar o arquivo JSON: {e}")
            
        return filename
    except Exception as e:
        print(f"❌ Erro durante teste de risco máximo: {e}")
        return None
        
def run_tests():
    """Executa todos os testes"""
    print("🚀 Iniciando testes...")
    
    # Teste 1: Falha na verificação facial
    test1_result = test_facial_verification_failure()
    
    # Teste 2: Risco máximo (score 100)
    test2_result = test_risk_score_100()
    
    print("\n" + "="*50)
    print("📊 RESULTADOS DOS TESTES")
    print("="*50)
    print(f"Teste 1 - Falha verificação facial: {'✅' if test1_result else '❌'}")
    print(f"Teste 2 - Risco máximo: {'✅' if test2_result else '❌'}")
    print("="*50)


if __name__ == "__main__":
    # Verificar se é modo de teste
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
        exit(0)
    
    # Modo normal de execução
    verifier = FaceVerifier()
    face_verified = False
    verified_username = "Unknown"

    # Criar monitor para exportar dados mesmo se verificação falhar
    monitor = RealTimeMonitor()
    
    # Verificar se há faces conhecidas
    if not verifier.known_faces:
        logger.error("Nenhuma face conhecida encontrada. Verificação facial falhou.")
        # Exportar dados de falha de verificação facial
        face_verification_result = {
            "status": "failed",
            "reason": "no_known_faces",
            "username": "Unknown",
            "timestamp": datetime.now().isoformat()
        }
        filename = monitor.export_session_data(face_verification_result=face_verification_result)
        logger.info(f"Dados de falha de verificação exportados para: {filename}")
        exit(1)
    else:
        logger.info("Tentando verificar a face existente...")
        face_verified, verified_username = verifier.verify_face()

    # Se a verificação facial falhou, exportar dados e sair
    if not face_verified:
        logger.error("Verificação facial falhou.")
        # Exportar dados de falha de verificação facial
        face_verification_result = {
            "status": "failed",
            "reason": "face_not_recognized",
            "username": "Unknown",
            "timestamp": datetime.now().isoformat()
        }
        filename = monitor.export_session_data(face_verification_result=face_verification_result)
        logger.info(f"Dados de falha de verificação exportados para: {filename}")
        exit(1)

    # Se chegou aqui, face_verified == True - verificação bem-sucedida
    logger.info(f"Verificação facial bem-sucedida para {verified_username}. Iniciando o monitoramento de comportamento.")
    monitor.start_monitoring()

    scorer = RiskScorer()
    device = DeviceEnvironmentSDK()
    ip_info = device.get_network_info() or {}
    ip = ip_info.get("public_ip")

    # Configurar autenticação com o nome do usuário verificado
    auth = AuthenticationData()
    auth.username = verified_username  # Usar o nome reconhecido pelo FaceVerifier
    auth.ip_address = ip_info.get("public_ip", "0.0.0.0")
    auth.auth_method = AuthMethod.PASSWORD
    auth.auth_result = AuthResult.SUCCESS  # Assumir sucesso já que a verificação facial foi bem-sucedida
    auth.consecutive_failures = 0

    # Resultado da verificação facial para incluir no export
    face_verification_result = {
        "status": "success",
        "username": verified_username,
        "timestamp": datetime.now().isoformat()
    }

    try:
        while True:
            monitor.show_live_stats()
            summary = monitor.get_session_summary()

            # calcula score periodicamente (aqui a cada loop)
            result = scorer.calcular_score(auth.ip_address or (ip or "0.0.0.0"), session_id, summary, auth)
            
            # Exibir informações de risco detalhadas
            print(f"\n🔎 Score Atual: {result['score']} ({result['risk_level']})")
            if "risk_factors" in result and result["risk_factors"]:
                print("📋 Fatores de Risco:")
                for factor in result["risk_factors"]:
                    print(f"   • {factor}")
            if "recommendations" in result and result["recommendations"]:
                print("💡 Recomendações:")
                for recommendation in result["recommendations"]:
                    print(f"   • {recommendation}")
            
            if result["score"] >= 100:
                print("⚠️ Desligando atividade suspeita de usuário")
                # exporta dados com cálculo de risco ativo (passamos o auth usado e resultado da verificação facial)
                try:
                    filename = monitor.export_session_data(calculate_risk=True, auth_override=auth, face_verification_result=face_verification_result)
                    print(f"\n💾 Dados exportados para: {filename}")
                except Exception as e:
                    logger.error(f"Erro ao exportar dados após detecção de risco: {e}")
                monitor.stop_monitoring()
                exit(1)

            time.sleep(1)

    except KeyboardInterrupt:
        try:
            # ao finalizar por KeyboardInterrupt, exporta com cálculo de risco e resultado da verificação facial
            filename = monitor.export_session_data(calculate_risk=True, auth_override=auth, face_verification_result=face_verification_result)
            print(f"\n💾 Dados exportados para: {filename}")
        except Exception as e:
            print(f"❌ Erro ao exportar dados: {e}")
        finally:
            monitor.stop_monitoring()
            print("\n👋 Monitoramento finalizado.")