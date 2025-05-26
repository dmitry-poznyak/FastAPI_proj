from pydantic import BaseModel
from typing import Optional, List


# ===== СХЕМЫ ДЛЯ ИНГРЕДИЕНТОВ =====
class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    pass

class IngredientOut(IngredientBase):
    id: int

    class Config:
        orm_mode = True


# ===== СХЕМЫ ДЛЯ КАТЕГОРИЙ =====
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# ===== СХЕМЫ ДЛЯ РЕЦЕПТОВ =====
class RecipeBase(BaseModel):
    title: str
    description: str
    steps: str
    cooking_time: int
    author_id: Optional[int] = None
    image: Optional[str] = None

class RecipeCreate(RecipeBase):
    ingredient_ids: List[int] = []
    category_ids: List[int] = []

class RecipeOut(RecipeBase):
    id: int
    ingredients: List[IngredientOut] = []
    categories: List[CategoryOut] = []

    class Config:
        orm_mode = True
