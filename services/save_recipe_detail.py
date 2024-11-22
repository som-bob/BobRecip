from db.models import BobRecipeDetail

def save_recipe_details(session, recipe_id, steps):
    """Save recipe steps into bob_recipe_detail table."""
    recipe_details = []
    for step_data in steps:
        recipe_detail = BobRecipeDetail(
            recipe_id=recipe_id,
            image_url=step_data.get("image_url"),
            recipe_order=step_data["step_number"],
            recipe_detail_text=step_data["description"],
            reg_id="system@system.com"
        )
        session.add(recipe_detail)
        session.commit()  # Commit after adding detail to get the detail_id
        recipe_details.append((recipe_detail.recipe_detail_id, step_data["ingredient_list"]))
    return recipe_details
