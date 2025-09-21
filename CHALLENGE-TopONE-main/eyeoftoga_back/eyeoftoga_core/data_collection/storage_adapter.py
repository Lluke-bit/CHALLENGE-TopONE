"""
Session Behavior SDK - Monitoramento REAL de Comportamento
Captura interações reais do usuário em tempo real em toda a tela
"""

from dataclasses import dataclass, field
import pygame
import sys
import time
from datetime import datetime
import json
from typing import Dict, List, Optional, Any
from enum import Enum
import threading
from collections import defaultdict
import logging
import pyautogui
from screeninfo import get_monitors

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EventType(Enum):
    MOUSE_CLICK = "mouse_click"
    MOUSE_MOVE = "mouse_move"
    KEY_PRESS = "key_press"
    WINDOW_FOCUS = "window_focus"
    SCROLL = "scroll"
    DRAG = "drag"

@dataclass
class RealTimeEvent:
    event_id: str
    event_type: EventType
    timestamp: datetime
    position: Optional[Dict[str, int]] = None
    key: Optional[str] = None
    button: Optional[str] = None
    scroll_direction: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class RealTimeMonitor:
    def __init__(self):
        self.events: List[RealTimeEvent] = []
        self.is_monitoring = False
        self.monitor_thread = None
        self.last_position = None
        self.click_count = 0
        self.keypress_count = 0
        self.start_time = None
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Obter informações sobre todos os monitores
        self.monitors = []
        for m in get_monitors():
            self.monitors.append({
                "x": m.x,
                "y": m.y,
                "width": m.width,
                "height": m.height,
                "name": str(m.name)
            })
        
        logger.info(f"Tela detectada: {self.screen_width}x{self.screen_height}")
        logger.info(f"Monitores detectados: {len(self.monitors)}")
        
        # Configuração do pygame para visualização (opcional)
        pygame.init()
        self.screen = pygame.display.set_mode((300, 200))
        pygame.display.set_caption("EyeOfToga Monitor")
        
    def start_monitoring(self):
        """Inicia o monitoramento em tempo real"""
        if self.is_monitoring:
            logger.warning("Monitoramento já está ativo")
            return
            
        self.is_monitoring = True
        self.start_time = datetime.now()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Monitoramento iniciado - Capturando suas interações em toda a tela...")
        
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        logger.info("Monitoramento parado")
        
    def _monitor_loop(self):
        """Loop principal de monitoramento usando pyautogui para capturar eventos em toda a tela"""
        try:
            # Configurar callbacks do pyautogui
            pygame_event_types = {
                pygame.MOUSEBUTTONDOWN: self._process_mouse_click,
                pygame.MOUSEMOTION: self._process_mouse_move,
                pygame.KEYDOWN: self._process_key_press
            }
            
            while self.is_monitoring:
                # Capturar a posição atual do mouse em toda a tela
                current_x, current_y = pyautogui.position()
                current_pos = {"x": current_x, "y": current_y}
                
                # Registrar movimento se significativo
                if self.last_position and (
                    abs(current_pos["x"] - self.last_position["x"]) > 2 or
                    abs(current_pos["y"] - self.last_position["y"]) > 2
                ):
                    self._record_mouse_move(current_pos)
                
                self.last_position = current_pos
                
                # Processar eventos do pygame (para interface)
                for event in pygame.event.get():
                    if event.type in pygame_event_types:
                        pygame_event_types[event.type](event)
                    elif event.type == pygame.QUIT:
                        self.is_monitoring = False
                
                time.sleep(0.01)  # Pequena pausa para não sobrecarregar
                
        except Exception as e:
            logger.error(f"Erro no loop de monitoramento: {e}")
            
    def _process_mouse_click(self, event):
        """Processa cliques do mouse em toda a tela"""
        timestamp = datetime.now()
        current_x, current_y = pyautogui.position()
        
        button_map = {1: "left", 2: "middle", 3: "right", 4: "scroll_up", 5: "scroll_down"}
        button = button_map.get(event.button, f"button_{event.button}")
        
        if event.button in [4, 5]:  # Scroll
            event_obj = RealTimeEvent(
                event_id=f"event_{len(self.events)}",
                event_type=EventType.SCROLL,
                timestamp=timestamp,
                position={"x": current_x, "y": current_y},
                scroll_direction="up" if event.button == 4 else "down",
                metadata={
                    "screen_size": {"width": self.screen_width, "height": self.screen_height},
                    "monitors": self.monitors
                }
            )
        else:  # Clique normal
            event_obj = RealTimeEvent(
                event_id=f"event_{len(self.events)}",
                event_type=EventType.MOUSE_CLICK,
                timestamp=timestamp,
                position={"x": current_x, "y": current_y},
                button=button,
                metadata={
                    "screen_size": {"width": self.screen_width, "height": self.screen_height},
                    "monitors": self.monitors
                }
            )
            self.click_count += 1
            
        self.events.append(event_obj)
        logger.info(f"Clique capturado: {button} em ({current_x}, {current_y})")
    
    def _record_mouse_move(self, position):
        """Registra movimento do mouse"""
        timestamp = datetime.now()
        
        event_obj = RealTimeEvent(
            event_id=f"event_{len(self.events)}",
            event_type=EventType.MOUSE_MOVE,
            timestamp=timestamp,
            position=position,
            metadata={
                "screen_size": {"width": self.screen_width, "height": self.screen_height},
                "monitors": self.monitors
            }
        )
        self.events.append(event_obj)
    
    def _process_mouse_move(self, event):
        """Processa movimento do mouse (usando pyautogui em vez das coordenadas do pygame)"""
        # O movimento já é tratado no loop principal usando pyautogui.position()
        pass
        
    def _process_key_press(self, event):
        """Processa teclas pressionadas"""
        timestamp = datetime.now()
        key_name = pygame.key.name(event.key)
        
        event_obj = RealTimeEvent(
            event_id=f"event_{len(self.events)}",
            event_type=EventType.KEY_PRESS,
            timestamp=timestamp,
            key=key_name,
            metadata={
                "modifiers": {
                    "shift": bool(event.mod & pygame.KMOD_SHIFT),
                    "ctrl": bool(event.mod & pygame.KMOD_CTRL),
                    "alt": bool(event.mod & pygame.KMOD_ALT)
                },
                "screen_size": {"width": self.screen_width, "height": self.screen_height}
            }
        )
        self.events.append(event_obj)
        self.keypress_count += 1
        logger.info(f"Tecla pressionada: {key_name}")
            
    def get_session_summary(self) -> Dict[str, Any]:
        """Retorna resumo da sessão de monitoramento"""
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
                "screen_info": {
                    "width": self.screen_width,
                    "height": self.screen_height,
                    "monitors": self.monitors
                }
            }
            
        duration = (datetime.now() - self.start_time).total_seconds()
        
        # Contar eventos por tipo
        event_counts = defaultdict(int)
        for event in self.events:
            event_counts[event.event_type.value] += 1
            
        # Calcular taxa de eventos por minuto
        events_per_minute = {}
        for event_type, count in event_counts.items():
            events_per_minute[event_type] = (count / duration * 60) if duration > 0 else 0
        
        # Encontrar áreas mais clicadas
        click_positions = [
            event.position for event in self.events 
            if event.event_type == EventType.MOUSE_CLICK and event.position
        ]
        
        hotspots = []
        if click_positions:
            # Agrupar cliques por região (100x100 pixels para toda a tela)
            region_clicks = defaultdict(int)
            for pos in click_positions:
                region_x = (pos["x"] // 100) * 100
                region_y = (pos["y"] // 100) * 100
                region_clicks[f"{region_x},{region_y}"] += 1
                
            hotspots = sorted(
                [{"region": region, "clicks": count} 
                 for region, count in region_clicks.items()],
                key=lambda x: x["clicks"],
                reverse=True
            )[:5]  # Top 5 hotspots
        
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
            "screen_info": {
                "width": self.screen_width,
                "height": self.screen_height,
                "monitors": self.monitors
            }
        }
        
    def _calculate_activity_level(self, events_per_minute: Dict[str, float]) -> str:
        """Calcula nível de atividade baseado em eventos por minuto"""
        if not events_per_minute:
            return "Nenhuma"
            
        total_epm = sum(events_per_minute.values())
        
        if total_epm > 100:
            return "Muito Alta"
        elif total_epm > 50:
            return "Alta"
        elif total_epm > 20:
            return "Moderada"
        elif total_epm > 5:
            return "Baixa"
        else:
            return "Muito Baixa"
            
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
        
    def export_session_data(self, filename: str = None):
        """Exporta dados da sessão para JSON"""
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
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Dados exportados para {filename}")
        return filename

# Interface interativa para demonstração
def interactive_demo():
    """Demonstração interativa do monitoramento"""
    monitor = RealTimeMonitor()
    
    print("🎯 EyeOfToga - Monitor de Comportamento em Tempo Real")
    print("=" * 60)
    print("Este programa vai capturar suas interações em TODA A TELA:")
    print("• Cliques do mouse em qualquer lugar")
    print("• Movimentos do mouse em qualquer lugar") 
    print("• Teclas pressionadas")
    print("• Scroll")
    print()
    print(f"Tela detectada: {monitor.screen_width}x{monitor.screen_height}")
    print(f"Monitores: {len(monitor.monitors)}")
    for i, m in enumerate(monitor.monitors):
        print(f"  Monitor {i+1}: {m['width']}x{m['height']} at ({m['x']}, {m['y']})")
    print()
    print("Pressione ESC para parar o monitoramento")
    print()
    
    input("Pressione Enter para iniciar...")
    
    # Iniciar monitoramento
    monitor.start_monitoring()
    
    try:
        last_summary_time = time.time()
        
        while monitor.is_monitoring:
            # Atualizar display a cada 2 segundos
            if time.time() - last_summary_time > 2:
                summary = monitor.get_session_summary()
                
                # Limpar console e mostrar informações
                print("\033[H\033[J")  # Clear screen
                print("📊 Monitoramento Ativo - EyeOfToga (Toda a Tela)")
                print("=" * 50)
                print(f"⏱️  Duração: {summary.get('session_duration_seconds', 0):.1f}s")
                print(f"📈 Nível de atividade: {summary.get('activity_level', 'Nenhuma')}")
                print(f"🖱️  Total cliques: {summary.get('total_clicks', 0)}")
                print(f"⌨️  Total teclas: {summary.get('total_keypresses', 0)}")
                print(f"📋 Total eventos: {summary.get('total_events', 0)}")
                print()
                
                # Mostrar eventos por minuto
                print("Eventos por minuto:")
                for event_type, epm in summary.get('events_per_minute', {}).items():
                    print(f"  {event_type}: {epm:.1f}")
                
                # Mostrar posição atual do mouse
                try:
                    x, y = pyautogui.position()
                    print(f"📍 Posição atual do mouse: ({x}, {y})")
                except:
                    pass
                
                print()
                print("Pressione ESC para parar...")
                
                last_summary_time = time.time()
                
            # Processar eventos (manter o pygame responsivo)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    monitor.is_monitoring = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    monitor.is_monitoring = False
                    
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nParando monitoramento...")
    except Exception as e:
        print(f"\nErro durante o monitoramento: {e}")
    finally:
        monitor.stop_monitoring()
        
        # Mostrar relatório final
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DA SESSÃO (Toda a Tela)")
        print("=" * 60)
        
        final_summary = monitor.get_session_summary()
        heatmap = monitor.get_click_heatmap()
        
        print(f"⏰ Duração total: {final_summary.get('session_duration_seconds', 0):.1f} segundos")
        print(f"🎯 Total de eventos: {final_summary.get('total_events', 0)}")
        print(f"🖱️  Cliques registrados: {final_summary.get('total_clicks', 0)}")
        print(f"⌨️  Teclas pressionadas: {final_summary.get('total_keypresses', 0)}")
        print(f"📈 Nível de atividade: {final_summary.get('activity_level', 'Nenhuma')}")
        print()
        
        print("📋 Distribuição de eventos:")
        for event_type, count in final_summary.get('event_counts', {}).items():
            print(f"  {event_type}: {count} eventos")
        
        print()
        print("🗺️  Áreas mais clicadas:")
        for hotspot in final_summary.get('click_hotspots', [])[:3]:
            coords = hotspot.get('region', '0,0').split(',')
            x, y = int(coords[0]), int(coords[1])
            print(f"  Região ({x}-{x+100}, {y}-{y+100}): {hotspot.get('clicks', 0)} cliques")
        
        # Exportar dados
        try:
            filename = monitor.export_session_data()
            print(f"\n💾 Dados exportados para: {filename}")
        except Exception as e:
            print(f"\n❌ Erro ao exportar dados: {e}")
        
        print("\n🎉 Análise comportamental concluída!")

# Função simplificada para análise de padrões
def analyze_behavior_patterns(events: List[RealTimeEvent]) -> Dict[str, Any]:
    """Analisa padrões comportamentais básicos"""
    if not events:
        return {"error": "No events to analyze"}
    
    # Separar eventos por tipo
    clicks = [e for e in events if e.event_type == EventType.MOUSE_CLICK]
    moves = [e for e in events if e.event_type == EventType.MOUSE_MOVE]
    keypresses = [e for e in events if e.event_type == EventType.KEY_PRESS]
    
    # Análise básica
    return {
        "total_events": len(events),
        "mouse_clicks": len(clicks),
        "mouse_movements": len(moves),
        "key_presses": len(keypresses),
        "unique_keys": len(set(e.key for e in keypresses if e.key)),
        "analysis_timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Executar demonstração interativa
    interactive_demo()