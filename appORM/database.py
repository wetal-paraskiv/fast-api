'''
ORM method for creating a new postgreSQL table
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from appORM.config import settings as set


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgrespass@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{set.database_user}:{set.database_password}@{set.database_hostname}:{set.database_port}/{set.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
