from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import Annotated
from app.schemas.products import Product, ProductCreate
from app.backend.db_depends import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[Product])
def get_all_products(db: DbSession):
    """Получить список всех продуктов через execute"""
    query = text("SELECT * FROM products")
    result = db.execute(query).fetchall()
    return [
        Product(
            id=row.id,
            name=row.name,
            slug=row.slug,
            category_id=row.category_id,
        )
        for row in result
    ]


@router.post("/create", response_model=Product)
def create_product(product: ProductCreate, db: DbSession):
    """Создать продукт"""
    query = text(
        "INSERT INTO products (name, slug, category_id) VALUES (:name, :slug, :category_id)"
    )
    db.execute(
        query,
        {
            "name": product.name,
            "slug": product.slug,
            "category_id": product.category_id,
        },
    )
    db.commit()

    # Возвращаем созданный продукт
    select_query = text("SELECT * FROM products WHERE name = :name AND slug = :slug")
    result = db.execute(
        select_query, {"name": product.name, "slug": product.slug}
    ).fetchone()
    return Product(
        id=result.id,
        name=result.name,
        slug=result.slug,
        category_id=result.category_id,
    )


@router.put("/update", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: DbSession):
    """Обновить продукт"""
    select_query = text("SELECT * FROM products WHERE id = :id")
    result = db.execute(select_query, {"id": product_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    update_query = text(
        "UPDATE products SET name = :name, slug = :slug, category_id = :category_id WHERE id = :id"
    )
    db.execute(
        update_query,
        {
            "id": product_id,
            "name": product.name,
            "slug": product.slug,
            "category_id": product.category_id,
        },
    )
    db.commit()

    # Возвращаем обновлённый продукт
    updated_result = db.execute(select_query, {"id": product_id}).fetchone()
    return Product(
        id=updated_result.id,
        name=updated_result.name,
        slug=updated_result.slug,
        category_id=updated_result.category_id,
    )


@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: DbSession):
    """Удалить продукт"""
    select_query = text("SELECT * FROM products WHERE id = :id")
    result = db.execute(select_query, {"id": product_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_query = text("DELETE FROM products WHERE id = :id")
    db.execute(delete_query, {"id": product_id})
    db.commit()
    return {"message": "Product deleted"}
