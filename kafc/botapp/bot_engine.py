from . import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.DATABASE_URI)

Session = sessionmaker(bind=engine)
db = Session()
