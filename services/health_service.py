from utils.logger import get_logger

logger = get_logger(__name__)

# ── Ingredient classification sets ────────────────────────────────────────────
_SUPERFOODS = {
    "spinach", "kale", "broccoli", "avocado", "blueberry", "blueberries",
    "salmon", "quinoa", "chia seeds", "flaxseed", "turmeric", "ginger",
    "garlic", "walnuts", "almonds", "sweet potato"
}

_FRESH_PRODUCE = {
    "tomato", "tomatoes", "cherry tomatoes", "onion", "red onion",
    "carrot", "carrots", "potato", "potatoes", "bell pepper",
    "green bell pepper", "red bell pepper", "cucumber", "lettuce",
    "celery", "zucchini", "mushroom", "mushrooms", "lemon", "lime",
    "apple", "apples", "banana", "bananas", "orange", "oranges",
    "strawberry", "strawberries", "mango", "peach", "pear",
    "cauliflower", "asparagus", "beetroot", "radish", "rosemary",
    "basil", "parsley", "cilantro", "thyme", "mint"
}

_PROTEINS = {
    "egg", "eggs", "chicken", "beef", "pork", "tofu", "lentils",
    "chickpeas", "black beans", "kidney beans", "tuna", "shrimp",
    "turkey", "greek yogurt", "cottage cheese", "tempeh"
}

_PROCESSED_PENALTY = {
    "chips", "soda", "candy", "white sugar", "margarine", "hot dogs",
    "instant noodles", "frozen pizza", "cream cheese frosting",
    "processed cheese", "white bread", "mayonnaise"
}


def health_score(ingredients: list[str]) -> tuple[int, str]:
    """
    Score the healthiness of a pantry on a scale of 1–10.

    Scoring logic:
      +1  for every fresh produce item (max +3)
      +2  for every superfood (max +4)
      +1  for every protein source (max +2)
      -1  for every processed/junk item (max -3)
      Base score: 4

    Args:
        ingredients: List of ingredient name strings (lowercase).

    Returns:
        Tuple of (score: int, explanation: str).
    """
    logger.info(f"Computing health score for {len(ingredients)} ingredients.")

    normalised = {i.lower().strip() for i in ingredients}

    superfoods_found   = normalised & _SUPERFOODS
    fresh_found        = normalised & _FRESH_PRODUCE
    proteins_found     = normalised & _PROTEINS
    processed_found    = normalised & _PROCESSED_PENALTY

    score = 4
    score += min(len(fresh_found),     3)
    score += min(len(superfoods_found) * 2, 4)
    score += min(len(proteins_found),  2)
    score -= min(len(processed_found), 3)
    score  = max(1, min(10, score))

    logger.info(
        f"Score: {score} | superfoods={superfoods_found} "
        f"fresh={fresh_found} proteins={proteins_found} processed={processed_found}"
    )

    # ── Build explanation ──────────────────────────────────────────────────────
    parts = []
    if superfoods_found:
        parts.append(f"Superfoods detected: **{', '.join(sorted(superfoods_found))}** 🌟")
    if fresh_found:
        parts.append(f"Fresh produce: **{', '.join(sorted(fresh_found))}** 🥦")
    if proteins_found:
        parts.append(f"Good protein sources: **{', '.join(sorted(proteins_found))}** 💪")
    if processed_found:
        parts.append(f"Processed items to limit: **{', '.join(sorted(processed_found))}** ⚠️")
    if not parts:
        parts.append("Add more fresh vegetables, fruits, and lean proteins to boost your score.")

    explanation = "\n\n".join(parts)
    return score, explanation
