from huggingface_hub import InferenceClient
import os 

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

client = InferenceClient(token=HF_API_TOKEN)

def generate_recipe(ingr: list[str]) -> str:
    prompt = (
        "You are a professional recipe generator AI.\n"
        f"Based only on the following ingredients: {', '.join(ingr)}.\n\n"
        "Generate:\n"
        "- Title\n"
        "- Ingredients: (as comma-separated list)\n"
        "- Instructions: step-by-step numbered.\n\n"
        "Do NOT include nutritional info."
    )

    response = client.text_generation(
        model="mistralai/Mixtral-8x7B-v0.1",
        prompt=prompt,
        max_new_tokens=600,
        temperature=0.7,
    )

    return response