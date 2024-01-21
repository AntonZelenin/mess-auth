from datetime import timedelta, timezone, datetime

from jose import jwt
from passlib.context import CryptContext

from mess_auth import constants

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def is_valid_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta

    return jwt.encode(to_encode, constants.SECRET_KEY, algorithm=constants.ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, constants.SECRET_KEY, algorithms=[constants.ALGORITHM])
