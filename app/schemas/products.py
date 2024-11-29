from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    category_id: int
