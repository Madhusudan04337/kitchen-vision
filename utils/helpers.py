from utils.logger import get_logger

logger = get_logger(__name__)

_FRESH_PRODUCE = {
    "tomato", "tomatoes", "cherry tomatoes", "onion", "red onion", "spring onion",
    "potato", "potatoes", "sweet potato", "carrot", "carrots", "spinach",
    "kale", "lettuce", "cucumber", "zucchini", "courgette", "bell pepper",
    "green bell pepper", "red bell pepper", "yellow bell pepper", "broccoli",
    "cauliflower", "celery", "asparagus", "beetroot", "radish", "mushroom",
    "mushrooms", "avocado", "lemon", "lime", "apple", "apples", "banana",
    "bananas", "orange", "oranges", "strawberry", "strawberries", "mango",
    "peach", "pear", "blueberry", "blueberries", "garlic", "ginger",
    "rosemary", "basil", "parsley", "cilantro", "thyme", "mint", "dill"
}

_COLD_STORAGE = {"milk", "oat milk", "almond milk", "cheese", "yogurt", "greek yogurt",
    "butter", "cream", "sour cream", "cream cheese", "cottage cheese",
    "tofu", "tempeh", "eggs", "egg", "fresh pasta", "orange juice",
    "hummus", "leftovers"
}

_FROZEN = {
    "frozen peas", "frozen corn", "frozen berries", "ice cream",
    "frozen chicken", "frozen fish", "frozen prawns", "frozen shrimp",
    "frozen vegetables", "frozen pizza", "frozen waffles"
}

_PROTEINS = {
    "chicken", "chicken breast", "chicken thigh", "beef", "ground beef",
    "pork", "pork chop", "bacon", "salmon", "tuna", "shrimp", "prawns",
    "lentils", "chickpeas", "black beans", "kidney beans", "white beans",
    "edamame", "turkey", "lamb"
}


def categorize_items(ingredients: list[str]) -> dict[str, list[str]]:
    """
    Sort a flat list of ingredients into pantry storage categories.
    Priority order: Frozen > Cold Storage > Fresh Produce > Proteins > Dry Storage
    """
    categories: dict[str, list[str]] = {
        "🥬 Fresh Produce": [],
        "❄️ Cold Storage":  [],
        "🧊 Frozen":        [],
        "🥩 Proteins":      [],
        "🌾 Dry Storage":   [],
    }

    for item in ingredients:
        lower = item.lower().strip()

        if lower in _FROZEN:
            categories["🧊 Frozen"].append(item)
        elif lower in _COLD_STORAGE:
            categories["❄️ Cold Storage"].append(item)
        elif lower in _FRESH_PRODUCE:
            categories["🥬 Fresh Produce"].append(item)
        elif lower in _PROTEINS:
            categories["🥩 Proteins"].append(item)
        else:
            categories["🌾 Dry Storage"].append(item)

    logger.info(f"Categorised {len(ingredients)} ingredients: { {k: len(v) for k, v in categories.items()} }")
    return categories