from utils.logger import get_logger

logger = get_logger(__name__)

_SUBSTITUTIONS: dict[str, str] = {
    # Dairy
    "milk":            "oat milk or almond milk",
    "butter":          "olive oil or coconut oil",
    "cream":           "coconut cream or cashew cream",
    "cream cheese":    "blended silken tofu",
    "sour cream":      "plain Greek yogurt",
    "parmesan":        "nutritional yeast (vegan) or pecorino",
    # Eggs
    "egg":             "1 tbsp flaxseed + 3 tbsp water (flax egg)",
    "eggs":            "1 tbsp flaxseed + 3 tbsp water per egg",
    # Sweeteners
    "sugar":           "honey, maple syrup, or coconut sugar",
    "white sugar":     "coconut sugar or raw cane sugar",
    "honey":           "maple syrup or agave nectar",
    # Flour
    "all-purpose flour": "whole wheat flour or oat flour",
    "white flour":     "whole wheat flour (use 7/8 cup per 1 cup)",
    # Oils
    "vegetable oil":   "avocado oil or light olive oil",
    "canola oil":      "avocado oil",
    # Proteins
    "chicken":         "tofu, tempeh, or chickpeas",
    "beef":            "lentils or mushrooms (texture match)",
    "pork":            "turkey or jackfruit",
    # Misc
    "breadcrumbs":     "crushed oats or almond flour",
    "soy sauce":       "coconut aminos (gluten-free option)",
    "mayonnaise":      "plain Greek yogurt or avocado mash",
    "pasta":           "zucchini noodles or whole wheat pasta",
    "white rice":      "brown rice, quinoa, or cauliflower rice",
}


def suggest_substitutions(ingredients: list[str]) -> dict[str, str]:
    """
    Return a dict mapping any ingredient that has a known substitution
    to its healthier / dietary-friendly alternative.
    """
    suggestions: dict[str, str] = {}

    for item in ingredients:
        key = item.lower().strip()
        if key in _SUBSTITUTIONS:
            suggestions[item] = _SUBSTITUTIONS[key]
            logger.info(f"Substitution found: {item} → {_SUBSTITUTIONS[key]}")

    logger.info(f"{len(suggestions)} substitution(s) found out of {len(ingredients)} ingredients.")
    return suggestions