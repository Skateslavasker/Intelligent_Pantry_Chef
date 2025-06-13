from together import Together
from dotenv import load_dotenv

import os

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


def generate_recipe(ingr: list[str]) -> str:
    prompt = (
        "You are a professional recipe generator AI.\n"
        f"Based only on the following ingredients: {', '.join(ingr)}.\n\n"
        "Return the following in JSON format:\n\n"
        "{\n"
        '  "title": "Recipe Title",\n'
        '  "ingredients": ["ingredient 1", "ingredient 2", ...],\n'
        '  "instructions": ["Step 1", "Step 2", ...]\n'
        "}\n\n"
        "Do NOT include nutritional info. Do not add any extra commentary. Only return the JSON object."
    )

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "system", "content": "You generate recipes from ingredients."},
            {"role": "user", "content": prompt},
        ],
        json_mode=True,
    )

    return response.choices[0].message.content
