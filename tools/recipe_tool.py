from langchain.tools import tool
from utils.recipe_api import fetch_recipe


@tool
def recipe_lookup(ingredients: str) -> str:
    """
    Fetch a recipe based on the provided ingredients."""
    result = fetch_recipe(ingredients)
    return result[0] if result else "TOOL_ERROR: Recipe API failed."
