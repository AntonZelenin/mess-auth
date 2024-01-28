import os

# to get a string like this run:
# openssl rand -hex 32
# todo change this to something more secure
SECRET_KEY = "83eaa7fa1dc94c5f7c5a48f0314ad0d93a33b4c14e8cb7d5c848e999e0b2478e"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14

DB_DRIVER = os.environ.get('DB_DRIVER')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')
