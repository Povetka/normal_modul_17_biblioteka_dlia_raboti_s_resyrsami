from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass  # Для создания категории


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с данными ORM
