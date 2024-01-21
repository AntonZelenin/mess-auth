from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from mess_auth import repository, schemas
from mess_auth.models.user import User

# to get a string like this run:
# openssl rand -hex 32
# todo change this to something more secure
SECRET_KEY = "83eaa7fa1dc94c5f7c5a48f0314ad0d93a33b4c14e8cb7d5c848e999e0b2478e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

app = FastAPI()


class Token(BaseModel):
    access_token: str
    token_type: str


def is_valid_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate(username: str, password: str) -> Optional[User]:
    user = repository.get_user_by_username(username)
    if user and is_valid_password(password, user.hashed_password):
        return user

    return None


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = repository.get_user(user_id)
    if user is None:
        raise credentials_exception

    return user


@app.post("/api/v1/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")


@app.post("/api/v1/users")
async def create_user(user: schemas.User):
    repository.create_user(user.username, get_password_hash(user.password))

    return {"message": "User created successfully"}


@app.get("/api/v1/users/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
