import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from mess_auth import constants


class Settings(BaseSettings):
    database_url: str
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str

    def __init__(self):
        if os.environ.get('ENVIRONMENT', 'dev') == 'dev':
            Settings.model_config = SettingsConfigDict(env_file=constants.ENV_FILE)

        super().__init__()


@lru_cache
def get_settings():
    return Settings()
