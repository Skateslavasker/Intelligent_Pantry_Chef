import os 
import requests
from dotenv import load_dotenv

load_dotenv()

EDAMAM_API_KEY = os.getenv("EDAMAM_API_KEY")
EDAMAM_API_HOST = os.getenv("EDAMAM_API_HOST")

def clean_ingredients(item):
    parts = item.split("--")[0].split("Env")[0].strip()
    if not any(char.isdigit() for char in parts):
        return None
    return parts 


def fetch_nutrition(ingredients: str):
    url = f"https://{EDAMAM_API_HOST}/api/nutrition-data"

    headers = {
        "X-RapidApi-Key": EDAMAM_API_KEY,
        "X-RapidApi-Host": EDAMAM_API_HOST,
    }

    ingr = [clean_ingredients(i.strip()) for i in ingredients.split("|")]
    ingr = [i for i in ingr if i]

    total = {
        "calories": 0,
        "FAT": 0,
        "PROCNT":0,
        "CHOCDF":0,
        "CHOLE":0,
    }

    for item in ingr:
        params = {
        "ingr": item,
        "nutrition-type": "cooking"
    }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                total["calories"] += data.get("calories", 0)
                total["FAT"] += data.get("totalNutrients", {}).get("FAT", {}).get("quantity", 0)
                total["PROCNT"] += data.get("totalNutrients", {}).get("PROCNT", {}).get("quantity", 0)
                total["CHOCDF"] += data.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0)
                total["CHOLE"] += data.get("totalNutrients", {}).get("CHOLE", {}).get("quantity", 0)
    
        except Exception as e:
            print(f"Nutrition fetch failed for: {item} - {str(e)}")

    return total
    

