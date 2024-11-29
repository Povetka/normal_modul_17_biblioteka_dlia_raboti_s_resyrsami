from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Создаём движок для подключения к базе данных
engine = create_engine("sqlite:///./shop.db", echo=True)  # Путь к базе данных SQLite

# Создаём фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(bind=engine)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()
