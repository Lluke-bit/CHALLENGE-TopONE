import face_recognition
import numpy as np

def verify_face(current_encoding: np.ndarray, stored_encoding: np.ndarray) -> bool:
    """Compara o encoding atual com o armazenado para verificar a correspondência."""
    # face_recognition.compare_faces retorna uma lista de booleanos.
    # [True] se corresponder, [False] caso contrário.
    matches = face_recognition.compare_faces([stored_encoding], current_encoding, tolerance=0.6) # Ajuste a tolerância conforme necessário
    return matches[0]

def bytes_to_encoding(data_bytes: bytes) -> np.ndarray:
    """Converte bytes de volta para um encoding NumPy array."""
    return np.frombuffer(data_bytes, dtype=np.float64) # Certifique-se de usar o dtype correto