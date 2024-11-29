from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    slug: str
    category_id: int


class ProductCreate(ProductBase):
    pass  # Для создания продукта


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с данными ORM
