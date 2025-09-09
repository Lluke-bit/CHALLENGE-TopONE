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

---

Esta documentação cobre os arquivos principais da estrutura atual do EyeOfToga SDK. Para uma documentação completa, seria necessário expandir para os demais arquivos e módulos específicos.
