from db.models import BobIngredient

def save_ingredient(session, ingredient_data):
    ingredient_data_name_ = ingredient_data["name"]
    existing = session.query(BobIngredient).filter_by(name=ingredient_data_name_).first()
    if existing:
        return existing.ingredient_id

    ingredient = BobIngredient(
        ingredient_name=ingredient_data_name_,
        ingredient_description=ingredient_data.get("description", ""),
        image_url=ingredient_data.get("image_url", ""),
        icon_url=ingredient_data.get("icon_url", ""),
        storage_method=ingredient_data.get("storage_method", ""),
        storage_days=ingredient_data.get("storage_days", None),
    )
    session.add(ingredient)
    session.commit()
    return ingredient.ingredient_id
