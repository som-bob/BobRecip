from db.models import BobRecipeIngredient

def save_recipe_ingredient(session, recipe_id, ingredient_id, amount):
    relationship = BobRecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=ingredient_id,
        amount=amount
    )
    session.add(relationship)
    session.commit()
