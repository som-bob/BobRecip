from db.models import BobRecipeDetailIngredient
from services.save_ingredients import save_ingredient

def save_recipe_detail_ingredients(session, recipe_detail_id, ingredient_list):
    """Save ingredients for a specific recipe step into bob_recipe_detail_ingredient table."""
    for ingredient_name in ingredient_list:
        ingredient_id = save_ingredient(session, ingredient_name)
        detail_ingredient = BobRecipeDetailIngredient(
            recipe_detail_id=recipe_detail_id,
            ingredient_id=ingredient_id,
            reg_id="system@system.com"
        )
        session.add(detail_ingredient)
    session.commit()
