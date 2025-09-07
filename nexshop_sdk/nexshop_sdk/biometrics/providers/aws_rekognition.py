import boto3
from botocore.exceptions import ClientError
import os

# Configure seu cliente boto3 (melhor usar variáveis de ambiente ou secrets manager)
rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def register_face_rekognition(image_bytes: bytes, collection_id: str, user_id: str) -> str:
    """Registra uma face no AWS Rekognition."""
    try:
        response = rekognition_client.index_faces(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            ExternalImageId=user_id, # ID que você associa ao seu usuário
            MaxFaces=1,
            QualityFilter="AUTO"
        )
        if response['FaceRecords']:
            face_id = response['FaceRecords'][0]['Face']['FaceId']
            print(f"Face registrada com FaceId: {face_id}")
            return face_id
        else:
            raise ValueError("Nenhum rosto detectado ou indexado pelo Rekognition.")
    except ClientError as e:
        raise Exception(f"Erro ao registrar face no Rekognition: {e}")

def search_face_rekognition(image_bytes: bytes, collection_id: str) -> str | None:
    """Busca uma face correspondente em uma coleção do AWS Rekognition."""
    try:
        response = rekognition_client.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=80 # Limite de similaridade, ajuste conforme necessário
        )
        if response['FaceMatches']:
            # Retorna o ExternalImageId do rosto correspondente
            return response['FaceMatches'][0]['Face']['ExternalImageId']
        else:
            return None # Nenhuma correspondência encontrada
    except ClientError as e:
        raise Exception(f"Erro ao buscar face no Rekognition: {e}")
