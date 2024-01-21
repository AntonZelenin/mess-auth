from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import *

engine = create_engine(f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(engine)
