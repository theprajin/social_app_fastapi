from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#this file contains database connection logics

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/fastapicourse'  # for SQLite, we need connect_args

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# postgresql://<username>:<password>@<ip-address/hostname>/database_name
