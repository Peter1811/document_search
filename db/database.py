import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv('.env_database', override=True)
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')

DATABASE_URL = f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}'

engine = create_async_engine(url=DATABASE_URL)
session = async_sessionmaker(bind=engine)

async def get_db():
    async with session() as db:
        yield db
