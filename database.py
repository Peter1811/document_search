import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv('.env_database', override=True)
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')

DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(url=DATABASE_URL)

session = sessionmaker(bind=engine)
