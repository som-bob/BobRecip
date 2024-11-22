from db.models import BobRecipe

def save_recipe(session, recipe_data, url):
    recipe = BobRecipe(
        recipe_name=recipe_data["title"],
        recipe_description=recipe_data.get("description", ""),
        servings=recipe_data.get("servings", ""),
        source=url,
        image_url=recipe_data.get("image_url", "")
    )
    session.add(recipe)
    session.commit()
    return recipe.recipe_id
