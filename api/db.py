from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base  # Import Base from models/base.py

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables if they don't exist


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
