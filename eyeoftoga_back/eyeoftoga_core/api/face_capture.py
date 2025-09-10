import face_recognition
import numpy as np
import io

def get_face_encoding(image_bytes: bytes) -> np.ndarray:
    """Processa bytes de imagem e retorna o encoding facial."""
    # Carregar imagem do stream de bytes
    image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        raise ValueError("Nenhum rosto detectado na imagem.")
    if len(face_encodings) > 1:
        raise ValueError("Mais de um rosto detectado na imagem. Por favor, envie uma imagem com um único rosto.")

    return face_encodings[0] # Retorna o encoding do primeiro (e único) rosto