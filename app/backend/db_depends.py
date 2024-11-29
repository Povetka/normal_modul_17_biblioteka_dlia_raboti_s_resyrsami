from sqlalchemy.orm import Session
from fastapi import Depends
from app.backend.db import SessionLocal


# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
