from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class BobRecipe(Base):
    __tablename__ = "bob_recipe"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_name = Column(String(200), nullable=False)
    recipe_description = Column(String(1000))
    servings = Column(String(50))
    source = Column(String(255))
    image_url = Column(String(255))
    reg_date = Column(DateTime, default=datetime.datetime.utcnow)
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    ingredients = relationship("BobRecipeIngredient", back_populates="recipe")

class BobIngredient(Base):
    __tablename__ = "bob_ingredients"

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_name = Column(String(100), nullable=False)
    ingredient_description = Column(String(500))
    image_url = Column(String(255))
    icon_url = Column(String(255))
    storage_method = Column(String(100))
    storage_days = Column(Integer)
    reg_date = Column(DateTime, default=datetime.datetime.utcnow)
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class BobRecipeIngredient(Base):
    __tablename__ = "bob_recipe_ingredients"

    detail_ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("bob_recipe.recipe_id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("bob_ingredients.ingredient_id"), nullable=False)
    amount = Column(String(100))
    reg_date = Column(DateTime, default=datetime.datetime.utcnow)
    mod_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    recipe = relationship("BobRecipe", back_populates="ingredients")
    ingredient = relationship("BobIngredient")
