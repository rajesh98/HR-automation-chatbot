from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from .config import settings
import urllib.parse
from langchain_community.utilities.sql_database import SQLDatabase
import os
from dotenv import load_dotenv
import urllib.parse

from sqlalchemy import URL



# Load environment variables from .env file
load_dotenv()
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
#DB_PORT = os.getenv("DB_PORT")
db_port = 5102
#print(db_password)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=1,include_tables=['customers','orders'],custom_table_info={'customers':"customer"})
#db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
import urllib.parse

url_object = URL.create(
    "postgresql+psycopg2",
    username=db_user,
    password=db_password,  # plain (unescaped) text
    host=db_host,
    database=db_name,
    port=5102, # Optional: specify port if needed
    # query={"key": "value"} # Optional: for driver-specific parameters
)


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_user}:{urllib.parse.quote_plus(db_password)}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
db = SQLDatabase.from_uri(url_object)
#engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=20)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_for_login():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



""" SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.database_username}:{urllib.parse.quote_plus(settings.database_password)}@{settings.database_hostname}/{settings.database_name}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() """

def get_db():
    return db

		