import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise EnvironmentError("GEMINI_API_KEY is not set. Add it to your .env file.")

# Configure Gemini API
genai.configure(api_key=_api_key)

# Initialize model
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

    # Clean return — no code after return statement

    prompt = """
    You are a kitchen assistant. Carefully examine this pantry/food image.
    Identify every visible food ingredient.
    Return ONLY a comma-separated list of ingredient names, nothing else.
    Example: apple, onion, olive oil, pasta
    """

    try:
        response = model.generate_content([prompt, image])
        raw_text = response.text.strip()

        ingredients = [
            item.strip().lower()
            for item in raw_text.split(",")
            if item.strip()
        ]

        return ingredients

    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")