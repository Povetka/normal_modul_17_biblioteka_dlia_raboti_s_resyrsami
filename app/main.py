from fastapi import FastAPI
from app.backend.db import engine, Base
from app.routers import category, products

app = FastAPI()

# Подключаем роутеры
app.include_router(category.router)
app.include_router(products.router)

# Создаём таблицы в базе данных
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """Главная страница"""
    return {"message": "Welcome to the Shop API"}

# uvicorn app.main:app --reload
