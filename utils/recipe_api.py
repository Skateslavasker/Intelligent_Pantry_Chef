import os
import requests
from dotenv import load_dotenv

load_dotenv()


NINJAS_RECIPE_API_KEY = os.getenv("NINJAS_RECIPE_API_KEY")
NINJAS_API_HOST = "recipe-by-api-ninjas.p.rapidapi.com"


def fetch_recipe(query: str):
    url = f"https://{NINJAS_API_HOST}/v1/recipe"

    headers = {
        "x-rapidapi-host": NINJAS_API_HOST,
        "x-rapidapi-key": NINJAS_RECIPE_API_KEY,
    }

    params = {
        "query": query,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching recipe: {response.status_code} - {response.text}")
        return []
