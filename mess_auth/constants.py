import os

ROOT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
)
DEV_ENV_FILE = os.path.join(ROOT_DIR, 'dev.env')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14
