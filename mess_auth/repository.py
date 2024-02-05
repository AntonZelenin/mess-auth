from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mess_auth.models.token import RefreshToken
from mess_auth.models.user import User


async def get_user(session: AsyncSession, user_id: str) -> Optional[User]:
    return (await session.scalars(select(User).filter(User.user_id == user_id))).first()


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    return (await session.scalars(select(User).filter(User.username == username))).first()


async def create_user(session: AsyncSession, user_id: str, username: str, hashed_password: str) -> User:
    user = User(user_id=user_id, username=username, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def get_refresh_token(session: AsyncSession, user_id: str) -> Optional[str]:
    return (await session.scalars(select(RefreshToken.refresh_token).filter(RefreshToken.user_id == user_id))).first()


async def create_refresh_token(session: AsyncSession, user_id: str, refresh_token: str) -> RefreshToken:
    token = RefreshToken(user_id=user_id, token=refresh_token)
    session.add(token)
    await session.commit()
    await session.refresh(token)

    return token


# todo if multiple devices are used they'll break each other tokens
async def update_refresh_token(session: AsyncSession, user_id: str, refresh_token: str) -> RefreshToken:
    token = (await session.scalars(select(RefreshToken).filter(RefreshToken.user_id == user_id))).first()

    if token is None:
        return await create_refresh_token(session, user_id, refresh_token)

    token.refresh_token = refresh_token
    await session.commit()
    await session.refresh(token)

    return token
