import time
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv()

# this file contains database connection logics

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST_NAME = os.getenv("HOST_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOST_NAME}/{DATABASE_NAME}"  # for SQLite, we need connect_args

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


# For reference only
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="postgres",
#             user="postgres",
#             password="root",
#             cursor_factory=RealDictCursor,
#         )
#         cur = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as errors:
#         print("Connecting to database failed")
#         print("Error: ", errors)
#         time.sleep(3)
