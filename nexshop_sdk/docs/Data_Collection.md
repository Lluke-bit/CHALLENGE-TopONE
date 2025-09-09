## 📥 Data-Collection

### 🔎 O que vamos coletar

#### 1. Identificação do Dispositivo e Ambiente
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

#### 2. Sessão, Acesso e Autenticação
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

#### 3. Dados de Uso e Comportamento
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

#### 4. Segurança e Compliance
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

#### 5. Métricas de Performance e Telemetria
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

#### 6. Integrações Externas e Serviços
- Chamadas para APIs de terceiros (endpoint, tempo de resposta, status)
- Status de integrações (ativo, falho, indisponível)
- Logs de auditoria de integrações
- Dependências externas do SDK
- Webhooks disparados (payload, resposta)
- Comunicação com mensageria (Kafka, RabbitMQ, SQS, etc.)
- Configurações recebidas remotamente (feature flags, parâmetros)

---

#### 7. Dados de Negócio (Customizáveis)
*(Definidos pela aplicação que usa o SDK – exemplos abaixo)*
- Identificador único do cliente
- Plano/assinatura do usuário
- Funções/papéis no sistema (roles)
- Preferências do usuário
- Histórico de compras/transações
- Pontos de engajamento (gamificação, níveis, badges)
- Contexto de uso (mobile app, portal web, API backend)
