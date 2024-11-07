import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = "mysql+pymysql://{}:{}@{}:3306/{}".format(
    DATABASE_USERNAME, DATABASE_PASSWORD, ENVIRONMENT, DATABASE_NAME
)
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
