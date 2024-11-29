from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import Annotated
from app.schemas.category import Category, CategoryCreate
from app.backend.db_depends import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

# Сессия для работы с базой данных через FastAPI и SQLAlchemy
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[Category])
def get_all_categories(db: DbSession):
    """Получить список всех категорий через execute"""
    query = text("SELECT * FROM categories")
    result = db.execute(query).fetchall()
    return [Category(id=row.id, name=row.name, slug=row.slug) for row in result]


@router.post("/create", response_model=Category)
def create_category(category: CategoryCreate, db: DbSession):
    """Создать новую категорию"""
    query = text("INSERT INTO categories (name, slug) VALUES (:name, :slug)")
    db.execute(query, {"name": category.name, "slug": category.slug})
    db.commit()
    # Возвращаем созданную категорию
    select_query = text("SELECT * FROM categories WHERE name = :name")
    result = db.execute(select_query, {"name": category.name}).fetchone()
    return Category(id=result.id, name=result.name, slug=result.slug)


@router.put("/update", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: DbSession):
    """Обновить категорию"""
    select_query = text("SELECT * FROM categories WHERE id = :id")
    result = db.execute(select_query, {"id": category_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")

    update_query = text(
        "UPDATE categories SET name = :name, slug = :slug WHERE id = :id"
    )
    db.execute(
        update_query,
        {"id": category_id, "name": category.name, "slug": category.slug},
    )
    db.commit()

    # Возвращаем обновлённую категорию
    updated_result = db.execute(select_query, {"id": category_id}).fetchone()
    return Category(id=updated_result.id, name=updated_result.name, slug=updated_result.slug)


@router.delete("/delete/{category_id}")
def delete_category(category_id: int, db: DbSession):
    """Удалить категорию"""
    select_query = text("SELECT * FROM categories WHERE id = :id")
    result = db.execute(select_query, {"id": category_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")

    delete_query = text("DELETE FROM categories WHERE id = :id")
    db.execute(delete_query, {"id": category_id})
    db.commit()
    return {"message": "Category deleted"}
