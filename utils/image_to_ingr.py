import os

from dotenv import load_dotenv

import requests
import base64
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def upload_to_imgbb(img_file):
    image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}&expiration=600"
    payload = {"image": image_base64}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json()["data"]["url"]
        else:
            print("imgbb error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Upload error:", e)
        return None


def extract_ingr_from_image(img_file):
    image_url = upload_to_imgbb(img_file)

    if not image_url:
        return ""

    vision_prompt = (
        "You are an assistant that identifies food items in an image. "
        "Return only the names of the food items present in the image. "
        "Use singular tense (e.g., 'onion' instead of 'onions'). "
        "Do not include quantities, descriptions, or extra words. "
        "Just return a plain, comma-separated list of the food items."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": vision_prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=10,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI error: ", str(e))
        return ""
