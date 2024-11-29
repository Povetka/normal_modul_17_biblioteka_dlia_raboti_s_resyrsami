from fastapi import APIRouter, HTTPException
from app.schemas.category import Category, CategoryCreate

router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)
# фейковые данные
categories = [{'id': 1, 'name': 'Electonics'}, {'id': 2, 'name': 'Books'}]


@router.get('/', response_model=list[Category])
def get_all_categories():
    """Получить все категории"""
    return categories


@router.post("/", response_model=Category)
def create_category(category: CategoryCreate):
    """Создать новую категорию"""
    new_category = {"id": len(categories) + 1, "name": category.name}
    categories.append(new_category)
    return new_category


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate):
    """Обновить категорию"""
    for cat in categories:
        if cat["id"] == category_id:
            cat["name"] = category.name
            return cat
    raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{category_id}")
def delete_category(category_id: int):
    """Удалить категорию"""
    global categories
    categories = [cat for cat in categories if cat["id"] != category_id]
    return {"message": "Category deleted"}
