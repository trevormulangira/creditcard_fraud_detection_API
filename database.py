from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

Base = declarative_base()  # Create a base class for declarative models
DATABASE_URL = os.getenv("DATABASE_URL")  # Get the database URL from environment variables

engine = create_engine(DATABASE_URL)  # Create a SQLAlchemy engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to be used in the request
    finally:
        db.close()  # Close the session after the request is done

from sqlalchemy import text
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())  