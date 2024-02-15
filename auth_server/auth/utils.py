"""Module with security operations"""

from datetime import datetime, timedelta

import jwt
import bcrypt

from core.config import settings


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def encode_jwt(
    payload: dict,
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algorithm,
    expire_minutes: int = settings.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algorithm,
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
