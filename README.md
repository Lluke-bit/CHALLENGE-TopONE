# EyeOfToga - Doc
## Ideia Principal
 > É um software que fará a analise de comportamento do usuário.  Valide a identidade de usuários no momento do login, checkout ou ações sensiveis, com o minimo de fricção. Coletar dados úteis. Gerar score de confiança permitido que o hospedeiro possa agir com base na avaliação.

### Validação de Identidade

> Cuida da autenticação e do gerenciamento de sessões. A autenticação pode ser feita internamente, com as credenciais armazenadas localmente, ou externamente, por meio do componente de federação.
 - Podendo suportar até:
    - ID exclusivo(UID) e senha;
    - Senha de uso unico(OTP)(e-mail, SMS ou Voz);
    - Senha de uso unico baseada em tempo(TOTP);
    - Codigo QR(Requer modulo de identidade Movel);
    - Notificação Push(Requer o modulo mobile identity);
    - Logout Unico SAML(SLO);
    - Revogação de token.

### Analise de comportamento
> Responsavel por analisar o comportamento dos usuarios e capturar dados como:
    - Device fingerprint (navegador, IP, timezone, resolução, idioma, etc.)
    - Comportamento do usuário (tempo na página, movimentos do mouse, interações, foco da aba, etc.)
    - Metadados da sessão
> Transformar a analise da I.A. em 3 respostas:
    - Allow 
    - Review
    - Deny
> Caso seja um "Deny" - auto:
    - Definir a criticidade da ameaça
        # Critical
        # High
        # Medium
        # Low

# OUTPUT - Doc
##

# Data_Collection - Doc
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

# Biometrics - DOC
## 🔄 Fluxo Principal do Processamento Biométrico

### Diagrama de Fluxo Simplificado

```
Captura de Imagem → Pré-processamento → Validação de Qualidade → 
Seleção do Provedor → Comparação Facial → Análise de Resultados → 
Armazenamento e Logging → Retorno da Resposta
```

## 🏢 Provedores de Biometria Suportados

### Tabela Comparativa de Provedores

| Provedor              | Tipo       | Precisão     | Latência   | Custo    | Melhor Para         |
|-----------------------|------------|--------------|------------|----------|---------------------|
| **AWS Rekognition**   | Cloud      | 99.9%        | 200-500ms  | Por uso  | Produção enterprise |
| **Local Recognition** | On-premise | 95-98%       | 500-2000ms | Hardware | Ambientes offline   |
| **Mock Provider**     | Simulação  | Configurável | 0-100ms    | Zero     | Desenvolvimento     |

### Critérios de Seleção Automática

| Condição                            | Provedor Escolhido | Motivo                  |
|-------------------------------------|--------------------|-------------------------|
| Internet disponível + Alta precisão | AWS Rekognition    | Máxima acurácia         |
| Internet indisponível               | Local Recognition  | Funcionamento offline   |
| Modo desenvolvimento                | Mock Provider      | Resultados controlados  |
| Baixa latência requerida            | AWS Rekognition    | Performance superior    |
| Alta privacidade requerida          | Local Recognition  | Dados não saem do local |

## 🎯 Processo de Validação Biométrica

### Etapas de Validação Técnica

| Etapa                   | Descrição                     | Critérios de Aceitação            |
|-------------------------|-------------------------------|-----------------------------------|
| **Validação de Imagem** | Verifica formato e qualidade  | Formato JPG/PNG, tamanho 50KB-5MB |
| **Detecção Facial**     | Identifica rostos na imagem   | Exatamente 1 rosto detectado      |
| **Qualidade da Imagem** | Analisa condições técnicas    | Brilho 40-220, nitidez >500       | 
| **Pré-processamento**   | Prepara imagem para análise   | Alinhamento, normalização         |
| **Comparação Facial**   | Executa algoritmo de matching | Score > threshold configurado     |

### Thresholds de Segurança por Cenário

| Nível de Segurança | Similaridade Mínima | Confiança Mínima | Aplicação Típica       |
|--------------------|---------------------|------------------|------------------------|
| **Crítico**        | 90%                 | 95%              | Transações financeiras |
| **Alto**           | 85%                 | 90%              | Acesso administrativo  |
| **Médio**          | 75%                 | 80%              | Login de usuário       |
| **Baixo**          | 65%                 | 70%              | Recuperação de conta   |

## 📊 Destino dos Dados Coletados

### Estrutura de Armazenamento

| Tipo de Dado               | Destino Principal  | Destino Secundário | Período de Retenção      |
|----------------------------|--------------------|--------------------|--------------------------|
| **Imagens brutas**         | Azure Blob Storage | -                  | 7 dias (criptografadas)  |
| **Resultados verificação** | AWS S3             | Redis Cache        | 365 dias                 |
| **Logs de auditoria**      | Elasticsearch      | -                  | 2 anos                   |
| **Métricas performance**   | Snowflake          | Kafka Stream       | Indefinido (anonimizado) |
| **Eventos tempo real**     | Kafka              | Webhooks           | 30 dias                  |

### Exemplo de Payload para Data Collection

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "session_id": "sess_abc123",
  "provider": "aws_rekognition",
  "result": {
    "similarity_score": 0.92,
    "is_match": true,
    "confidence": 0.98
  },
  "image_metrics": {
    "quality_score": 0.88,
    "face_count": 1
  }
}
```

## ⚙️ Configurações de Performance

### Estratégias de Otimização

| Otimização                | AWS Rekognition | Local Recognition | Mock Provider |
|---------------------------|---------------  |-------------------|---------------|
| **Processamento em lote** | ✅ Suportado    | ❌ Não suportado | ✅ Simulado  |
| **Cache de resultados**   | 1 hora          | 24 horas          | 5 minutos     |
| **Conexões paralelas**    | 10 conexões     | 4 threads         | Ilimitado     |
| **Compressão**            | ✅ Ativado      | ❌ Desativado    | ✅ N/A       |

## 🔒 Políticas de Segurança

### Medidas de Proteção por Camada

| Camada            | Medidas de Segurança                 | Compliance |
|-------------------|--------------------------------------|------------|
| **Rede**          | TLS 1.3, VPN, Firewall               | ISO 27001  |
| **Armazenamento** | AES-256-GCM, Criptografia em repouso | LGPD, GDPR |
| **Processamento** | Dados anonimizados, Logs mascarados  | PDPA, CCPA |
| **Acesso**        | MFA, Rotação de chaves, Audit trails | SOC 2      |

### Política de Retenção e Privacidade

| Tipo de Dado            | Período Retenção | Anonimização     | Direito ao Esquecimento |
|-------------------------|------------------|------------------|-------------------------|
| Dados biométricos crus  | 7 dias           | ✅ Completa     | ✅ Imediato             |
| Metadados processamento | 1 ano            | ✅ Parcial      | ✅ 30 dias              |
| Logs de auditoria       | 2 anos           | ✅ Mascaramento | ❌ Regulamentado        |
| Dados analytics         | Indefinido       | ✅ Total        | ✅ Implementado         |

## 📈 Monitoramento e Métricas

### Principais Indicadores de Performance (KPI)

| Métrica                   | Limite Aceitável | Limite Crítico | Ação               |
|---------------------------|------------------|----------------|--------------------|
| Taxa de falso positivo    | < 1%             | > 2%           | Revisar thresholds |
| Tempo médio processamento | < 800ms          | > 2000ms       | Otimizar provedor  |
| Disponibilidade provedor  | > 99.5%          | < 95%          | Ativar fallback    |
| Qualidade média imagem    | > 0.7            | < 0.4          | Melhorar captura   |

### Sistema de Alertas

| Severidade  | Condição                   | Ação Imediata                      |
|-------------|----------------------------|------------------------------------|
| **Crítico** | FAR > 2%                   | Bloquear sistema, notificar equipe |
| **Alto**    | Provedor principal offline | Ativar fallback automático         |
| **Médio**   | Latência > 1500ms          | Escalar para análise               |
| **Baixo**   | Qualidade imagem < 0.5     | Logar para melhoria                |

## 🚀 Estratégia de Implantação

### Fases de Rollout

| Fase                    | Provedores         | Tráfego | Ambientes  | Duração   |
|-------------------------|--------------------|---------|------------|-----------|
| **1 - Desenvolvimento** | Mock               | 100%    | Dev, Test  | 2 semanas |
| **2 - Staging**         | Mock + Local       | 50%/50% | Staging    | 1 semana  |
| **3 - Pré-produção**    | AWS + Local        | 25%/75% | Preprod    | 1 semana  |
| **4 - Produção**        | AWS + Local + Mock | 100%    | Production | Contínuo  |

### Health Checks Implementados

| Check            | Frequência  | Timeout | Ação em Falha       |
|------------------|-------------|---------|---------------------|  
| Conexão AWS      | 30 segundos | 10s     | Fallback para local |
| Modelo local     | 60 segundos | 15s     | Restart service     |
| Qualidade imagem | Por request | 5s      | Rejeitar imagem     |
| Storage          | 5 minutos   | 30s     | Alertar equipe      |

## 💡 Melhores Práticas Recomendadas

### Para Implementação
1. **Sempre usar modo "auto"** para seleção automática de provedor
2. **Configurar fallbacks** em ordem: AWS → Local → Mock
3. **Implementar circuit breaker** para provedores externos
4. **Validar qualidade de imagem** antes do processamento

### Para Monitoramento
1. **Monitorar FAR/FRR** semanalmente
2. **Ajustar thresholds** baseado em dados reais
3. **Manter modelos locais** atualizados
4. **Revisar logs de auditoria** diariamente

### Para Segurança
1. **Nunca armazenar** imagens brutas por mais de 7 dias
2. **Implementar criptografia** end-to-end
3. **Validar compliance** regularmente
4. **Realizar pentests** trimestralmente

# Achitecture - DOC
## Back-end
CHALLENGE_TOP_ONE/                    .............................................# raiz do repositório <br>
│<br>
├── eyeoftoga_back/                  .............................................# pacote principal do SDK ( código fonte )<br>
│   ├── __init__.py               .............................................# exporta classes públicas, __version__<br>
│   ├── __main__.py               .............................................# entrypoint para `python -m nexshop_sdk` (CLI)<br>
│   ├── core.py                   .............................................# orquestrador - interface pública do SDK<br>
│   ├── config.py                 .............................................# configuração: carregamento de env, arquivos, defaults<br>
│   ├── logging_config.py         .............................................# configuração central de logging (struct log)<br>
│   ├── utils.py                  .............................................# helpers genéricos (serialização, validators)<br>
│   ├── exceptions.py             .............................................# exceções específicas do SDK<br>
│   ├── types.py                  .............................................# dataclasses / pydantic models (UserData, DeviceInfo, ScoreResult)<br>
│   │<br>
│   ├── api/                      .............................................# adaptadores / middleware para frameworks web<br>
│   │   ├── __init__.py<br>
│   │   ├── fastapi_adapter.py    .............................................# funções para integrar com FastAPI (dependências, endpoints)<br>
│   │   ├── flask_adapter.py      .............................................# blueprint/handlers para Flask<br>
│   │   └── django_adapter.py     .............................................# hooks / middleware para Django<br>
│   │<br>
│   ├── data_collection/          .............................................# coleta de dados (apenas backend-side hooks)<br>
│   │   ├── __init__.py<br>
│   │   ├── device_info.py        .............................................# parser de user-agent, browser, OS, fingerprint server-side<br>
│   │   ├── ip_location.py        .............................................# IP -> geolocalização (abstração / provider interface)<br>
│   │   ├── session_behavior.py   .............................................# endpoints/handlers para eventos (click, scroll, timing)<br>
│   │   └── storage_adapter.py    .............................................# abstração para persistência temporária (cache/db)<br>
│   │<br>
│   ├── biometrics/               .............................................# biometria backend (captura/validação delegada)<br>
│   │   ├── __init__.py<br>
│   │   ├── face_capture.py       .............................................# helpers para receber/validar imagens (base64/bytes)<br>
│   │   ├── face_validation.py    .............................................# wrapper para modelos/serviços de verificação facial<br>
│   │   └── providers/            .............................................# adaptadores para diferentes providers (local / cloud)<br>
│   │       ├── __init__.py<br>
│   │       ├── mock_provider.py<br>
│   │       └── aws_rekognition.py<br>
│   │<br>
│   ├── score_engine/              .............................................# cálculo do score e regras<br>
│   │   ├── __init__.py<br>
│   │   ├── scoring.py            .............................................# função principal calcular_score(dados) -> ScoreResult<br>
│   │   ├── features.py           .............................................# extratores de features (device_risk, behavior_risk, geo_risk, bio_risk)<br>
│   │   ├── rules.py              .............................................# regras fixas / thresholds e pipeline de decisão<br>
│   │   └── explainability.py     .............................................# gerar razões/atribuições (why score = X)<br>
│   │<br>
│   ├── integrations/             .............................................# adaptadores para sistemas/fluxos externos<br>
│   │   ├── __init__.py<br>
│   │   ├── ecommerce_mock.py     .............................................# simula fluxo de checkout/login para testes<br>
│   │   ├── webhook_sender.py     .............................................# enviar webhook para sistemas que consomem o resultado<br>
│   │   └── adapters/             .............................................# adapters para plataformas reais (Shopify, Magento, Woo)<br>
│   │       ├── __init__.py<br>
│   │       └── shopify_adapter.py<br>
│   │<br>
│   ├── output/                   .............................................# formatação/serialização da saída (backend "page")<br>
│   │   ├── __init__.py<br>
│   │   ├── score_output.py       .............................................# monta ScoreResult (dict / JSON) com detalhes + reasons<br>
│   │   ├── events.py             .............................................# eventos internos (Audit log, Decisions)<br>
│   │   └── policies.py           .............................................# ações recomendadas (allow, step-up, block) e payloads<br>
│   │<br>
│   ├── persistence/              .............................................# interfaces para armazenamento (opcional)<br>
│   │   ├── __init__.py<br>
│   │   ├── cache.py              .............................................# interface Redis / in-memory<br>
│   │   └── db_adapter.py         .............................................# interface para RDBMS / timeseries / data lake<br>
│   │<br>
│   ├── telemetry/                .............................................# métricas, tracing e health checks<br>
│   │   ├── __init__.py<br>
│   │   ├── metrics.py            .............................................# contadores / histogram (Prometheus)<br>
│   │   └── tracing.py            .............................................# hooks de tracing (opentelemetry)<br>
│   │<br>
│   └── tests_support/            .............................................# utilitários para testes (mocks, fixtures)<br>
│       ├── __init__.py<br>
│       └── fixtures.py<br>
│
├── examples/                     .............................................# exemplos de integração backend-only<br>
│   ├── exemplo_login.py          .............................................# exemplo de chamada em login<br>
│   ├── exemplo_checkout.py       .............................................# exemplo de chamada no checkout<br>
│   └── run_simulation.py         .............................................# simula fluxo completo (coleta -> scoring -> webhook)<br>
│<br>
├── tests/                         .............................................# testes unitários / integração<br>
│   ├── __init__.py<br>
│   ├── test_scoring.py<br>
│   ├── test_data_collection.py<br>
│   ├── test_biometrics.py<br>
│   └── test_output.py<br>
│<br>
├── docs/                          .............................................# Documentação <br>
│   ├── API.md<br>
│   ├── Architeture.md<br>
│   ├── Biometrics.md<br>
│   ├── Data_Collection.md<br>
│   ├── EyeOfToga_SDK.md<br>
│   ├── Integrations.md<br>
│   ├── Output.md<br>
│   ├── Percistence.md<br>
│   ├── Scoring.md<br>
│   ├── Scripts.md<br>
│   └── Telemetrt.md<br>
│<br>
├── scripts/                      .............................................# scripts úteis (dev, build, lint)<br>
│   ├── run_local.sh<br>
│   └── generate_api_stub.sh<br>
│<br>
├── .github/                       .............................................# CI / templates<br>
│   └── workflows/<br>
│       └── ci.yml<br>
│<br>
├── Dockerfile                     .............................................# containerização do SDK para testes/execução<br>
├── pyproject.toml                 .............................................# build system / dependências (preferível moderno)<br>
├── setup.cfg / setup.py           .............................................# empacotamento (opcional)<br>
├── requirements.txt               .............................................# dependências (se não usar pyproject)<br>
├── README.md<br>
└── LICENSE<br>
## Front-end
src/<br>
│<br>
├── front/<br>
│   ├── dashboard/<br>
│   │   ├── dashboard_screen.dart         # Explicação: Tela inicial com KPIs, gráficos e visão geral dos eventos<br>
│   │   ├── dashboard_controller.dart     # Explicação: Lógica para buscar dados do backend e atualizar a tela<br>
│   │   ├── widgets/<br>
│   │   │   ├── metric_card.dart          # Explicação: Card visual para exibir métricas rápidas (ex: bloqueios hoje)<br>
│   │   │   ├── activity_graph.dart       # Explicação: Gráfico mostrando evolução de eventos ao longo do tempo<br>
│   │   │   ├── user_table.dart           # Explicação: Tabela com usuários bloqueados, status e filtros<br>
│   │   │   └── real_time_log.dart        # Explicação: Lista de eventos atualizada em tempo real<br>
│   │<br>
│   ├── setup/<br>
│   │   ├── wizard_screen.dart            # Explicação: Assistente passo a passo para configuração inicial do sistema<br>
│   │   ├── storage_settings.dart         # Explicação: Configuração de armazenamento (Local, Cloud, Retenção de dados)<br>
│   │   ├── module_settings.dart          # Explicação: Escolha dos módulos ativos (biometria, análise de comportamento, etc.)<br>
│   │   ├── integration_settings.dart     # Explicação: Configuração de integrações externas (SIEM, SOAR, IAM, Webhooks)<br>
│   │   └── confirmation_screen.dart      # Explicação: Resumo final antes de aplicar as configurações<br>
│   │<br>
│   ├── auth/<br>
│   │   ├── login_screen.dart             # Explicação: Tela de login para administradores<br>
│   │   ├── register_screen.dart          # Explicação: Tela para cadastro de novos administradores<br>
│   │   └── forgot_password.dart          # Explicação: Tela para recuperação de senha via e-mail ou OTP<br>
│   │<br>
│   ├── reports/<br>
│   │   ├── reports_screen.dart           # Explicação: Lista e visualização de relatórios filtrados<br>
│   │   └── export_options.dart           # Explicação: Opções para exportar relatórios (CSV, PDF, JSON)<br>
│   │<br>
│   ├── monitoring/<br>
│   │   ├── real_time_monitor_screen.dart # Explicação: Tela com monitoramento ao vivo dos eventos de segurança<br>
│   │   └── event_details_modal.dart      # Explicação: Modal com detalhes completos de um evento<br>
│   │<br>
│   ├── settings/<br>
│   │   ├── general_settings.dart         # Explicação: Configurações gerais (idioma, tema, fuso horário)<br>
│   │   ├── security_settings.dart        # Explicação: Ajuste de thresholds, níveis de bloqueio e tempo de sessão<br>
│   │   └── permissions_settings.dart     # Explicação: Gerenciamento de usuários e permissões<br>
│   │<br>
│   └── shared/<br>
│       ├── styles.dart                   # Explicação: Definição de temas, cores, tipografia e espaçamentos<br>
│       ├── constants.dart                # Explicação: Variáveis fixas, chaves de API e URLs base<br>  
│       └── widgets/<br>
│           ├── custom_button.dart        # Explicação: Botão padronizado do sistema<br>
│           ├── custom_input_field.dart   # Explicação: Campo de texto padronizado do sistema<br>
│           └── page_header.dart          # Explicação: Cabeçalho de páginas com título e breadcrumbs<br>

# API - DOC
## 🔐 Auth.py

### 🎯 Finalidade
Fornecer serviços de autenticação e autorização para o SDK EyeOfToga, incluindo validação de tokens JWT, gerenciamento de permissões e controle de acesso baseado em roles.

### 📦 Dependências
- `jose` - Para validação e decodificação de tokens JWT
- `datetime` - Para manipulação de datas e expiração de tokens
- `cryptography` - Para operações criptográficas avançadas
- `logging` - Para registro de logs de segurança
- `typing` - Para type hints e definição de tipos

### 🧩 Principais Componentes

**Classes Principais:**
- `AuthManager` - Gerenciador central de autenticação
- `TokenValidator` - Validador de tokens JWT
- `PermissionService` - Serviço de gerenciamento de permissões

**Estruturas de Dados:**
- `UserClaims` - Claims do usuário extraídos do token
- `AuthConfig` - Configuração de autenticação
- `AccessPolicy` - Políticas de acesso baseadas em roles

### 🔧 Funcionamento

O módulo implementa um sistema completo de autenticação:

1. **Validação de Token**: Verifica assinatura, expiração e claims
2. **Extração de Claims**: Extrai informações do usuário do token JWT
3. **Verificação de Permissões**: Valida se usuário tem acesso ao recurso
4. **Logs de Segurança**: Registra tentativas de acesso bem-sucedidas e falhas

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.auth import AuthManager, UserClaims

# Inicializar gerenciador de autenticação
auth_manager = AuthManager()

# Validar token JWT
try:
    user_claims: UserClaims = auth_manager.validate_token("jwt_token_here")
    print(f"Usuário autenticado: {user_claims.username}")
except Exception as e:
    print(f"Falha na autenticação: {e}")

# Verificar permissões
if auth_manager.has_permission(user_claims, "biometrics:read"):
    print("Usuário tem permissão para leitura biométrica")
```

### ⚠️ Observações

- **Segurança**: Utiliza algoritmos criptográficos robustos para validação
- **Performance**: Cache de chaves públicas para melhor performance
- **Extensível**: Suporte a múltiplos provedores de identidade
- **Logs Detalhados**: Auditoria completa de acesso

---

## 🤖 Biometrics.py

### 🎯 Finalidade
Módulo principal para integração e orquestração dos serviços biométricos do EyeOfToga, proporcionando uma interface unificada para captura, validação e verificação facial.

### 📦 Dependências
- `numpy` - Para manipulação de arrays e operações matemáticas
- `PIL` - Para processamento básico de imagens
- `base64` - Para codificação/decodificação de imagens
- `typing` - Para type hints e definição de tipos
- `logging` - Para registro de logs de operações biométricas

### 🧩 Principais Componentes

**Classes Principais:**
- `BiometricService` - Serviço principal de biometria
- `FaceAnalyzer` - Analisador de características faciais
- `QualityChecker` - Verificador de qualidade de imagens

**Estruturas de Dados:**
- `BiometricConfig` - Configuração do serviço biométrico
- `FaceDetectionResult` - Resultado da detecção facial
- `VerificationResult` - Resultado da verificação biométrica

### 🔧 Funcionamento

O módulo coordena todo o fluxo biométrico:

1. **Recebimento de Imagem**: Aceita imagens em múltiplos formatos (base64, bytes, caminho)
2. **Pré-processamento**: Ajusta qualidade, redimensiona e normaliza
3. **Análise Facial**: Detecta faces e extrai características
4. **Verificação**: Compara com referência ou base de dados
5. **Resultado**: Retorna score de confiança e metadados

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.biometrics import BiometricService, VerificationResult

# Inicializar serviço biométrico
biometric_service = BiometricService()

# Carregar imagem de referência
with open("reference_face.jpg", "rb") as f:
    reference_image = f.read()

# Carregar imagem para verificar
with open("unknown_face.jpg", "rb") as f:
    unknown_image = f.read()

# Realizar verificação facial
result: VerificationResult = biometric_service.verify_faces(
    reference_image=reference_image,
    unknown_image=unknown_image,
    threshold=0.75  # Limite de confiança
)

print(f"Similaridade: {result.confidence:.2f}")
print(f"Verificado: {result.is_verified}")
```

### ⚠️ Observações

- **Multi-formato**: Suporte a JPEG, PNG, WebP e outros formatos
- **Otimizado**: Balanceamento entre precisão e performance
- **Extensível**: Fácil integração com novos provedores
- **Detalhado**: Metadados ricos para análise posterior

---

## 🔒 Crypto.py

### 🎯 Finalidade
Fornecer serviços criptográficos seguros para o EyeOfToga SDK, incluindo criptografia de dados sensíveis, geração de hashes, assinaturas digitais e gerenciamento de chaves.

### 📦 Dependências
- `cryptography` - Para operações criptográficas primitivas
- `hashlib` - Para funções de hash criptográficas
- `secrets` - Para geração de números aleatórios seguros
- `base64` - Para codificação/decodificação segura
- `logging` - Para auditoria de operações criptográficas

### 🧩 Principais Componentes

**Classes Principais:**
- `CryptoService` - Serviço principal de criptografia
- `KeyManager` - Gerenciador de chaves criptográficas
- `HashService` - Serviço de geração de hashes

**Algoritmos Suportados:**
- Criptografia: AES-256-GCM, ChaCha20-Poly1305
- Hash: SHA-256, SHA-512, BLAKE2b
- Assinatura: ECDSA, Ed25519

### 🔧 Funcionamento

O módulo oferece operações criptográficas completas:

1. **Criptografia Simétrica**: Dados sensíveis com chaves AES
2. **Hashing Seguro**: Hashes com salt para armazenamento seguro
3. **Assinatura Digital**: Verificação de integridade e autenticidade
4. **Geração de Chaves**: Criação segura de chaves criptográficas

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.crypto import CryptoService

# Inicializar serviço criptográfico
crypto_service = CryptoService()

# Dados sensíveis para criptografar
sensitive_data = "dados super secretos"
key = crypto_service.generate_key()  # Gera chave AES-256

# Criptografar dados
encrypted_data, nonce, tag = crypto_service.encrypt(
    plaintext=sensitive_data.encode(),
    key=key
)

print(f"Dados criptografados: {encrypted_data.hex()}")

# Descriptografar dados
decrypted_data = crypto_service.decrypt(
    ciphertext=encrypted_data,
    key=key,
    nonce=nonce,
    tag=tag
)

print(f"Dados originais: {decrypted_data.decode()}")
```

### ⚠️ Observações

- **Auditável**: Todas as operações são registradas em log
- **Secure by Default**: Configurações seguras como padrão
- **Performance**: Otimizado para operações em lote
- **Compliance**: Conformidade com padrões de segurança

---

## 🔗 Dependencies.py

### 🎯 Finalidade
Gerenciar injeção de dependências e configuração do EyeOfToga SDK, proporcionando inicialização lazy, caching de instâncias e resolução automática de dependências.

### 📦 Dependências
- `injector` - Para injeção de dependências avançada
- `typing` - Para type hints e definição de tipos
- `logging` - Para debug de resolução de dependências
- `functools` - Para decorators e caching

### 🧩 Principais Componentes

**Classes Principais:**
- `DependencyContainer` - Container principal de DI
- `ServiceLocator` - Localizador de serviços registrados
- `ConfigProvider` - Provedor de configuração centralizada

**Padrões Implementados:**
- Singleton: Instâncias únicas por classe
- Factory: Criação sob demanda de serviços
- Lazy: Inicialização apenas quando necessário

### 🔧 Funcionamento

O sistema de dependências opera em três fases:

1. **Registro**: Serviços são registrados no container
2. **Resolução**: Dependências são resolvidas automaticamente
3. **Injeção**: Instâncias são injetadas nos consumidores

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.dependencies import DependencyContainer
from eyeoftoga_sdk.biometrics import BiometricService
from eyeoftoga_sdk.auth import AuthManager

# Configurar container de dependências
container = DependencyContainer()

# Registrar serviços
container.register_singleton(BiometricService)
container.register_singleton(AuthManager)

# Resolver dependências (injeção automática)
biometric_service = container.resolve(BiometricService)
auth_manager = container.resolve(AuthManager)

# Usar serviços injetados
result = biometric_service.verify_faces(...)
```

### ⚠️ Observações

- **Thread-Safe**: Adequado para ambientes concorrentes
- **Extensível**: Fácil adição de novos serviços
- **Debugável**: Logs detalhados de resolução
- **Performance**: Cache de instâncias para melhor performance

---

## 🛡️ Middleware.py

### 🎯 Finalidade
Fornecer middlewares comuns para frameworks web, incluindo autenticação, logging, tratamento de erros e métricas de performance para integração transparente do EyeOfToga SDK.

### 📦 Dependências
- `time` - Para medição de tempo e performance
- `logging` - Para registro structured logging
- `functools` - Para decorators de middleware
- `typing` - Para type hints e definição de tipos

### 🧩 Principais Componentes

**Middlewares Principais:**
- `AuthMiddleware` - Middleware de autenticação JWT
- `LoggingMiddleware` - Middleware de logging estruturado
- `ErrorHandlingMiddleware` - Middleware de tratamento de erros
- `MetricsMiddleware` - Middleware de coleta de métricas

**Compatibilidade:**
- FastAPI: Decorators e dependencies
- Flask: Blueprints e before/after request
- Django: Middleware classes

### 🔧 Funcionamento

Cada middleware executa em uma fase específica do request:

1. **Before Request**: Autenticação, validação, logging
2. **During Request**: Processamento principal
3. **After Request**: Logging, métricas, limpeza
4. **Error Handling**: Tratamento consistente de erros

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.middleware import AuthMiddleware, LoggingMiddleware
from fastapi import FastAPI

app = FastAPI()

# Adicionar middlewares
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

@app.get("/protected")
async def protected_route():
    # Rota automaticamente protegida por autenticação
    return {"message": "Acesso permitido"}
```

### ⚠️ Observações

- **Framework Agnostic**: Funciona com FastAPI, Flask, Django
- **Configurável**: Comportamento personalizável por configuração
- **Performance**: Baixo overhead nas operações
- **Extensível**: Fácil criação de novos middlewares

---

## 🐳 Dockerfile

### 🎯 Finalidade
Fornecer containerização consistente e otimizada para o EyeOfToga SDK, garantindo ambiente reproduzível, dependências controladas e deployment simplificado.

### 📦 Dependências
- Python 3.9+ - Versão base do runtime
- Build essentials - Para compilação de dependências
- Security updates - Pacotes atualizados para segurança

### 🧩 Estágios de Build

**Multi-stage build para otimização:**
1. **Builder Stage**: Compilação de dependências e assets
2. **Runtime Stage**: Imagem final minimalista e segura

### 🔧 Funcionamento

O Dockerfile implementa práticas recomendadas:

1. **Layer Caching**: Ordenação inteligente para cache eficiente
2. **Security Hardening**: Usuário não-root, permissões restritas
3. **Size Optimization**: Multi-stage build para imagem minimalista
4. **Healthchecks**: Verificação automática de saúde do container

### 📊 Exemplo de Uso

```bash
# Build da imagem
docker build -t eyeoftoga-sdk .

# Executar container
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -v ./config:/app/config \
  eyeoftoga-sdk
```

### ⚠️ Observações

- **Security**: Sem root privileges, packages atualizados
- **Performance**: Otimizado para cold start rápido
- **Production Ready**: Configurações adequadas para produção
- **Extensível**: Fácil adaptação para diferentes ambientes

---

## 📋 Requirements.txt

### 🎯 Finalidade
Gerenciar dependências Python do EyeOfToga SDK com versionamento preciso, garantindo consistência entre ambientes de desenvolvimento, teste e produção.

### 📦 Categorias de Dependências

**Core:**
- fastapi>=0.68.0 - Framework web async
- numpy>=1.21.0 - Computação numérica
- pillow>=8.3.0 - Processamento de imagem

**Security:**
- cryptography>=3.4.0 - Criptografia
- python-jose>=3.3.0 - JWT tokens

**Utils:**
- pydantic>=1.8.0 - Validação de dados
- loguru>=0.5.0 - Logging estruturado

### 🔧 Gerenciamento de Versões

- **Versionamento Pinned**: Versões exatas para produção
- **Range Testing**: ranges para desenvolvimento
- **Security Scanning**: Dependências verificadas por vulnerabilidades

### 📊 Exemplo de Conteúdo

```txt
# Core dependencies
fastapi==0.68.0
uvicorn==0.15.0

# Security
cryptography==3.4.8
python-jose==3.3.0

# Image processing
numpy==1.21.0
pillow==8.3.0

# Utilities
pydantic==1.8.2
loguru==0.5.0
```

### ⚠️ Observações

- **Reprodutibilidade**: Builds consistentes em qualquer ambiente
- **Security**: Análise regular de vulnerabilidades
- **Manutenção**: Atualizações regulares de dependências
- **Compatibilidade**: Testes de compatibilidade entre versões

## 🔍 AWS Rekognition Provider

### 🎯 Finalidade
Integração com o Amazon Rekognition para serviços de análise facial, proporcionando reconhecimento facial em escala empresarial com alta precisão e baixa latência através de APIs gerenciadas pela AWS.

### 📦 Dependências
- `boto3` - SDK oficial da AWS para Python
- `botocore` - Biblioteca core do AWS SDK
- `logging` - Para logging estruturado de operações
- `time` - Para medição de performance e timeouts
- `base64` - Para codificação/decodificação de imagens
- `json` - Para serialização de respostas da AWS

### 🧩 Principais Componentes

**Classes Principais:**
- `AWSRekognitionProvider` - Implementação do provedor AWS
- `RekognitionConfig` - Configuração específica do AWS Rekognition
- `RekognitionResponse` - Modelo de resposta padronizado

**Métodos Principais:**
- `compare_faces()` - Compara duas imagens faciais
- `detect_faces()` - Detecta faces em uma imagem
- `search_faces()` - Busca faces em coleção (face matching)
- `index_face()` - Indexa face em coleção para busca futura

### 🔧 Funcionamento

O provedor implementa a interface `BiometricProvider` com:

1. **Autenticação AWS**: Configuração de credenciais via IAM
2. **Chamadas API**: Comunicação com endpoints do Rekognition
3. **Processamento**: Análise de imagens e extração de features
4. **Normalização**: Adaptação de respostas AWS para formato padrão

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.biometrics.providers.aws_rekognition import AWSRekognitionProvider

# Configurar provedor AWS
aws_config = {
    'region_name': 'us-east-1',
    'aws_access_key_id': 'your-access-key',
    'aws_secret_access_key': 'your-secret-key',
    'collection_id': 'eyeoftoga-faces'
}

provider = AWSRekognitionProvider(aws_config)

# Comparar duas faces
with open("face1.jpg", "rb") as f1, open("face2.jpg", "rb") as f2:
    result = provider.compare_faces(f1.read(), f2.read())
    
print(f"Similaridade: {result['similarity']:.2f}")
print(f"Confiança: {result['confidence']:.2f}")

# Resultado esperado:
# Similaridade: 0.92
# Confiança: 99.8
```

### ⚠️ Observações

- **Custos AWS**: Utiliza Amazon Rekognition (cobrança por uso)
- **Latência**: Depende da região AWS e qualidade de rede
- **Limites**: Respeita limites de API da AWS (TPS)
- **Disponibilidade**: Sujeito ao SLA da AWS (99.9% uptime)

---

## 🧪 Mock Provider

### 🎯 Finalidade
Provedor simulado para desenvolvimento, testes e ambientes de staging que não requerem integração com serviços reais de biometria, proporcionando comportamento previsível e configurável.

### 📦 Dependências
- `random` - Para geração de valores aleatórios controlados
- `time` - Para simulação de latência de rede
- `logging` - Para debug de operações simuladas
- `unittest.mock` - Para criação de objetos mock (opcional)

### 🧩 Principais Componentes

**Classes Principais:**
- `MockBiometricProvider` - Implementação do provedor mock
- `MockConfig` - Configuração do comportamento simulado
- `MockResponse` - Respostas predefinidas para testes

**Comportamentos Simulados:**
- ✅ Sucesso com similaridade configurável
- ❌ Falhas controladas (erros de rede, timeout)
- ⏱️ Latência artificial para testes de performance
- 📊 Dados consistentes para testes repetíveis

### 🔧 Funcionamento

O provedor mock oferece várias estratégias de simulação:

1. **Modo Determinístico**: Sempre retorna mesmo resultado
2. **Modo Aleatório**: Gera resultados dentro de ranges configuráveis
3. **Modo Sequencial**: Ciclo através de respostas predefinidas
4. **Modo Erro**: Simula falhas específicas sob demanda

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.biometrics.providers.mock_provider import MockBiometricProvider

# Configurar provedor mock para testes
mock_config = {
    'mode': 'deterministic',
    'fixed_similarity': 0.85,
    'fixed_confidence': 0.95,
    'simulate_latency': True,
    'min_latency_ms': 100,
    'max_latency_ms': 500
}

provider = MockBiometricProvider(mock_config)

# Teste com resultado previsível
result = provider.compare_faces(b"fake_image_1", b"fake_image_2")
print(f"Similaridade: {result['similarity']}")  # Sempre 0.85
print(f"Confiança: {result['confidence']}")     # Sempre 0.95

# Teste com modo aleatório
random_config = {
    'mode': 'random',
    'min_similarity': 0.1,
    'max_similarity': 0.99,
    'error_rate': 0.1  # 10% de chance de erro
}

random_provider = MockBiometricProvider(random_config)
```

### ⚠️ Observações

- **Desenvolvimento**: Ideal para desenvolvimento sem dependências externas
- **Testes**: Permite testes unitários isolados e consistentes
- **Performance**: Sem latência real de rede ou processamento
- **Limitações**: Não oferece validação real de algoritmos biométricos

---

## 💻 Local Face Recognition Provider

### 🎯 Finalidade
Provedor de reconhecimento facial local utilizando bibliotecas open-source, proporcionando funcionalidade biométrica offline sem dependência de serviços cloud ou APIs externas.

### 📦 Dependências
- `face_recognition` - Biblioteca base para reconhecimento facial
- `dlib` - Dependency principal para machine learning
- `numpy` - Para operações matriciais e manipulação de embeddings
- `cv2` (OpenCV) - Para processamento de imagem avançado
- `PIL` - Para manipulação básica de imagens

### 🧩 Principais Componentes

**Classes Principais:**
- `LocalFaceRecognitionProvider` - Implementação local
- `FaceEncoding` - Representação numérica de características faciais
- `LocalRecognitionConfig` - Configuração para processamento local

**Funcionalidades:**
- `extract_face_encodings()` - Extrai embeddings faciais
- `calculate_face_distance()` - Calcula distância entre embeddings
- `detect_face_locations()` - Detecta coordenadas de faces na imagem
- `compare_face_encodings()` - Compara múltiplos encodings

### 🔧 Funcionamento

O provedor local opera completamente offline:

1. **Detecção Facial**: Identifica rostos usando HOG + SVM
2. **Extração de Features**: Gera embeddings de 128 dimensões
3. **Comparação**: Calcula distância euclidiana entre embeddings
4. **Decisão**: Aplica threshold para verificação

### 📊 Exemplo de Uso

```python
from eyeoftoga_sdk.biometrics.providers.local_face_recognition import LocalFaceRecognitionProvider

# Configurar provedor local
local_config = {
    'model': 'hog',  # ou 'cnn' para melhor precisão (mais lento)
    'number_of_times_to_upsample': 1,
    'tolerance': 0.6,  # Threshold para matching
    'gpu_acceleration': False  # Usar GPU se disponível
}

provider = LocalFaceRecognitionProvider(local_config)

# Carregar e comparar imagens
image_1 = load_image("person_1.jpg")
image_2 = load_image("person_2.jpg")

result = provider.compare_faces(image_1, image_2)

if result['match']:
    print(f"Faces correspondem! Similaridade: {result['similarity']:.2f}")
else:
    print("Faces não correspondem")
```

### ⚠️ Observações

- **Offline**: Funciona completamente sem internet
- **Privacidade**: Dados nunca saem do dispositivo/local
- **Performance**: Consome mais CPU que soluções cloud
- **Precisão**: Alta precisão mas depende da qualidade das imagens
- **Recursos**: Requer mais memória RAM que provedores cloud

---

## 📊 Comparação entre Provedores

| Característica | AWS Rekognition | Local Recognition | Mock Provider |
|----------------|-----------------|-------------------|---------------|
| **Precisão** | ⭐⭐⭐⭐⭐ (99.9%) | ⭐⭐⭐⭐ (95-98%) | ⭐ (Configurável) |
| **Latência** | ⭐⭐⭐⭐ (200-500ms) | ⭐⭐⭐ (500-2000ms) | ⭐⭐⭐⭐⭐ (0-100ms) |
| **Custo** | $$$ (Por uso) | $ (Hardware) | $ (Zero) |
| **Privacidade** | ⭐⭐ (Dados na AWS) | ⭐⭐⭐⭐⭐ (Local) | ⭐⭐⭐⭐⭐ (Local) |
| **Offline** | ❌ | ✅ | ✅ |
| **Escalabilidade** | ⭐⭐⭐⭐⭐ (Auto-scale) | ⭐⭐ (Limitado local) | ⭐⭐⭐⭐⭐ (Ilimitado) |
| **Facilidade** | ⭐⭐⭐⭐ (API simples) | ⭐⭐ (Complexo setup) | ⭐⭐⭐⭐⭐ (Muito fácil) |

---

## 🔄 Estratégia de Fallback

O EyeOfToga SDK implementa fallback automático entre provedores:

```python
# Estratégia de tentativa em ordem de preferência
providers = [
    AWSRekognitionProvider(aws_config),
    LocalFaceRecognitionProvider(local_config),
    MockBiometricProvider(mock_config)  # Fallback final
]

for provider in providers:
    try:
        result = provider.compare_faces(image1, image2)
        break  # Sucesso, sair do loop
    except Exception as e:
        print(f"Provedor {type(provider).__name__} falhou: {e}")
        continue # Tentar próximo provedor
```
