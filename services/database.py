from os import environ
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

database_url = URL.create(drivername="postgresql+psycopg", username="postgres",
                          password=environ["CATALOG_DB_PASSWORD"], host="127.0.0.1", port=5433, database="catalog")

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    with SessionLocal() as session:
        yield session
