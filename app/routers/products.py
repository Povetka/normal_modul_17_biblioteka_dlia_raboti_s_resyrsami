from fastapi import APIRouter, HTTPException
from app.schemas.products import Product, ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
# Фейковые данные
products = [
    {"id": 1, "name": "Laptop", "slug": "laptop", "category_id": 1},
    {"id": 2, "name": "Book", "slug": "book", "category_id": 2},
]


@router.get("/", response_model=list[Product])
def get_all_products():
    """Получить список всех продуктов"""
    return products


@router.post("/", response_model=Product)
def create_product(product: ProductCreate):
    """Создать продукт"""
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "slug": product.slug,
        "category_id": product.category_id,
    }
    products.append(new_product)
    return new_product


@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    """Обновить продукт"""
    for prod in products:
        if prod["id"] == product_id:
            prod["name"] = product.name
            prod["slug"] = product.slug  # Обновляем slug
            prod["category_id"] = product.category_id
            return prod
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{product_id}")
def delete_product(product_id: int):
    """Удалить продукт"""
    global products
    products = [prod for prod in products if prod["id"] != product_id]
    return {"message": "Product deleted"}
