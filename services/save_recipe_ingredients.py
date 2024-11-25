from db.models import BobRecipeIngredient
from services.save_ingredients import save_ingredient

def save_recipe_ingredients(session, recipe_id, ingredients):
    """Save recipe ingredients into bob_recipe_ingredients table."""
    for ingredient_data in ingredients:
        ingredient_id = save_ingredient(session, ingredient_data["name"])
        volume_ = ingredient_data["volume"]
        recipe_ingredient = BobRecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            amount=volume_,
            reg_id="system@system.com"
        )
        session.add(recipe_ingredient)
    session.commit()
