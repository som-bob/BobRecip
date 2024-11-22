from db.models import BobIngredient

def save_ingredient(session, ingredient_name):
    """Check if ingredient exists, if not, save it and return its ID."""
    ingredient = session.query(BobIngredient).filter(BobIngredient.name == ingredient_name).first()
    if not ingredient:
        ingredient = BobIngredient(name=ingredient_name)
        session.add(ingredient)
        session.commit()
    return ingredient.ingredient_id
