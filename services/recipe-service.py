import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise EnvironmentError("GEMINI_API_KEY is not set. Add it to your .env file.")

genai.configure(api_key=_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_recipes(ingredients: list[str]) -> list[dict]:
    """
    Generate 3 beginner-friendly recipes from the given ingredients.

    Returns:
        List of recipe dicts with keys: name, ingredients, steps, time, difficulty

    Raises:
        RuntimeError: If the Gemini API call or JSON parsing fails.
    """
    ingredient_list = ", ".join(ingredients)

    prompt = f"""
    You are a friendly recipe assistant. Using ONLY these ingredients
    (plus basic pantry staples like salt, pepper, oil, water):

    {ingredient_list}

    Generate exactly 3 beginner-friendly recipes.

    Respond ONLY with a valid JSON array in this exact format:
    [
      {{
        "name": "Recipe Name",
        "ingredients": ["2 cups spinach", "1 salmon fillet"],
        "steps": ["Step 1.", "Step 2.", "Step 3."],
        "time": "20 minutes",
        "difficulty": "Easy"
      }}
    ]
    """

    try:
        logger.info(f"Generating recipes for ingredients: {ingredients}")
        response = model.generate_content(prompt)
        raw = response.text.strip()
        recipes = json.loads(raw)
        logger.info(f"Successfully parsed {len(recipes)} recipes.")
        return recipes

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise RuntimeError("Failed to parse recipe response from AI.") from e

    except Exception as e:
        logger.error(f"Recipe generation failed: {e}")
        raise RuntimeError(f"Recipe generation failed: {e}") from e

