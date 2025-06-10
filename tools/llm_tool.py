from langchain.tools import tool 
from utils.generate_recipe import generate_recipe

@tool
def llm_lookup(ingr: list[str]) -> str:
    """
    Generate a recipe based on the provided ingredients using an LLM."""
    response = generate_recipe(ingr)
    return response if response else "TOOL_ERROR: LLM API failed."