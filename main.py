from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from typing import Optional, List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Сайт рецептов",
    description="Описание API на русском",
    version="1.0.0"
)

@app.post("/recipes/", response_model=schemas.RecipeOut)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        steps=recipe.steps,
        cooking_time=recipe.cooking_time,
        author_id=recipe.author_id,
        image=recipe.image
    )

    # Привязка ингредиентов
    if recipe.ingredient_ids:
        ingredients = db.query(models.Ingredient).filter(models.Ingredient.id.in_(recipe.ingredient_ids)).all()
        db_recipe.ingredients = ingredients

    # Привязка категорий
    if recipe.category_ids:
        categories = db.query(models.Category).filter(models.Category.id.in_(recipe.category_ids)).all()
        db_recipe.categories = categories

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.get("/recipes/", response_model=list[schemas.RecipeOut])
def read_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).offset(skip).limit(limit).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
def read_recipe(recipe_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe

@app.put("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe(
    recipe_id: int, updated_recipe: schemas.RecipeCreate, db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    recipe.title = updated_recipe.title
    recipe.description = updated_recipe.description
    db.commit()
    db.refresh(recipe)
    return recipe

@app.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    db.delete(recipe)
    db.commit()
    return {"detail": "Рецепт удалён"}

@app.get("/recipes/search/", response_model=List[schemas.RecipeOut])
def search_recipes(
    title: Optional[str] = Query(None, description="Название рецепта (частичное совпадение)"),
    description: Optional[str] = Query(None, description="Описание (частичное совпадение)"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe)

    if title:
        query = query.filter(models.Recipe.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(models.Recipe.description.ilike(f"%{description}%"))

    return query.all()