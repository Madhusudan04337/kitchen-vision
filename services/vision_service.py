import google.generativeai as genai
import os
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

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

    try:
        logger.info("Calling Gemini vision model for ingredient detection.")
        response = model.generate_content([prompt, image])
        raw_text = response.text.strip()
        logger.info(f"Raw Gemini response: {raw_text}")

        ingredients = [
            item.strip().lower()
            for item in raw_text.split(",")
            if item.strip()
        ]

        logger.info(f"Detected {len(ingredients)} ingredients: {ingredients}")
        return ingredients

    except Exception as e:
        logger.error(f"Gemini vision call failed: {e}")
        raise RuntimeError(f"Ingredient detection failed: {e}") from e