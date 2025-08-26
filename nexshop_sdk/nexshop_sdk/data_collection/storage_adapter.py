"""
Storage Adapter SDK - Persistência e Coleta de Dados Avançados
Desenvolvido para TCC - Curso de Cyber Segurança

Funcionalidades:
- Abstração para persistência (Cache/DB)
- Dados de segurança e integridade
- Telemetria e performance avançada
- Dados de aplicação e transação
- Sistema avançado de antifraude
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib
import hmac
import base64
import time
import threading
import psutil
import platform
import ssl
import socket
import subprocess
import os
import sys
import gc
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
import logging
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import sqlite3
import redis
import uuid
import statistics
from functools import wraps
import traceback

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorageType(Enum):
    """Tipos de armazenamento suportados"""
    MEMORY = "memory"
    SQLITE = "sqlite"
    REDIS = "redis"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"


class TransactionStatus(Enum):
    """Status das transações"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PROCESSING = "processing"


class PaymentMethod(Enum):
    """Métodos de pagamento"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PIX = "pix"
    BOLETO = "boleto"
    PAYPAL = "paypal"
    CRYPTO = "crypto"
    BANK_TRANSFER = "bank_transfer"


class SecurityLevel(Enum):
    """Níveis de segurança"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============= DATA CLASSES =============

@dataclass
class SecurityData:
    """Dados de segurança e integridade"""
    session_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    payload_hash_sha256: str = ""
    payload_hash_md5: str = ""
    digital_signature: str = ""
    signature_valid: bool = False
    unauthorized_attempts: int = 0
    suspicious_parameter_changes: List[str] = field(default_factory=list)
    header_bypass_attempts: List[Dict[str, Any]] = field(default_factory=list)
    loaded_plugins: List[str] = field(default_factory=list)
    loaded_extensions: List[str] = field(default_factory=list)
    tls_version: str = ""
    cipher_suite: str = ""
    certificate_valid: bool = False
    transport_encrypted: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class PerformanceData:
    """Dados de telemetria e performance"""
    session_id: str = ""
    request_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    cpu_usage_percent: float = 0.0
    memory_usage_mb: float = 0.0
    memory_peak_mb: float = 0.0
    disk_read_bytes: int = 0
    disk_write_bytes: int = 0
    network_sent_bytes: int = 0
    network_received_bytes: int = 0
    execution_time_ms: float = 0.0
    function_timings: Dict[str, float] = field(default_factory=dict)
    latency_avg_ms: float = 0.0
    latency_max_ms: float = 0.0
    network_errors: List[str] = field(default_factory=list)
    custom_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class ApplicationData:
    """Dados da aplicação"""
    session_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    sdk_version: str = "1.0.0"
    python_version: str = field(default_factory=lambda: sys.version)
    platform_info: str = field(default_factory=lambda: platform.platform())
    runtime_config: Dict[str, Any] = field(default_factory=dict)
    loaded_modules: List[str] = field(default_factory=list)
    loaded_libraries: List[str] = field(default_factory=list)
    debug_mode: bool = False
    production_mode: bool = True
    environment: str = "production"
    feature_flags: Dict[str, bool] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class TransactionData:
    """Dados de transação e negócio"""
    transaction_id: str = ""
    session_id: str = ""
    order_id: str = ""
    purchase_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    amount: float = 0.0
    currency: str = "BRL"
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    status: TransactionStatus = TransactionStatus.PENDING
    product_id: str = ""
    service_id: str = ""
    product_name: str = ""
    is_recurring: bool = False
    subscription_id: str = ""
    billing_cycle: str = ""
    related_transactions: List[str] = field(default_factory=list)
    correlation_data: Dict[str, Any] = field(default_factory=dict)
    merchant_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['payment_method'] = self.payment_method.value
        data['status'] = self.status.value
        return data


@dataclass
class AntiFraudData:
    """Dados avançados para antifraude"""
    session_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    device_fingerprint: str = ""
    screen_resolution: str = ""
    browser_fingerprint: str = ""
    typing_patterns: Dict[str, float] = field(default_factory=dict)
    interaction_patterns: Dict[str, Any] = field(default_factory=dict)
    running_processes_server: List[str] = field(default_factory=list)
    running_processes_client: List[str] = field(default_factory=list)
    ip_changes: List[Dict[str, Any]] = field(default_factory=list)
    rapid_ip_changes: int = 0
    blacklist_matches: List[str] = field(default_factory=list)
    geolocation_anomalies: List[str] = field(default_factory=list)
    behavioral_anomalies: List[str] = field(default_factory=list)
    device_inconsistencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


# ============= STORAGE INTERFACES =============

class StorageInterface(ABC):
    """Interface abstrata para armazenamento"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Conecta ao armazenamento"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Desconecta do armazenamento"""
        pass
    
    @abstractmethod
    def store_data(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """Armazena dados"""
        pass
    
    @abstractmethod
    def retrieve_data(self, key: str) -> Optional[Any]:
        """Recupera dados"""
        pass
    
    @abstractmethod
    def delete_data(self, key: str) -> bool:
        """Remove dados"""
        pass
    
    @abstractmethod
    def list_keys(self, pattern: str = "*") -> List[str]:
        """Lista chaves"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do armazenamento"""
        pass


# ============= STORAGE IMPLEMENTATIONS =============

class MemoryStorage(StorageInterface):
    """Armazenamento em memória (para desenvolvimento/testes)"""
    
    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
        self._ttl: Dict[str, datetime] = {}
        self._lock = threading.Lock()
        self.connected = False
    
    def connect(self) -> bool:
        """Conecta (sempre disponível em memória)"""
        self.connected = True
        logger.info("MemoryStorage: Conectado")
        return True
    
    def disconnect(self) -> bool:
        """Desconecta"""
        with self._lock:
            self._data.clear()
            self._ttl.clear()
        self.connected = False
        logger.info("MemoryStorage: Desconectado")
        return True
    
    def store_data(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """Armazena dados em memória"""
        try:
            with self._lock:
                self._data[key] = {
                    'data': data,
                    'stored_at': datetime.now(),
                    'accessed_at': datetime.now()
                }
                
                if ttl:
                    self._ttl[key] = datetime.now() + timedelta(seconds=ttl)
                
                logger.debug(f"MemoryStorage: Dados armazenados para chave '{key}'")
                return True
        except Exception as e:
            logger.error(f"MemoryStorage: Erro ao armazenar dados: {str(e)}")
            return False
    
    def retrieve_data(self, key: str) -> Optional[Any]:
        """Recupera dados da memória"""
        try:
            with self._lock:
                # Verificar TTL
                if key in self._ttl and datetime.now() > self._ttl[key]:
                    del self._data[key]
                    del self._ttl[key]
                    return None
                
                if key in self._data:
                    self._data[key]['accessed_at'] = datetime.now()
                    return self._data[key]['data']
                
                return None
        except Exception as e:
            logger.error(f"MemoryStorage: Erro ao recuperar dados: {str(e)}")
            return None
    
    def delete_data(self, key: str) -> bool:
        """Remove dados da memória"""
        try:
            with self._lock:
                if key in self._data:
                    del self._data[key]
                if key in self._ttl:
                    del self._ttl[key]
                return True
        except Exception as e:
            logger.error(f"MemoryStorage: Erro ao deletar dados: {str(e)}")
            return False
    
    def list_keys(self, pattern: str = "*") -> List[str]:
        """Lista chaves (implementação simples)"""
        with self._lock:
            if pattern == "*":
                return list(self._data.keys())
            else:
                # Implementação básica de pattern matching
                import fnmatch
                return [key for key in self._data.keys() if fnmatch.fnmatch(key, pattern)]
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do armazenamento em memória"""
        with self._lock:
            return {
                "status": "healthy" if self.connected else "disconnected",
                "total_keys": len(self._data),
                "memory_usage_mb": sum(sys.getsizeof(item) for item in self._data.values()) / 1024 / 1024,
                "connected": self.connected
            }


class SQLiteStorage(StorageInterface):
    """Armazenamento SQLite"""
    
    def __init__(self, db_path: str = "storage_adapter.db"):
        self.db_path = db_path
        self.connection = None
        self._lock = threading.Lock()
    
    def connect(self) -> bool:
        """Conecta ao SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS storage_data (
                    key TEXT PRIMARY KEY,
                    data TEXT,
                    stored_at TIMESTAMP,
                    accessed_at TIMESTAMP,
                    ttl_expires_at TIMESTAMP
                )
            """)
            self.connection.commit()
            logger.info(f"SQLiteStorage: Conectado ao banco {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"SQLiteStorage: Erro ao conectar: {str(e)}")
            return False
    
    def disconnect(self) -> bool:
        """Desconecta do SQLite"""
        try:
            if self.connection:
                self.connection.close()
            logger.info("SQLiteStorage: Desconectado")
            return True
        except Exception as e:
            logger.error(f"SQLiteStorage: Erro ao desconectar: {str(e)}")
            return False
    
    def store_data(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """Armazena dados no SQLite"""
        try:
            with self._lock:
                data_json = json.dumps(data, default=str)
                now = datetime.now()
                ttl_expires = now + timedelta(seconds=ttl) if ttl else None
                
                self.connection.execute("""
                    INSERT OR REPLACE INTO storage_data 
                    (key, data, stored_at, accessed_at, ttl_expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (key, data_json, now, now, ttl_expires))
                
                self.connection.commit()
                logger.debug(f"SQLiteStorage: Dados armazenados para chave '{key}'")
                return True
        except Exception as e:
            logger.error(f"SQLiteStorage: Erro ao armazenar dados: {str(e)}")
            return False
    
    def retrieve_data(self, key: str) -> Optional[Any]:
        """Recupera dados do SQLite"""
        try:
            with self._lock:
                cursor = self.connection.cursor()
                cursor.execute("""
                    SELECT data, ttl_expires_at FROM storage_data 
                    WHERE key = ?
                """, (key,))
                
                result = cursor.fetchone()
                if not result:
                    return None
                
                data_json, ttl_expires = result
                
                # Verificar TTL
                if ttl_expires:
                    ttl_datetime = datetime.fromisoformat(ttl_expires) if isinstance(ttl_expires, str) else ttl_expires
                    if datetime.now() > ttl_datetime:
                        self.delete_data(key)
                        return None
                
                # Atualizar último acesso
                self.connection.execute("""
                    UPDATE storage_data SET accessed_at = ? WHERE key = ?
                """, (datetime.now(), key))
                self.connection.commit()
                
                return json.loads(data_json)
                
        except Exception as e:
            logger.error(f"SQLiteStorage: Erro ao recuperar dados: {str(e)}")
            return None
    
    def delete_data(self, key: str) -> bool:
        """Remove dados do SQLite"""
        try:
            with self._lock:
                self.connection.execute("DELETE FROM storage_data WHERE key = ?", (key,))
                self.connection.commit()
                return True
        except Exception as e:
            logger.error(f"SQLiteStorage: Erro ao deletar dados: {str(e)}")
            return False
    
    def list_keys(self, pattern: str = "*") -> List[str]:
        """Lista chaves do SQLite"""
        try:
            with self._lock:
                cursor = self.connection.cursor()
                if pattern == "*":
                    cursor.execute("SELECT key FROM storage_data")
                else:
                    cursor.execute("SELECT key FROM storage_data WHERE key LIKE ?", (pattern.replace("*", "%"),))
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"SQLiteStorage: Erro ao listar chaves: {str(e)}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do SQLite"""
        try:
            with self._lock:
                cursor = self.connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM storage_data")
                total_keys = cursor.fetchone()[0]
                
                # Verificar tamanho do arquivo
                db_size_mb = os.path.getsize(self.db_path) / 1024 / 1024 if os.path.exists(self.db_path) else 0
                
                return {
                    "status": "healthy",
                    "total_keys": total_keys,
                    "db_size_mb": round(db_size_mb, 2),
                    "db_path": self.db_path,
                    "connected": self.connection is not None
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "connected": False
            }


class RedisStorage(StorageInterface):
    """Armazenamento Redis"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.connection = None
    
    def connect(self) -> bool:
        """Conecta ao Redis"""
        try:
            import redis
            self.connection = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
            # Testar conexão
            self.connection.ping()
            logger.info(f"RedisStorage: Conectado ao Redis {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"RedisStorage: Erro ao conectar: {str(e)}")
            return False
    
    def disconnect(self) -> bool:
        """Desconecta do Redis"""
        try:
            if self.connection:
                self.connection.close()
            logger.info("RedisStorage: Desconectado")
            return True
        except Exception as e:
            logger.error(f"RedisStorage: Erro ao desconectar: {str(e)}")
            return False
    
    def store_data(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """Armazena dados no Redis"""
        try:
            data_json = json.dumps(data, default=str)
            if ttl:
                self.connection.setex(key, ttl, data_json)
            else:
                self.connection.set(key, data_json)
            
            logger.debug(f"RedisStorage: Dados armazenados para chave '{key}'")
            return True
        except Exception as e:
            logger.error(f"RedisStorage: Erro ao armazenar dados: {str(e)}")
            return False
    
    def retrieve_data(self, key: str) -> Optional[Any]:
        """Recupera dados do Redis"""
        try:
            data_json = self.connection.get(key)
            if data_json:
                return json.loads(data_json)
            return None
        except Exception as e:
            logger.error(f"RedisStorage: Erro ao recuperar dados: {str(e)}")
            return None
    
    def delete_data(self, key: str) -> bool:
        """Remove dados do Redis"""
        try:
            self.connection.delete(key)
            return True
        except Exception as e:
            logger.error(f"RedisStorage: Erro ao deletar dados: {str(e)}")
            return False
    
    def list_keys(self, pattern: str = "*") -> List[str]:
        """Lista chaves do Redis"""
        try:
            return list(self.connection.scan_iter(match=pattern))
        except Exception as e:
            logger.error(f"RedisStorage: Erro ao listar chaves: {str(e)}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do Redis"""
        try:
            info = self.connection.info()
            return {
                "status": "healthy",
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_mb": info.get("used_memory", 0) / 1024 / 1024,
                "total_keys": self.connection.dbsize(),
                "redis_version": info.get("redis_version", "unknown"),
                "connected": True
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "connected": False
            }


# ============= SECURITY MANAGER =============

class SecurityManager:
    """Gerenciador de segurança e integridade"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self._generate_keys()
        self.unauthorized_attempts = defaultdict(int)
        self.suspicious_activities = defaultdict(list)
    
    def _generate_keys(self):
        """Gera chaves RSA para assinatura digital"""
        try:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.public_key = self.private_key.public_key()
            logger.info("SecurityManager: Chaves RSA geradas")
        except Exception as e:
            logger.error(f"SecurityManager: Erro ao gerar chaves: {str(e)}")
    
    def generate_payload_hash(self, payload: Any) -> Dict[str, str]:
        """Gera hashes de integridade do payload"""
        try:
            payload_str = json.dumps(payload, sort_keys=True, default=str)
            payload_bytes = payload_str.encode('utf-8')
            
            sha256_hash = hashlib.sha256(payload_bytes).hexdigest()
            md5_hash = hashlib.md5(payload_bytes).hexdigest()
            
            return {
                "sha256": sha256_hash,
                "md5": md5_hash,
                "payload_size": len(payload_bytes)
            }
        except Exception as e:
            logger.error(f"SecurityManager: Erro ao gerar hash: {str(e)}")
            return {"sha256": "", "md5": "", "payload_size": 0}
    
    def sign_payload(self, payload: Any) -> str:
        """Assina digitalmente o payload"""
        try:
            if not self.private_key:
                return ""
            
            payload_str = json.dumps(payload, sort_keys=True, default=str)
            payload_bytes = payload_str.encode('utf-8')
            
            signature = self.private_key.sign(
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            logger.error(f"SecurityManager: Erro ao assinar payload: {str(e)}")
            return ""
    
    def verify_signature(self, payload: Any, signature: str) -> bool:
        """Verifica assinatura digital"""
        try:
            if not self.public_key or not signature:
                return False
            
            payload_str = json.dumps(payload, sort_keys=True, default=str)
            payload_bytes = payload_str.encode('utf-8')
            signature_bytes = base64.b64decode(signature.encode('utf-8'))
            
            self.public_key.verify(
                signature_bytes,
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def detect_unauthorized_access(self, session_id: str, ip_address: str, 
                                 headers: Dict[str, str]) -> Dict[str, Any]:
        """Detecta tentativas de acesso não autorizado"""
        suspicious_indicators = []
        
        # Verificar headers suspeitos
        suspicious_headers = [
            'x-forwarded-for',
            'x-real-ip', 
            'x-originating-ip',
            'x-remote-ip'
        ]
        
        for header in suspicious_headers:
            if header in [h.lower() for h in headers.keys()]:
                suspicious_indicators.append(f"Header suspeito detectado: {header}")
        
        # Verificar User-Agent suspeito
        user_agent = headers.get('User-Agent', '').lower()
        suspicious_ua_patterns = ['bot', 'crawler', 'spider', 'curl', 'wget', 'python']
        
        for pattern in suspicious_ua_patterns:
            if pattern in user_agent:
                suspicious_indicators.append(f"User-Agent suspeito: {pattern}")
                break
        
        # Registrar tentativas
        if suspicious_indicators:
            self.unauthorized_attempts[session_id] += 1
            self.suspicious_activities[session_id].extend(suspicious_indicators)
        
        return {
            "suspicious": len(suspicious_indicators) > 0,
            "indicators": suspicious_indicators,
            "total_attempts": self.unauthorized_attempts[session_id]
        }
    
    def detect_header_bypass(self, original_headers: Dict[str, str], 
                           current_headers: Dict[str, str]) -> List[Dict[str, Any]]:
        """Detecta tentativas de bypass ou falsificação de headers"""
        bypass_attempts = []
        
        # Headers críticos que não deveriam mudar
        critical_headers = ['host', 'authorization', 'content-type']
        
        for header in critical_headers:
            orig_value = original_headers.get(header.lower(), '')
            curr_value = current_headers.get(header.lower(), '')
            
            if orig_value and orig_value != curr_value:
                bypass_attempts.append({
                    "header": header,
                    "original_value": orig_value,
                    "current_value": curr_value,
                    "timestamp": datetime.now().isoformat(),
                    "severity": "high"
                })
        
        return bypass_attempts
    
    def get_tls_info(self, hostname: str, port: int = 443) -> Dict[str, Any]:
        """Obtém informações de TLS/SSL"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    return {
                        "tls_version": version,
                        "cipher_suite": cipher[0] if cipher else "",
                        "cipher_bits": cipher[2] if cipher else 0,
                        "certificate_valid": cert is not None,
                        "certificate_subject": cert.get('subject', []) if cert else [],
                        "certificate_expires": cert.get('notAfter', '') if cert else '',
                        "transport_encrypted": True
                    }
        except Exception as e:
            logger.warning(f"SecurityManager: Erro ao obter info TLS: {str(e)}")
            return {
                "tls_version": "unknown",
                "cipher_suite": "",
                "cipher_bits": 0,
                "certificate_valid": False,
                "transport_encrypted": False,
                "error": str(e)
            }


# ============= PERFORMANCE MONITOR =============

class PerformanceMonitor:
    """Monitor de performance e telemetria"""
    
    def __init__(self):
        self.start_time = time.time()
        self.process = psutil.Process()
        self.network_baseline = self._get_network_stats()
        self.disk_baseline = self._get_disk_stats()
        self.function_timings = defaultdict(list)
    
    def _get_network_stats(self) -> Dict[str, int]:
        """Obtém estatísticas de rede"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            }
        except Exception:
            return {}
    
    def _get_disk_stats(self) -> Dict[str, int]:
        """Obtém estatísticas de disco"""
        try:
            disk_io = psutil.disk_io_counters()
            return {
                "read_bytes": disk_io.read_bytes,
                "write_bytes": disk_io.write_bytes,
                "read_count": disk_io.read_count,
                "write_count": disk_io.write_count
            }
        except Exception:
            return {}
    
    def get_current_performance(self) -> PerformanceData:
        """Obtém dados de performance atuais"""
        perf_data = PerformanceData()
        
        try:
            # CPU e Memória
            perf_data.cpu_usage_percent = self.process.cpu_percent()
            memory_info = self.process.memory_info()
            perf_data.memory_usage_mb = memory_info.rss / 1024 / 1024
            perf_data.memory_peak_mb = memory_info.peak_wset / 1024 / 1024 if hasattr(memory_info, 'peak_wset') else perf_data.memory_usage_mb
            
            # Disco
            current_disk = self._get_disk_stats()
            if current_disk and self.disk_baseline:
                perf_data.disk_read_bytes = current_disk.get("read_bytes", 0) - self.disk_baseline.get("read_bytes", 0)
                perf_data.disk_write_bytes = current_disk.get("write_bytes", 0) - self.disk_baseline.get("write_bytes", 0)
            
            # Rede
            current_network = self._get_network_stats()
            if current_network and self.network_baseline:
                perf_data.network_sent_bytes = current_network.get("bytes_sent", 0) - self.network_baseline.get("bytes_sent", 0)
                perf_data.network_received_bytes = current_network.get("bytes_recv", 0) - self.network_baseline.get("bytes_recv", 0)
                
                # Erros de rede
                errors = []
                if current_network.get("errin", 0) > self.network_baseline.get("errin", 0):
                    errors.append(f"Network input errors: {current_network.get('errin', 0) - self.network_baseline.get('errin', 0)}")
                if current_network.get("errout", 0) > self.network_baseline.get("errout", 0):
                    errors.append(f"Network output errors: {current_network.get('errout', 0) - self.network_baseline.get('errout', 0)}")
                if current_network.get("dropin", 0) > self.network_baseline.get("dropin", 0):
                    errors.append(f"Dropped input packets: {current_network.get('dropin', 0) - self.network_baseline.get('dropin', 0)}")
                
                perf_data.network_errors = errors
            
            # Timings de funções
            perf_data.function_timings = {
                func: statistics.mean(times[-10:]) if times else 0  # Média das últimas 10 execuções
                for func, times in self.function_timings.items()
            }
            
        except Exception as e:
            logger.error(f"PerformanceMonitor: Erro ao obter performance: {str(e)}")
        
        return perf_data
    
    def measure_function_time(self, func_name: str):
        """Decorator para medir tempo de execução de funções"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000  # em ms
                    self.function_timings[func_name].append(execution_time)
                    # Manter apenas as últimas 100 medições
                    if len(self.function_timings[func_name]) > 100:
                        self.function_timings[func_name] = self.function_timings[func_name][-100:]
            return wrapper
        return decorator
    
    def calculate_latency(self, start_time: float, end_time: float = None) -> float:
        """Calcula latência em milissegundos"""
        if end_time is None:
            end_time = time.time()
        return (end_time - start_time) * 1000
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtém informações do sistema"""
        try:
            return {
                "platform": platform.platform(),
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
                "memory_total_gb": psutil.virtual_memory().total / 1024 / 1024 / 1024,
                "disk_usage": {
                    partition.mountpoint: psutil.disk_usage(partition.mountpoint)._asdict()
                    for partition in psutil.disk_partitions()
                    if partition.mountpoint and os.access(partition.mountpoint, os.R_OK)
                },
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                "uptime_seconds": time.time() - psutil.boot_time()
            }
        except Exception as e:
            logger.error(f"PerformanceMonitor: Erro ao obter info do sistema: {str(e)}")
            return {}


# ============= APPLICATION MONITOR =============

class ApplicationMonitor:
    """Monitor de dados da aplicação"""
    
    def __init__(self, sdk_version: str = "1.0.0"):
        self.sdk_version = sdk_version
        self.loaded_modules = list(sys.modules.keys())
        self.runtime_config = {}
        self.feature_flags = {}
        
    def get_application_data(self) -> ApplicationData:
        """Obtém dados atuais da aplicação"""
        app_data = ApplicationData()
        app_data.sdk_version = self.sdk_version
        app_data.python_version = sys.version
        app_data.platform_info = platform.platform()
        app_data.loaded_modules = list(sys.modules.keys())
        app_data.runtime_config = self.runtime_config.copy()
        app_data.feature_flags = self.feature_flags.copy()
        
        # Detectar modo debug
        app_data.debug_mode = __debug__ or bool(os.environ.get('DEBUG'))
        app_data.production_mode = not app_data.debug_mode
        app_data.environment = os.environ.get('ENVIRONMENT', 'production')
        
        # Bibliotecas carregadas (principais)
        important_libs = []
        for module_name in sys.modules:
            if any(lib in module_name.lower() for lib in ['flask', 'django', 'fastapi', 'requests', 'psutil', 'redis', 'sqlite']):
                if hasattr(sys.modules[module_name], '__version__'):
                    important_libs.append(f"{module_name}=={sys.modules[module_name].__version__}")
                else:
                    important_libs.append(module_name)
        
        app_data.loaded_libraries = important_libs
        
        return app_data
    
    def set_runtime_config(self, key: str, value: Any):
        """Define configuração em runtime"""
        self.runtime_config[key] = value
        logger.info(f"ApplicationMonitor: Config atualizada - {key}: {value}")
    
    def set_feature_flag(self, flag_name: str, enabled: bool):
        """Define feature flag"""
        self.feature_flags[flag_name] = enabled
        logger.info(f"ApplicationMonitor: Feature flag - {flag_name}: {enabled}")
    
    def get_loaded_plugins(self) -> List[str]:
        """Obtém lista de plugins carregados"""
        plugins = []
        
        # Verificar módulos que parecem plugins
        for module_name in sys.modules:
            if any(plugin_indicator in module_name.lower() 
                   for plugin_indicator in ['plugin', 'extension', 'addon', 'middleware']):
                plugins.append(module_name)
        
        return plugins
    
    def get_loaded_extensions(self) -> List[str]:
        """Obtém lista de extensões carregadas"""
        extensions = []
        
        # Verificar extensões C compiladas
        for module_name, module in sys.modules.items():
            if module and hasattr(module, '__file__') and module.__file__:
                if module.__file__.endswith(('.so', '.dll', '.pyd')):
                    extensions.append(module_name)
        
        return extensions

    # magrao - Sistema de validação de licenças e chaves
    # def validate_license_key(self, license_key: str) -> Dict[str, Any]:
    #     """Valida chave de licença do SDK"""
    #     # Implementação futura para validação de licenças
    #     # Irá verificar:
    #     # - Validade da licença
    #     # - Recursos disponíveis
    #     # - Data de expiração
    #     # - Limites de uso
    #     return {"valid": True, "expires_at": None, "features": []}
    
    # def get_api_keys_status(self) -> Dict[str, Any]:
    #     """Obtém status das chaves de API utilizadas"""
    #     # Implementação futura para monitorar chaves de API
    #     # Irá verificar:
    #     # - Chaves ativas/inativas
    #     # - Quotas utilizadas
    #     # - Rate limits
    #     # - Permissões
    #     return {"active_keys": 0, "quota_usage": {}, "rate_limits": {}}


# ============= ANTI FRAUD MONITOR =============

class AntiFraudMonitor:
    """Monitor avançado de antifraude"""
    
    def __init__(self):
        self.known_blacklists = {
            "malicious_ips": set(),
            "suspicious_user_agents": set(),
            "blocked_fingerprints": set()
        }
        self.behavioral_baselines = defaultdict(dict)
        self.typing_patterns_cache = defaultdict(list)
    
    def generate_device_fingerprint(self, request_data: Dict[str, Any]) -> str:
        """Gera fingerprint do dispositivo"""
        try:
            fingerprint_data = {
                "user_agent": request_data.get("user_agent", ""),
                "screen_resolution": request_data.get("screen_resolution", ""),
                "timezone": request_data.get("timezone", ""),
                "language": request_data.get("language", ""),
                "plugins": sorted(request_data.get("plugins", [])),
                "platform": request_data.get("platform", ""),
                "color_depth": request_data.get("color_depth", ""),
                "pixel_ratio": request_data.get("pixel_ratio", "")
            }
            
            fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
            return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
            
        except Exception as e:
            logger.error(f"AntiFraudMonitor: Erro ao gerar fingerprint: {str(e)}")
            return "unknown"
    
    def analyze_typing_patterns(self, session_id: str, typing_data: List[Dict[str, float]]) -> Dict[str, float]:
        """Analisa padrões de digitação"""
        if not typing_data:
            return {}
        
        try:
            # Calcular métricas de digitação
            key_intervals = []
            dwell_times = []
            
            for i, keystroke in enumerate(typing_data):
                if i > 0:
                    interval = keystroke.get("timestamp", 0) - typing_data[i-1].get("timestamp", 0)
                    key_intervals.append(interval)
                
                dwell_time = keystroke.get("key_up_time", 0) - keystroke.get("key_down_time", 0)
                if dwell_time > 0:
                    dwell_times.append(dwell_time)
            
            patterns = {}
            if key_intervals:
                patterns["avg_key_interval"] = statistics.mean(key_intervals)
                patterns["std_key_interval"] = statistics.stdev(key_intervals) if len(key_intervals) > 1 else 0
                patterns["typing_rhythm"] = patterns["avg_key_interval"] / max(patterns["std_key_interval"], 0.001)
            
            if dwell_times:
                patterns["avg_dwell_time"] = statistics.mean(dwell_times)
                patterns["std_dwell_time"] = statistics.stdev(dwell_times) if len(dwell_times) > 1 else 0
            
            # Cache para comparação futura
            self.typing_patterns_cache[session_id] = patterns
            
            return patterns
            
        except Exception as e:
            logger.error(f"AntiFraudMonitor: Erro ao analisar padrões de digitação: {str(e)}")
            return {}
    
    def detect_rapid_ip_changes(self, session_id: str, current_ip: str, 
                               previous_ips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detecta mudanças rápidas de IP"""
        recent_ips = [
            ip_data for ip_data in previous_ips
            if (datetime.now() - datetime.fromisoformat(ip_data["timestamp"])).total_seconds() < 3600  # 1 hora
        ]
        
        # Contar IPs únicos na última hora
        unique_ips = set(ip_data["ip"] for ip_data in recent_ips)
        unique_ips.add(current_ip)
        
        rapid_changes = len(unique_ips) > 3  # Mais de 3 IPs diferentes em 1 hora é suspeito
        
        return {
            "rapid_ip_changes": rapid_changes,
            "unique_ips_last_hour": len(unique_ips),
            "ip_list": list(unique_ips),
            "risk_level": "high" if len(unique_ips) > 5 else "medium" if rapid_changes else "low"
        }
    
    def check_blacklists(self, ip_address: str, user_agent: str, 
                        device_fingerprint: str) -> List[str]:
        """Verifica contra blacklists conhecidas"""
        matches = []
        
        if ip_address in self.known_blacklists["malicious_ips"]:
            matches.append(f"IP {ip_address} está na blacklist de IPs maliciosos")
        
        if user_agent in self.known_blacklists["suspicious_user_agents"]:
            matches.append(f"User-Agent suspeito detectado")
        
        if device_fingerprint in self.known_blacklists["blocked_fingerprints"]:
            matches.append(f"Device fingerprint bloqueado")
        
        return matches
    
    def get_running_processes(self, limit: int = 50) -> List[str]:
        """Obtém lista de processos em execução (servidor)"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    processes.append({
                        "pid": proc_info['pid'],
                        "name": proc_info['name'],
                        "cpu_percent": proc_info['cpu_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Ordenar por uso de CPU e limitar
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            return [f"{p['name']} (PID: {p['pid']}, CPU: {p['cpu_percent']:.1f}%)" 
                   for p in processes[:limit]]
            
        except Exception as e:
            logger.error(f"AntiFraudMonitor: Erro ao obter processos: {str(e)}")
            return []
    
    def analyze_behavioral_anomalies(self, session_id: str, 
                                   current_behavior: Dict[str, Any]) -> List[str]:
        """Analisa anomalias comportamentais"""
        anomalies = []
        
        try:
            baseline = self.behavioral_baselines.get(session_id, {})
            
            if not baseline:
                # Primeira vez, estabelecer baseline
                self.behavioral_baselines[session_id] = current_behavior.copy()
                return anomalies
            
            # Verificar desvios significativos
            for metric, current_value in current_behavior.items():
                if metric in baseline and isinstance(current_value, (int, float)):
                    baseline_value = baseline[metric]
                    if baseline_value > 0:
                        deviation = abs(current_value - baseline_value) / baseline_value
                        if deviation > 0.5:  # Desvio de mais de 50%
                            anomalies.append(f"Anomalia em {metric}: desvio de {deviation:.1%}")
            
            # Atualizar baseline gradualmente
            for metric, current_value in current_behavior.items():
                if metric in baseline and isinstance(current_value, (int, float)):
                    # Média móvel exponencial
                    baseline[metric] = 0.9 * baseline[metric] + 0.1 * current_value
                else:
                    baseline[metric] = current_value
            
        except Exception as e:
            logger.error(f"AntiFraudMonitor: Erro ao analisar anomalias: {str(e)}")
        
        return anomalies
    
    def get_antifraud_data(self, session_id: str, request_data: Dict[str, Any]) -> AntiFraudData:
        """Obtém dados completos de antifraude"""
        antifraud_data = AntiFraudData()
        antifraud_data.session_id = session_id
        
        # Device fingerprint
        antifraud_data.device_fingerprint = self.generate_device_fingerprint(request_data)
        antifraud_data.screen_resolution = request_data.get("screen_resolution", "")
        
        # Browser fingerprint (mais detalhado)
        browser_data = {
            "user_agent": request_data.get("user_agent", ""),
            "language": request_data.get("language", ""),
            "timezone": request_data.get("timezone", ""),
            "plugins": request_data.get("plugins", []),
            "fonts": request_data.get("fonts", [])
        }
        antifraud_data.browser_fingerprint = hashlib.sha256(
            json.dumps(browser_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Padrões de digitação
        typing_data = request_data.get("typing_events", [])
        if typing_data:
            antifraud_data.typing_patterns = self.analyze_typing_patterns(session_id, typing_data)
        
        # Processos em execução
        antifraud_data.running_processes_server = self.get_running_processes()
        antifraud_data.running_processes_client = request_data.get("client_processes", [])
        
        # Mudanças de IP
        previous_ips = request_data.get("previous_ips", [])
        current_ip = request_data.get("ip_address", "")
        if previous_ips:
            ip_analysis = self.detect_rapid_ip_changes(session_id, current_ip, previous_ips)
            antifraud_data.rapid_ip_changes = ip_analysis["unique_ips_last_hour"]
            antifraud_data.ip_changes = previous_ips
        
        # Verificar blacklists
        antifraud_data.blacklist_matches = self.check_blacklists(
            current_ip,
            request_data.get("user_agent", ""),
            antifraud_data.device_fingerprint
        )
        
        # Anomalias comportamentais
        behavioral_data = request_data.get("behavior_metrics", {})
        antifraud_data.behavioral_anomalies = self.analyze_behavioral_anomalies(session_id, behavioral_data)
        
        return antifraud_data

    # lucas - Sistema avançado de cálculo de score de risco
    # def calculate_risk_score(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
    #     """Calcula score de risco usando machine learning e regras avançadas"""
    #     # Implementação futura com algoritmos de ML
    #     # Irá considerar:
    #     # - Histórico do usuário
    #     # - Padrões comportamentais
    #     # - Dados de geolocalização
    #     # - Velocidade de digitação
    #     # - Consistência de dispositivo
    #     # - Horários atípicos de acesso
    #     # - Correlação com fraudes conhecidas
    #     base_score = 50  # Score inicial neutro
    #     risk_factors = []
    #     return {"score": base_score, "level": "medium", "factors": risk_factors}
    
    # def update_ml_model(self, training_data: List[Dict[str, Any]]) -> bool:
    #     """Atualiza modelo de machine learning com novos dados"""
    #     # Implementação futura para retreinamento do modelo
    #     # Irá processar:
    #     # - Novos casos de fraude confirmada
    #     # - Falsos positivos
    #     # - Padrões emergentes
    #     # - Feedback do sistema
    #     return True


# ============= STORAGE ADAPTER PRINCIPAL =============

class StorageAdapter:
    """Adapter principal para persistência e coleta de dados"""
    
    def __init__(self, storage_type: StorageType = StorageType.MEMORY, **storage_kwargs):
        self.storage_type = storage_type
        self.storage = self._create_storage(**storage_kwargs)
        self.security_manager = SecurityManager()
        self.performance_monitor = PerformanceMonitor()
        self.application_monitor = ApplicationMonitor()
        self.antifraud_monitor = AntiFraudMonitor()
        
        self.session_data_cache = defaultdict(dict)
        self._lock = threading.Lock()
        
        # Conectar ao armazenamento
        if not self.storage.connect():
            logger.error("StorageAdapter: Falha ao conectar com o armazenamento")
            raise Exception("Não foi possível conectar ao armazenamento")
    
    def _create_storage(self, **kwargs) -> StorageInterface:
        """Factory para criar instância de armazenamento"""
        if self.storage_type == StorageType.MEMORY:
            return MemoryStorage()
        elif self.storage_type == StorageType.SQLITE:
            db_path = kwargs.get('db_path', 'storage_adapter.db')
            return SQLiteStorage(db_path)
        elif self.storage_type == StorageType.REDIS:
            return RedisStorage(
                host=kwargs.get('host', 'localhost'),
                port=kwargs.get('port', 6379),
                db=kwargs.get('db', 0),
                password=kwargs.get('password', None)
            )
        else:
            logger.warning(f"Tipo de storage {self.storage_type} não implementado, usando Memory")
            return MemoryStorage()
    
    # ============= COLETA DE DADOS =============
    
    def collect_security_data(self, session_id: str, payload: Any, 
                            headers: Dict[str, str], ip_address: str) -> str:
        """Coleta dados de segurança"""
        security_data = SecurityData()
        security_data.session_id = session_id
        
        # Gerar hashes de integridade
        hashes = self.security_manager.generate_payload_hash(payload)
        security_data.payload_hash_sha256 = hashes["sha256"]
        security_data.payload_hash_md5 = hashes["md5"]
        
        # Assinatura digital
        security_data.digital_signature = self.security_manager.sign_payload(payload)
        security_data.signature_valid = self.security_manager.verify_signature(payload, security_data.digital_signature)
        
        # Detectar tentativas não autorizadas
        unauthorized_check = self.security_manager.detect_unauthorized_access(session_id, ip_address, headers)
        security_data.unauthorized_attempts = unauthorized_check["total_attempts"]
        
        # Verificar bypass de headers
        cached_headers = self.session_data_cache[session_id].get("original_headers", {})
        if cached_headers:
            security_data.header_bypass_attempts = self.security_manager.detect_header_bypass(cached_headers, headers)
        else:
            self.session_data_cache[session_id]["original_headers"] = headers.copy()
        
        # Plugins e extensões
        security_data.loaded_plugins = self.application_monitor.get_loaded_plugins()
        security_data.loaded_extensions = self.application_monitor.get_loaded_extensions()
        
        # Informações TLS
        if "host" in headers:
            tls_info = self.security_manager.get_tls_info(headers["host"])
            security_data.tls_version = tls_info["tls_version"]
            security_data.cipher_suite = tls_info["cipher_suite"]
            security_data.certificate_valid = tls_info["certificate_valid"]
            security_data.transport_encrypted = tls_info["transport_encrypted"]

        # magrao - Sistema de detecção de alterações suspeitas em parâmetros da API
        # suspicious_params = self._detect_suspicious_parameter_changes(session_id, payload)
        # security_data.suspicious_parameter_changes = suspicious_params
        # Esta funcionalidade irá:
        # - Monitorar mudanças inesperadas em parâmetros
        # - Detectar tentativas de injeção
        # - Identificar manipulação de dados
        # - Alertar sobre parâmetros malformados
        # - Verificar encoding suspeito
        
        # Armazenar dados
        key = f"security:{session_id}:{int(time.time())}"
        self.storage.store_data(key, security_data.to_dict(), ttl=3600)
        
        logger.info(f"StorageAdapter: Dados de segurança coletados para sessão {session_id}")
        return key
    
    def collect_performance_data(self, session_id: str, request_id: str = "",
                               execution_time: float = 0.0) -> str:
        """Coleta dados de performance"""
        perf_data = self.performance_monitor.get_current_performance()
        perf_data.session_id = session_id
        perf_data.request_id = request_id or str(uuid.uuid4())
        
        if execution_time > 0:
            perf_data.execution_time_ms = execution_time
        
        # Métricas customizadas (exemplo)
        perf_data.custom_metrics = {
            "garbage_collections": len(gc.get_stats()) if hasattr(gc, 'get_stats') else 0,
            "thread_count": threading.active_count(),
            "process_id": os.getpid()
        }
        
        # Calcular latências
        if session_id in self.session_data_cache:
            session_start = self.session_data_cache[session_id].get("start_time", time.time())
            perf_data.latency_avg_ms = self.performance_monitor.calculate_latency(session_start)
        
        # Armazenar dados
        key = f"performance:{session_id}:{perf_data.request_id}"
        self.storage.store_data(key, perf_data.to_dict(), ttl=3600)
        
        logger.debug(f"StorageAdapter: Dados de performance coletados para sessão {session_id}")
        return key
    
    def collect_transaction_data(self, transaction_data: TransactionData) -> str:
        """Coleta dados de transação"""
        # Armazenar dados
        key = f"transaction:{transaction_data.transaction_id}"
        self.storage.store_data(key, transaction_data.to_dict(), ttl=86400)  # 24h
        
        # Cache para correlações
        self.session_data_cache[transaction_data.session_id]["transactions"] = \
            self.session_data_cache[transaction_data.session_id].get("transactions", []) + [transaction_data.transaction_id]
        
        logger.info(f"StorageAdapter: Dados de transação coletados: {transaction_data.transaction_id}")
        return key
    
    def collect_antifraud_data(self, session_id: str, request_data: Dict[str, Any]) -> str:
        """Coleta dados de antifraude"""
        antifraud_data = self.antifraud_monitor.get_antifraud_data(session_id, request_data)
        
        # Armazenar dados
        key = f"antifraud:{session_id}:{int(time.time())}"
        self.storage.store_data(key, antifraud_data.to_dict(), ttl=86400)  # 24h
        
        logger.info(f"StorageAdapter: Dados de antifraude coletados para sessão {session_id}")
        return key
    
    # ============= RECUPERAÇÃO DE DADOS =============
    
    def get_session_security_data(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera dados de segurança da sessão"""
        keys = self.storage.list_keys(f"security:{session_id}:*")
        keys.sort(reverse=True)  # Mais recentes primeiro
        
        security_data = []
        for key in keys[:limit]:
            data = self.storage.retrieve_data(key)
            if data:
                security_data.append(data)
        
        return security_data
    
    def get_session_performance_data(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera dados de performance da sessão"""
        keys = self.storage.list_keys(f"performance:{session_id}:*")
        keys.sort(reverse=True)
        
        performance_data = []
        for key in keys[:limit]:
            data = self.storage.retrieve_data(key)
            if data:
                performance_data.append(data)
        
        return performance_data
    
    def get_transaction_data(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Recupera dados de uma transação específica"""
        key = f"transaction:{transaction_id}"
        return self.storage.retrieve_data(key)
    
    def get_session_transactions(self, session_id: str) -> List[Dict[str, Any]
      def get_session_transactions(self, session_id: str) -> List[Dict[str, Any]]:
        """Recupera todas as transações associadas a uma sessão"""
        transaction_ids = self.session_data_cache[session_id].get("transactions", [])
        transactions = []
        for tx_id in transaction_ids:
            data = self.get_transaction_data(tx_id)
            if data:
                transactions.append(data)
        return transactions

    def get_session_antifraud_data(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recupera dados de antifraude da sessão"""
        keys = self.storage.list_keys(f"antifraud:{session_id}:*")
        keys.sort(reverse=True)  # Mais recentes primeiro

        antifraud_data = []
        for key in keys[:limit]:
            data = self.storage.retrieve_data(key)
            if data:
                antifraud_data.append(data)
        
        return antifraud_data

    def get_session_data_summary(self, session_id: str) -> Dict[str, Any]:
        """Retorna um resumo completo de todos os dados coletados para uma sessão"""
        return {
            "security_data": self.get_session_security_data(session_id),
            "performance_data": self.get_session_performance_data(session_id),
            "antifraud_data": self.get_session_antifraud_data(session_id),
            "transactions": self.get_session_transactions(session_id)
        }
