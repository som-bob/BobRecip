from db.models import BobRecipe
import re

def extract_cooking_time(cooking_time_str):
    """
    Extract numeric cooking time in minutes from the cooking_time string.
    If no numeric value exists, return -1.

    Args:
        cooking_time_str (str): The input string describing the cooking time.

    Returns:
        int: The numeric cooking time in minutes, or -1 if no numeric value is found.
    """
    # Use regex to find the first sequence of digits
    match = re.search(r'\d+', cooking_time_str)
    if match:
        return int(match.group())  # Return the numeric value as an integer
    return -1  # Return -1 if no digits are found
def save_recipe(session, recipe_data, url):
    """Save recipe data into bob_recipe table."""
    recipe = BobRecipe(
        recipe_name=recipe_data["title"],
        recipe_description=recipe_data["description"],
        servings=recipe_data["servings"],
        cooking_time=extract_cooking_time(recipe_data["cooking_time"]),
        difficulty=recipe_data["difficulty"],
        source=url,
        reg_id="system@system.com"
    )
    session.add(recipe)
    session.commit()
    return recipe.recipe_id
