import uuid
from typing import Optional

from mess_auth.db import Session
from mess_auth.models.user import User


def get_user(user_id: str) -> Optional[User]:
    with Session() as session:
        return session.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(username: str) -> Optional[User]:
    with Session() as session:
        return session.query(User).filter(User.username == username).first()


def create_user(username: str, hashed_password: str) -> User:
    with Session.begin() as session:
        user = User(user_id=str(uuid.uuid4()).replace('-', ''), username=username, hashed_password=hashed_password)
        session.add(user)
        session.commit()

    return user
