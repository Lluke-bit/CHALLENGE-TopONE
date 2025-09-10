from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from typing import Annotated
from pydantic import BaseModel

from biometrics import face_capture, face_validation
from database import crud
from database.config import get_db_session
from security import auth as security_auth, crypto as security_crypto

router = APIRouter()

class BiometricRegisterResponse(BaseModel):
    message: str
    user_id: int

class BiometricAuthResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=BiometricRegisterResponse)
async def register_biometric(
    user_id: int, # Ou pode ser inferido pelo token de um usuário logado
    file: UploadFile = File(...),
    db: Annotated[crud.Session, Depends(get_db_session)]
):
    # 1. Receber e processar a imagem
    image_bytes = await file.read()
    try:
        face_encoding = face_capture.get_face_encoding(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Criptografar o template biométrico
    encrypted_template = security_crypto.encrypt_data(face_encoding.tobytes())

    # 3. Armazenar no banco de dados (associado ao user_id)
    # O user_id aqui pressupõe que o usuário já foi criado ou está logado.
    # Em um cenário real, você buscaria o usuário pelo token ou criaria um novo.
    await crud.create_biometric_template(db, user_id, encrypted_template)

    return {"message": "Biometria registrada com sucesso!", "user_id": user_id}

@router.post("/authenticate", response_model=BiometricAuthResponse)
async def authenticate_biometric(
    file: UploadFile = File(...),
    db: Annotated[crud.Session, Depends(get_db_session)]
):
    # 1. Receber e processar a imagem de autenticação
    image_bytes = await file.read()
    try:
        current_face_encoding = face_capture.get_face_encoding(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Recuperar todos os templates biométricos do banco de dados (ou filtrar por usuário se já logado)
    # Para demonstração, vamos iterar sobre todos. Em produção, buscaríamos por user_id.
    templates_from_db = await crud.get_all_biometric_templates(db)

    authenticated_user_id = None
    for template_obj in templates_from_db:
        # Descriptografar o template
        decrypted_template_bytes = security_crypto.decrypt_data(template_obj.template_data)
        stored_face_encoding = face_validation.bytes_to_encoding(decrypted_template_bytes)

        # Validar biometria
        if face_validation.verify_face(current_face_encoding, stored_face_encoding):
            authenticated_user_id = template_obj.user_id
            break

    if authenticated_user_id is None:
        raise HTTPException(status_code=401, detail="Autenticação biométrica falhou.")

    # 3. Gerar token de autenticação
    user = await crud.get_user(db, authenticated_user_id) # Buscar o usuário para o token
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado após autenticação biométrica.")

    access_token = security_auth.create_access_token(
        data={"sub": user.username} # Usar o username para o token
    )
    return {"access_token": access_token, "token_type": "bearer"}