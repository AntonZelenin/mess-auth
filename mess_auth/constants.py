import os

ROOT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
)
ENV_FILE = os.path.join(ROOT_DIR, os.environ.get('ENV_FILE', 'dev.env'))

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14
