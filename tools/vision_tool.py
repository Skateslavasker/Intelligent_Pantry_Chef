from langchain.tools import tool
from utils.image_to_ingr import extract_ingr_from_image

@tool
def vision_lookup(image):
    """
    Extract ingredients from an image using a vision API."""
    response = extract_ingr_from_image(image)
    return response if response else "TOOL_ERROR: Vision API failed."


