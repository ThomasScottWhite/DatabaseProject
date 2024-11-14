from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal  # Import SessionLocal for database session
from models import *         # Import all models if needed

from routes import member         # Import all routes if needed
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
