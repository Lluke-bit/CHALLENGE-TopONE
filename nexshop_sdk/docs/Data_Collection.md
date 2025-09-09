# 📥 Data-Collection

## 🔎 O que vamos coletar

### 1. Identificação do Dispositivo e Ambiente
- Tipo de dispositivo (servidor físico, VM, container, desktop, mobile, IoT)
- Modelo e fabricante (via API do SO)
- Sistema Operacional e versão
- Quantidade de memória RAM total e disponível
- CPU (modelo, núcleos, threads, uso em %)
- Disco (tamanho, espaço livre, uso em %)
- GPU (quando disponível)
- Nome do host
- Endereço IP (IPv4/IPv6)
- Endereço MAC (quando permitido)
- Idioma, localização e timezone do sistema
- Provedor de internet (ASN, ISP)
- Tipo e status da rede (Ethernet, Wi-Fi, LTE, 5G, online/offline, latência/jitter)
- Uptime do dispositivo
- Versão do SDK instalado
- Sensores (mobile/IoT: acelerômetro, giroscópio, GPS, etc.)
- Navegador e versão (quando aplicável)

---

### 2. Sessão, Acesso e Autenticação
- ID único da sessão
- Token de autenticação (JWT, OAuth, API Key) – sempre mascarado/hasheado
- Timestamp de início e término da sessão
- Origem da requisição (URL, rota, referer)
- User Agent completo
- Geolocalização aproximada (via IP ou GPS)
- Métodos de login usados (senha, MFA, SSO)
- Resultado da autenticação (sucesso, falha, motivo)
- Tentativas de login consecutivas
- Mudança de credenciais (reset de senha, troca de e-mail, etc.)
- Sessões simultâneas abertas pelo mesmo usuário
- Expiração do token/sessão
- Fingerprint do dispositivo (hash único)

---

### 3. Dados de Uso e Comportamento
- Endpoints/rotas acessados
- Sequência de navegação e tempo gasto por rota
- Eventos de interação (cliques, formulários, ações críticas)
- Frequência e horário de acessos
- Erros de requisição (HTTP 4xx, 5xx)
- Padrões anômalos de uso (repetição de requests, acessos fora do horário)
- Número de requisições por minuto
- Taxa de falhas em chamadas de API
- Histórico de permissões acessadas
- Download/upload de arquivos (nome, tamanho, tipo, hash do arquivo)
- Logs de execução de comandos em servidores (quando aplicável)
- Erros de sistema (exceções não tratadas, crash reports)

---

### 4. Segurança e Compliance
- Tentativas de acesso maliciosas (SQLi, XSS, brute force, etc.)
- Registros de bloqueios de firewall/WAF
- Estado de integridade do dispositivo (root/jailbreak detectado)
- Certificados digitais instalados/validade
- Uso de VPN ou proxy
- Comparação contra listas de reputação (IP/ASN maliciosos)
- Estado de criptografia dos discos (BitLocker, LUKS, etc.)
- Logs de auditoria para LGPD/GDPR
- Consentimento de coleta de dados (opt-in/out)

---

### 5. Métricas de Performance e Telemetria
- Latência média das chamadas
- Tempo de resposta por endpoint
- Taxa de erro por serviço
- Disponibilidade do sistema (% uptime)
- Consumo de memória e CPU da aplicação
- Métricas de fila (jobs pendentes, tempo de execução)
- Monitoramento de containers (CPU, memória, IO, reinícios)
- Eventos de escalonamento automático (scale in/out)
- Tempo de inicialização do SDK
- Eventos offline/online do cliente
- Logs de falhas na sincronização

---

### 6. Integrações Externas e Serviços
- Chamadas para APIs de terceiros (endpoint, tempo de resposta, status)
- Status de integrações (ativo, falho, indisponível)
- Logs de auditoria de integrações
- Dependências externas do SDK
- Webhooks disparados (payload, resposta)
- Comunicação com mensageria (Kafka, RabbitMQ, SQS, etc.)
- Configurações recebidas remotamente (feature flags, parâmetros)

---

### 7. Dados de Negócio (Customizáveis)
*(Definidos pela aplicação que usa o SDK – exemplos abaixo)*
- Identificador único do cliente
- Plano/assinatura do usuário
- Funções/papéis no sistema (roles)
- Preferências do usuário
- Histórico de compras/transações
- Pontos de engajamento (gamificação, níveis, badges)
- Contexto de uso (mobile app, portal web, API backend)

## Documentação Técnica
### 2. Device Info

#### 🎯 Finalidade
Coletar informações completas sobre o dispositivo e ambiente de execução para criação de impressão digital digital (*fingerprint*) e análise de contexto de segurança.

#### 📦 Dependências
- `requests` - Para requisições HTTP à API de geolocalização
- `psutil` - Para informações de sistema e hardware
- `netifaces` - Para dados de interfaces de rede
- `uuid` - Para gerar identificadores únicos
- `platform` - Para informações da plataforma
- `socket` - Para operações de rede
- `locale` - Para informações de localização
- `datetime` - Para manipulação de datas e horas
- `re` - Para expressões regulares
- `subprocess` - Para execução de comandos do sistema
- `json` - Para manipulação de JSON

#### 🧩 Principais Componentes

**Classe Principal:** `DeviceEnvironmentSDK`

**Métodos Principais:**
- `detect_device_type()` - Identifica tipo de dispositivo
- `get_memory_info()` - Obtém informações de memória
- `get_host_info()` - Coleta dados do sistema
- `get_network_info()` - Obtém dados de rede
- `collect_all_data()` - Coleta todos os dados

#### 🔧 Funcionamento

O arquivo implementa uma classe única (`DeviceEnvironmentSDK`) que:

1. **Inicializa** uma sessão HTTP e cache de dados
2. **Detecta** automaticamente o tipo de dispositivo através de múltiplas técnicas
3. **Coleta** informações de hardware, sistema, rede e localização
4. **Exporta** dados em formatos JSON ou CSV
5. **Gerencia** erros gracefulmente com fallbacks

#### 📊 Exemplo de Uso

```python
# Importação e inicialização
from device_info import DeviceEnvironmentSDK

sdk = DeviceEnvironmentSDK()

# Coleta completa de dados
dados_dispositivo = sdk.collect_all_data()
print(f"Tipo de dispositivo: {dados_dispositivo['device_type']}")
print(f"Memória total: {dados_dispositivo['memory_info']['total_memory_gb']}GB")

# Exportação para JSON
json_data = sdk.export_data('json')
print(json_data)
```

#### ⚠️ Observações

- **Segurança:** Endereços MAC e tokens são mascarados
- **Performance:** Operações de rede possuem timeout de 10 segundos
- **Portabilidade:** Funciona em Windows, Linux e macOS
- **Erros:** Todos os métodos incluem tratamento de exceções

### 3. IP Location

#### 🎯 Finalidade
Fornecer uma SDK completa para coleta de dados de geolocalização por IP, gerenciamento de sessões e análise de segurança. O arquivo implementa um sistema modular com múltiplos provedores de geolocalização e funcionalidades avançadas de tracking.

#### 📦 Dependências
- `requests` - Para fazer requisições HTTP aos provedores de geolocalização
- `logging` - Para registro de logs e debug
- `datetime` - Para manipulação de datas e timestamps
- `hashlib` - Para geração de hashes de sessão
- `enum` - Para definição de enums (métodos de auth, resultados)
- `time` - Para operações de tempo e delays
- `abc` - Para definir a interface abstrata dos provedores

#### 🧩 Principais Componentes

**Classes Principais:**
- `IPLocationSDK` - Classe principal do SDK
- `GeoLocationProviderInterface` - Interface abstrata para provedores
- `GeoLocationData` - Modelo de dados para localização
- `SessionData` - Gerenciamento de sessões
- `AuthenticationData` - Dados de autenticação

**Provedores Implementados:**
- `IPInfoProvider` - Provedor IPInfo.io
- `IPAPIProvider` - Provedor IP-API.com  
- `MockGeoProvider` - Provedor mock para testes

**Enums:**
- `AuthMethod` - Métodos de autenticação (PASSWORD, MFA, SSO, etc.)
- `AuthResult` - Resultados de autenticação (SUCCESS, FAILED, etc.)

#### 🔧 Funcionamento

O SDK funciona através de um sistema de provedores múltiplos:

1. **Inicialização**: Cria instância com provedores padrão
2. **Geolocalização**: Tenta provedores em ordem até obter sucesso
3. **Sessões**: Gerencia ciclo de vida das sessões de usuário
4. **Autenticação**: Registra e analisa tentativas de login
5. **Análise de Risco**: Combina dados para calcular risco de segurança
6. **Relatórios**: Gera reports completos com todos os dados

#### 📊 Exemplo de Uso

```python
# Importar e inicializar SDK
from iplocation import IPLocationSDK, AuthMethod, AuthResult

sdk = IPLocationSDK()

# Obter localização de IP
location = sdk.get_ip_location("8.8.8.8")
print(f"País: {location.country}, Cidade: {location.city}")

# Gerenciar sessão
session = sdk.create_session("sessao_123")
sdk.update_session_activity("sessao_123")

# Registrar autenticação
auth_data = AuthenticationData()
auth_data.username = "usuario_teste"
auth_data.auth_method = AuthMethod.PASSWORD
auth_data.auth_result = AuthResult.SUCCESS
sdk.record_auth_attempt(auth_data)

# Gerar relatório completo
report = sdk.generate_comprehensive_report("8.8.8.8", "sessao_123")
print(f"Nível de risco: {report['security_analysis']['risk_level']}")
```

#### ⚠️ Observações

- **Fallback Automático**: Se um provedor falhar, tenta o próximo automaticamente
- **Thread-Safe**: Adequado para uso em ambientes multi-thread
- **Extensível**: Fácil adicionar novos provedores via interface
- **Logs Detalhados**: Logging completo para debug e auditoria
- **Mock Included**: Provedor mock para desenvolvimento e testes
- **Tratamento de Erros**: Robustecido contra falhas de rede e provedores

#### 🔄 Fluxo de Dados

```
IP Address → Provedores de Geo → Location Data → Session Tracking → 
Auth Tracking → Risk Analysis → Comprehensive Report
```

O arquivo é totalmente auto-contido e pode ser usado independentemente ou integrado com outros módulos do sistema de segurança.

### 4. Session Behavior

#### 🎯 Finalidade
Monitorar e analisar o comportamento de usuários em tempo real, rastreando eventos de interação, requisições HTTP e padrões de uso para detecção de anomalias e melhoria da experiência do usuário.

#### 📦 Dependências
- `dataclasses` - Para definição de estruturas de dados
- `threading` - Para operações thread-safe
- `statistics` - Para cálculos estatísticos
- `collections` - Para estruturas de dados otimizadas (defaultdict, deque)
- `uuid` - Para geração de IDs únicos
- `logging` - Para registro de logs
- `json` - Para serialização de dados
- `time` - Para medição de tempo
- `datetime` - Para manipulação de datas e horas
- `enum` - Para definição de enums
- `functools` - Para decorators

#### 🧩 Principais Componentes

**Classes Principais:**
- `SessionBehaviorSDK` - Classe principal do SDK
- `UserBehaviorAnalyzer` - Analisador de comportamento do usuário
- `EndpointMonitor` - Monitor de endpoints e performance
- `RealTimeEventProcessor` - Processador de eventos em tempo real

**Estruturas de Dados:**
- `UserEvent` - Modelo para eventos de usuário (cliques, scroll, etc.)
- `RequestEvent` - Modelo para eventos de requisição HTTP
- `EndpointMetrics` - Métricas de performance de endpoints

**Enums:**
- `EventType` - Tipos de eventos (CLICK, SCROLL, FORM_SUBMIT, etc.)
- `HTTPMethod` - Métodos HTTP (GET, POST, PUT, etc.)
- `RequestStatus` - Status das requisições (SUCCESS, ERROR, TIMEOUT)

#### 🔧 Funcionamento

O SDK opera em três camadas principais:

1. **Coleta de Dados**: 
   - Rastreia eventos de UI via métodos `track_click()`, `track_scroll()`, etc.
   - Monitora requisições HTTP via `track_request()`
   - Usa decorator `@request_timing_decorator` para timing automático

2. **Análise em Tempo Real**:
   - Calcula métricas de performance (RPM, tempo de resposta)
   - Identifica padrões de comportamento (hotspots de clique, tempo ocioso)
   - Detecta anomalias e gera alertas

3. **Relatórios e Insights**:
   - Gera análises de sessão detalhadas
   - Produz relatórios de performance de endpoints
   - Fornece métricas em tempo real

#### 📊 Exemplo de Uso

```python
from session_behavior import SessionBehaviorSDK, EventType, HTTPMethod

# Inicializar SDK
sdk = SessionBehaviorSDK()

# Registrar handlers de eventos
def click_handler(event):
    print(f"Clique detectado em: {event.element_id}")
    
sdk.register_event_handler(EventType.CLICK, click_handler)

# Rastrear eventos de usuário
session_id = "user_123"
sdk.track_click(session_id, "btn-submit", {"x": 100, "y": 200}, "/checkout")
sdk.track_scroll(session_id, {"x": 0, "y": 500}, "/product")

# Rastrear requisições HTTP
sdk.track_request(
    session_id=session_id,
    endpoint="/api/order",
    method=HTTPMethod.POST,
    status_code=201,
    response_time_ms=150.2
)

# Usar decorator para timing automático
@sdk.request_timing_decorator("/api/data", HTTPMethod.GET)
def get_data():
    return {"data": "example"}

# Gerar relatórios
analysis = sdk.get_session_behavior_analysis(session_id)
performance = sdk.get_endpoint_performance_report()
```

#### ⚠️ Observações

- **Thread-Safe**: Todas as operações são protegidas contra acesso concorrente
- **Baixo Overhead**: Otimizado para alto desempenho em produção
- **Extensível**: Fácil adicionar novos tipos de eventos e analisadores
- **Alertas em Tempo Real**: Detecta automaticamente comportamentos suspeitos
- **Múltiplas Sessões**: Suporte a tracking concorrente de várias sessões
- **Limpeza Automática**: Remove dados antigos automaticamente

#### 🔄 Fluxo de Dados

```
Eventos de UI → UserBehaviorAnalyzer → Análise de Padrões
Requisições HTTP → EndpointMonitor → Métricas de Performance
           ↘
        SessionBehaviorSDK → Relatórios Consolidados → Alertas
```

#### 🎨 Funcionalidades Avançadas

1. **Hotspot Detection**: Identifica áreas mais clicadas na interface
2. **Idle Time Analysis**: Calcula tempos de inatividade do usuário
3. **Rate Limiting**: Monitora taxa de requisições por sessão
4. **Custom Events**: Suporte a eventos personalizados
5. **Real-time Alerts**: Gera alertas para comportamentos anômalos
6. **Performance Decorator**: Decorator automático para timing de funções

### 5. Storage Adapter

#### 🎯 Finalidade
Fornecer uma camada de abstração unificada para operações de armazenamento, permitindo trocar entre diferentes provedores (SQLite, Redis, PostgreSQL, MongoDB, Memória) sem alterar o código da aplicação. Gerencia automaticamente serialização, segurança, caching e fallbacks com foco em compliance e performance.

#### 📦 Dependências
- `redis` - Para conexão com Redis
- `psycopg2-binary` - Para PostgreSQL (opcional)
- `pymongo` - Para MongoDB (opcional)
- `cryptography` - Para criptografia e assinaturas digitais
- `psutil` - Para monitoramento de recursos do sistema
- `dataclasses` - Para estruturas de dados tipadas
- `logging` - Para registro de logs estruturados
- `threading` - Para operações thread-safe

#### 🧩 Principais Componentes

##### 📊 Estruturas de Dados (Data Classes)
- `SecurityData` - Dados de segurança, integridade e auditoria
- `PerformanceData` - Telemetria, métricas e monitoramento
- `ApplicationData` - Configuração e ambiente da aplicação  
- `TransactionData` - Transações financeiras e negócio
- `AntiFraudData` - Detecção e prevenção de fraudes

##### 💾 Interfaces de Armazenamento
- `StorageInterface` - Interface abstrata com todos os métodos obrigatórios
- `MemoryStorage` - Armazenamento volátil em memória (dev/test)
- `SQLiteStorage` - Banco embutido com suporte a SQL
- `RedisStorage` - Cache distribuído de alta performance
- `PostgreSQLStorage` - Banco relacional transacional
- `MongoDBStorage` - Banco NoSQL orientado a documentos

##### 🎯 Enums e Tipos
- `StorageType` - Tipos de armazenamento suportados
- `TransactionStatus` - Status do ciclo de vida de transações
- `PaymentMethod` - Métodos de pagamento suportados
- `SecurityLevel` - Níveis críticos de segurança

#### 🔧 Funcionamento

##### Arquitetura em Camadas
O adapter implementa um padrão **Strategy** + **Factory**:

```
Aplicação → StorageAdapter → [Memory, SQLite, Redis, PostgreSQL, MongoDB]
```

##### Fluxo de Operação
1. **Inicialização**: Configuração do provedor via factory method
2. **Conexão**: Estabelecimento de conexão com validação
3. **Operação**: CRUD com serialização/criptografia automática
4. **Monitoramento**: Coleta de métricas de performance
5. **Fallback**: Troca automática em caso de falhas

#### 📊 Exemplo de Uso

```python
from storage_adapter import StorageAdapter, StorageType, SecurityData

# Inicialização com Redis
storage = StorageAdapter.create(StorageType.REDIS, {
    'host': 'localhost',
    'port': 6379,
    'password': 'secret'
})

# Conexão automática
storage.connect()

# Armazenar dados de segurança
security_data = SecurityData(
    session_id="sess_123",
    payload_hash_sha256="abc123...",
    unauthorized_attempts=3
)

storage.store_data(
    key="security:sess_123",
    data=security_data.to_dict(),
    ttl=3600  # 1 hora
)

# Recuperar dados
data = storage.retrieve_data("security:sess_123")
print(f"Tentativas não autorizadas: {data['unauthorized_attempts']}")

# Health check
status = storage.health_check()
print(f"Status: {status['status']}, Latência: {status['latency_ms']}ms")
```

#### ⚠️ Observações

##### 🔒 Segurança
- **Criptografia**: Dados sensíveis criptografados em repouso
- **Mascaramento**: Logs com dados sensíveis mascarados
- **Validação**: Assinaturas digitais para integridade
- **TTL**: Expiração automática de dados temporários

##### ⚡ Performance  
- **Connection Pooling**: Reuso de conexões para baixa latência
- **Batch Operations**: Operações em lote para grandes volumes
- **Compression**: Compactação automática de grandes dados
- **Caching**: Camada de cache integrada para consultas frequentes

##### 🔄 Resiliencia
- **Retry Automático**: Tentativas em caso de falhas transitórias
- **Fallback**: Alternância entre provedores secundários
- **Circuit Breaker**: Prevenção de cascata de falhas
- **Timeout**: Operações com timeout configurável

##### 📋 Compliance
- **Auditoria**: Logs detalhados de todas as operações
- **RGPD/LGPD**: Suporte a direito ao esquecimento
- **Retenção**: Políticas de retenção configuráveis
- **Backup**: Integração com sistemas de backup

#### 🚀 Implementações Específicas

##### Redis Storage
```python
# Configuração otimizada para Redis
redis_config = {
    'host': 'redis-cluster.example.com',
    'port': 6379,
    'password': 'secret',
    'ssl': True,
    'ssl_cert_reqs': 'required',
    'retry_on_timeout': True,
    'max_connections': 100
}
```

##### PostgreSQL Storage  
```python
# Configuração para PostgreSQL com pooling
postgres_config = {
    'host': 'postgres-primary.example.com',
    'port': 5432,
    'database': 'app_db',
    'user': 'app_user',
    'password': 'secret',
    'sslmode': 'verify-full',
    'pool_size': 20
}
```

#### 🔍 Métricas Coletadas

##### Performance Metrics
- `operation_latency_ms` - Tempo das operações
- `connection_pool_size` - Tamanho do pool de conexões
- `cache_hit_rate` - Taxa de acerto do cache
- `error_rate` - Taxa de erros por operação

##### Security Metrics
- `encryption_time_ms` - Tempo de criptografia
- `integrity_checks` - Verificações de integridade
- `access_violations` - Tentativas de acesso não autorizado

##### Business Metrics
- `storage_cost_per_gb` - Custo de armazenamento
- `data_retention_days` - Dias de retenção
- `backup_frequency` - Frequência de backups
