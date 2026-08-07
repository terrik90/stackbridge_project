import jwt

from src.config import settings


def encode_jwt(
    payload: dict, key: str = settings.jwt_key, algorithm: str = settings.algoritm
):
    encoded = jwt.encode(payload, key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes, key: str = settings.jwt_key, algorithm: str = settings.algoritm
):
    decoded = jwt.decode(token, key, algorithms=[algorithm])
    return decoded
