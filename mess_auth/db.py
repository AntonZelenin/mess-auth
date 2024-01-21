from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mess_auth.constants import *

# engine = create_engine(f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
engine = create_engine(f'sqlite:///mess-auth.db')
Session = sessionmaker(engine)
