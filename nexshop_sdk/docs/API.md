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
