from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base


class Product(Base):
    __tablename__ = "products"  # Имя таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор
    name = Column(String, index=True)  # Название продукта
    slug = Column(String, unique=True, index=True)  # Человекочитаемый URL
    category_id = Column(Integer, ForeignKey("categories.id"))  # Связь с Category
    # Определяем отношение "многие к одному"
    category = relationship("Category", back_populates="products")
