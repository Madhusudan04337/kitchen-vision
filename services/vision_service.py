import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise EnvironmentError("GEMINI_API_KEY is not set. Add it to your .env file.")

genai.configure(api_key=_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def detect_ingredients(image) -> list[str]:
    """
    Analyse a PIL image and return a list of detected food ingredients.

    Args:
        image: PIL.Image object from the uploaded file.

    Returns:
        List of ingredient name strings.

    Raises:
        RuntimeError: If the Gemini API call fails.
    """
    prompt = """
    You are a kitchen assistant. Carefully examine this pantry/food image.
    Identify every visible food ingredient.
    Return ONLY a comma-separated list of ingredient names, nothing else.
    Example: apple, onion, olive oil, pasta
    """

    response = model.generate_content([prompt, image])
    raw_text = response.text.strip()

    ingredients = [
        item.strip().lower()
        for item in raw_text.split(",")
        if item.strip()
    ]

    return ingredients