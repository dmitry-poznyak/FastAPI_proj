from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import engine

Base = declarative_base()


# Связующая таблица для связи многие-ко-многим между рецептами и ингредиентами
recipe_ingredient_association = Table(
    'recipe_recipe_ingredients',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe_recipe.id')),
    Column('ingredient_id', Integer, ForeignKey('recipe_ingredient.id'))
)

# Связующая таблица для связи многие-ко-многим между рецептами и категориями
recipe_category_association = Table(
    'recipe_recipe_categories',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe_recipe.id')),
    Column('category_id', Integer, ForeignKey('recipe_category.id'))
)

class Recipe(Base):
    __tablename__ = "recipe_recipe"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    author_id = Column(Integer) 
    image = Column(String(100), nullable=True)

    ingredients = relationship(
        "Ingredient",
        secondary=recipe_ingredient_association,
        back_populates="recipes"
    )

    categories = relationship(
        "Category",
        secondary=recipe_category_association,
        back_populates="recipes"
    )


class Ingredient(Base):
    __tablename__ = "recipe_ingredient"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    recipes = relationship(
        "Recipe",
        secondary=recipe_ingredient_association,
        back_populates="ingredients"
    )


class Category(Base):
    __tablename__ = "recipe_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    recipes = relationship(
        "Recipe",
        secondary=recipe_category_association,
        back_populates="categories"
    )


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
