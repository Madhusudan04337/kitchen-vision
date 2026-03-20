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


def _normalise_ingredient(ing) -> str:
    """
    Flatten an ingredient entry to a plain readable string.

    Gemini sometimes returns dicts like:
        {"item": "salmon fillet", "quantity": "1 (approx. 6 oz)"}
    instead of plain strings. This helper handles both forms.
    """
    if isinstance(ing, dict):
        item     = ing.get("item", ing.get("name", ""))
        quantity = ing.get("quantity", ing.get("amount", ""))
        if quantity:
            return f"{quantity} {item}".strip()
        return item.strip()
    return str(ing).strip()


def generate_recipes(ingredients: list[str]) -> list[dict]:
    """
    Generate 3 beginner-friendly recipes from the given ingredients.

    Args:
        ingredients: List of ingredient name strings.

    Returns:
        List of recipe dicts, each with keys:
            name        (str)
            ingredients (list[str])   — always plain strings after normalisation
            steps       (list[str])
            time        (str)
            difficulty  (str)

    Raises:
        RuntimeError: If the Gemini API call or JSON parsing fails.
    """
    ingredient_list = ", ".join(ingredients)

    prompt = f"""
    You are a friendly recipe assistant. Using ONLY these ingredients (plus basic pantry staples like salt, pepper, oil, water):

    {ingredient_list}

    Generate exactly 3 beginner-friendly recipes.

    IMPORTANT RULES FOR JSON FORMAT:
    - "ingredients" must be a plain list of strings like "2 cups spinach" — NOT objects or dicts
    - "steps" must be a plain list of strings — NOT objects
    - No markdown, no extra text outside the JSON array

    Respond ONLY with a valid JSON array in this exact format:
    [
      {{
        "name": "Recipe Name",
        "ingredients": ["2 cups spinach", "1 salmon fillet", "1 tbsp olive oil"],
        "steps": ["Step 1 description.", "Step 2 description.", "Step 3 description."],
        "time": "20 minutes",
        "difficulty": "Easy"
      }}
    ]
    """

    try:
        logger.info(f"Generating recipes for ingredients: {ingredients}")
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        recipes = json.loads(raw)

        # Normalise ingredient entries — flatten any dicts to plain strings
        for recipe in recipes:
            recipe["ingredients"] = [
                _normalise_ingredient(ing)
                for ing in recipe.get("ingredients", [])
            ]

        logger.info(f"Successfully parsed {len(recipes)} recipes.")
        return recipes

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e} — raw response: {raw}")
        raise RuntimeError("Failed to parse recipe response from AI.") from e

    except Exception as e:
        logger.error(f"Recipe generation failed: {e}")
        raise RuntimeError(f"Recipe generation failed: {e}") from e

