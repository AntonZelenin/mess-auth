import uuid
from typing import Optional

from mess_auth.db import session
from mess_auth.models.token import RefreshToken
from mess_auth.models.user import User


def get_user(user_id: str) -> Optional[User]:
    return session.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(username: str) -> Optional[User]:
    return session.query(User).filter(User.username == username).first()


def create_user(username: str, hashed_password: str) -> User:
    user = User(user_id=str(uuid.uuid4()).replace('-', ''), username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()

    return user


def get_refresh_token(user_id: str) -> Optional[str]:
    return session.query(RefreshToken.refresh_token).filter(RefreshToken.user_id == user_id).first()


def create_refresh_token(user_id: str, refresh_token: str) -> RefreshToken:
    token = RefreshToken(user_id=user_id, refresh_token=refresh_token)
    session.add(token)
    session.commit()

    return token


def update_refresh_token(user_id: str, refresh_token: str) -> RefreshToken:
    token = session.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()

    # todo maybe raise error if no token found?
    if token is None:
        token = create_refresh_token(user_id, refresh_token)
        return token

    token.refresh_token = refresh_token
    session.commit()

    return token
