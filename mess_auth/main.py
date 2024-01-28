from collections import defaultdict
from datetime import timedelta
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel
from starlette.responses import JSONResponse

from mess_auth import repository, schemas, utils, constants
from mess_auth.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

app = FastAPI()


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


def authenticate_by_creds(username: str, password: str) -> Optional[User]:
    user = repository.get_user_by_username(username)
    if user and utils.is_valid_password(password, user.hashed_password):
        return user

    return None


@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(_, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"errors": reformatted_message}
        ),
    )


@app.get("/api/v1/authorize")
async def authenticate_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = utils.decode_access_token(token)
    except JWTError:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = repository.get_user(user_id)
    if user is None:
        raise credentials_exception

    return payload


@app.post("/api/v1/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_by_creds(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = utils.create_jwt(
        data={"sub": user.user_id},
        expires_delta=timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = utils.create_jwt(
        data={"sub": user.user_id},
        expires_delta=timedelta(minutes=constants.REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@app.post("/api/v1/users")
async def create_user(user: schemas.User):
    if repository.get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    repository.create_user(user.username, utils.get_password_hash(user.password))

    return {"message": "User created successfully"}
