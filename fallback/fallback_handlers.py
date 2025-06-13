def fallback_recipe(ingredients: str) -> dict:

    base = ingredients.split(",")[0] if ingredients else "vegetables"
    return {
        "title": f"Simple sautéed {base.strip()}",
        "ingredients": [i.strip() for i in ingredients.split(",") if i.strip()],
        "instructions": [
            f"Wash and chop the {base.strip()}.",
            "Heat a pan, add oil.",
            "Sauté the ingredients for 5-7 minutes.",
            "Add salt and spices to taste.",
        ],
    }


def fallback_nutrition() -> dict:
    return {
        "calories": 200,
        "FAT": 10,
        "PROCNT": 5,
        "CHOCDF": 15,
        "CHOLE": 30,
    }


def fallback_vision() -> list:
    return ["onion", "potato", "carrot"]
