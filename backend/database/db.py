from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  """
  Creates a database session for each request.
  Automatically closes the session after the request is done.
  """
  db = SessionLocal()
  
  try:
    yield db

  finally:
    db.close()

def create_tables():
  Base.metadata.create_all(bind=engine)