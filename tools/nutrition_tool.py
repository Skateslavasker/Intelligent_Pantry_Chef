from langchain.tools import tool
from utils.nutrition_api import fetch_nutrition


@tool
def nutrition_lookup(ingredients: str):
    """
    Fetch nutrition information based on the provided ingredients."""
    result = fetch_nutrition(ingredients)
    return result if result else "TOOL_ERROR: Nutrition API failed."

