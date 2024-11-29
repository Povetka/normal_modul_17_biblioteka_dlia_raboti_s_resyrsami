from fastapi import FastAPI
from app.routers import category, products

app = FastAPI()

# Подключаем маршруты
app.include_router(category.router)
app.include_router(products.router)


@app.get("/")
def root():
    """Главная страница"""
    return {"message": "Welcome to the Shop API"}

# uvicorn app.main:app --reload
