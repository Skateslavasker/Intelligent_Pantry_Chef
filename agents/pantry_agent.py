from tools.recipe_tool import recipe_lookup
from tools.llm_tool import llm_lookup
from fallback.fallback_handlers import fallback_recipe
from schemas.recipe_schema import RecipeOutput
import json


def normalize_recipe_api_format(recipe: dict) -> dict:
    return {
        "title": recipe.get("title", "Untitled Recipe"),
        "ingredients": [
            i.strip() for i in recipe.get("ingredients", "").split("|")
            if i.strip()
        ],
        "instructions": (
            [recipe.get("instructions", "").strip()]
            if isinstance(recipe.get("instructions"), str)
            else recipe.get("instructions", [])
        ),
    }


def run_pantry_agent(ingredients: str) -> dict:
    try:
        result = recipe_lookup.run(ingredients)
        if "TOOL_ERROR" not in result:
            raw = json.loads(result) if isinstance(result, str) else result
            recipe = normalize_recipe_api_format(raw)
            return RecipeOutput.model_validate(recipe).model_dump()
        result = llm_lookup.run({"ingr": ingredients.split(", ")})
        if "TOOL_ERROR" not in result:
            raw = json.loads(result) if isinstance(result, str) else result
            return RecipeOutput.model_validate(raw).model_dump()
        return fallback_recipe(ingredients)
    except Exception as e:
        print("Agent Failed: ", str(e))
        return fallback_recipe(ingredients)
