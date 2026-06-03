# app/security.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

# Используем bcrypt_sha256 – сначала SHA-256, затем bcrypt
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Остальной код для JWT (create_access_token и т.д.)

# def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
#     """
#     Создает JWT-токен. В 'data' обязательно должно быть поле 'sub' (subject),
#     которое обычно содержит идентификатор пользователя.
#     """
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt