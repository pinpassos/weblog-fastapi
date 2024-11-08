import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Session

load_dotenv()
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")
BASE_URL = (
    f"://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{ENVIRONMENT}:3306/{DATABASE_NAME}"
)
DATABASE_URL = {
    "sync": "mysql+pymysql" + BASE_URL,
    "async": "mysql+aiomysql" + BASE_URL,
}


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    def get_sync_engine(self):
        return create_engine(DATABASE_URL["sync"], echo=True)

    def get_async_engine(self):
        return create_async_engine(DATABASE_URL["async"], echo=True)

    def async_session_maker(self):
        return async_sessionmaker(self.get_async_engine(), expire_on_commit=False)


database_manager = DatabaseManager()


def sync_session():
    sync_engine = database_manager.get_sync_engine()
    with Session(sync_engine) as session:
        yield session


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = database_manager.async_session_maker()
    async with async_session_maker() as session:
        yield session
