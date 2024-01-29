from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from mess_auth import constants


class Settings(BaseSettings):
    database_url: str
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str

    model_config = SettingsConfigDict(env_file=constants.ENV_FILE)


@lru_cache
def get_settings():
    return Settings()
