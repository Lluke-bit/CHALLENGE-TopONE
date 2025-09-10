from cryptography.fernet import Fernet
import os

# Gere uma chave Fernet e armazene-a de forma segura (variável de ambiente, Key Management Service)
# Apenas para desenvolvimento, você pode gerar uma: Fernet.generate_key().decode()
# Em produção, NUNCA gere a chave no código, use um KMS.
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode('utf-8')
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY não definida nas variáveis de ambiente.")

f = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: bytes) -> bytes:
    """Criptografa dados usando Fernet."""
    return f.encrypt(data)

def decrypt_data(encrypted_data: bytes) -> bytes:
    """Descriptografa dados usando Fernet."""
    return f.decrypt(encrypted_data)