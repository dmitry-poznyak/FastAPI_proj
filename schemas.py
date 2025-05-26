from pydantic import BaseModel
from typing import Optional, List

class RecipeBase(BaseModel):
    title: str
    description: str
    steps: str
    cooking_time: int
    author_id: Optional[int] = None
    image: Optional[str] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int

    class Config:
        orm_mode = True

