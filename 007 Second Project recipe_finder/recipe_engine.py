"""Recipe matching logic. Has no Streamlit code, so it can be tested on its own."""
import json
from pathlib import Path

RECIPES_PATH = Path(__file__).parent / "recipes.json"
ANY = "Any"

# Pantry basics we assume everyone has, so they never count as "missing".
STAPLES = {"salt", "pepper", "black pepper", "oil", "olive oil", "water", "sugar"}

MEAT_AND_SEAFOOD = {"Chicken", "Beef", "Pork", "Lamb", "Fish", "Shrimp"}
ANIMAL_PRODUCTS = {"Eggs", "Paneer"}


def load_recipes(path: Path = RECIPES_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_options(recipes: list[dict]) -> dict[str, list[str]]:
    """Dropdown choices come from the data, so new recipes add new options automatically."""
    proteins = sorted({r["protein"] for r in recipes} - {"No main protein"})
    return {
        "protein": [ANY] + proteins + ["No main protein"],
        "cuisine": [ANY] + sorted({r["cuisine"] for r in recipes}),
        "diet": [ANY] + sorted({d for r in recipes for d in r["diets"]}),
    }


def _singular(word: str) -> str:
    """Very small plural-to-singular helper: tomatoes→tomato, berries→berry, eggs→egg."""
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("oes"):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def normalize(ingredient: str) -> str:
    words = ingredient.lower().replace("-", " ").split()
    return " ".join(_singular(w) for w in words)


def parse_ingredients(text: str) -> list[str]:
    """Turn 'Tomatoes, garlic,, Onion ' into ['tomato', 'garlic', 'onion'] (no duplicates, staples removed)."""
    seen: list[str] = []
    for part in text.split(","):
        item = normalize(part.strip())
        if item and item not in seen and item not in {normalize(s) for s in STAPLES}:
            seen.append(item)
    return seen


def ingredients_match(user_item: str, recipe_item: str) -> bool:
    """'beef' matches 'ground beef', and 'ground beef' matches 'beef'."""
    user_words = set(normalize(user_item).split())
    recipe_words = set(normalize(recipe_item).split())
    return user_words <= recipe_words or recipe_words <= user_words


def score_recipe(recipe: dict, user_ingredients: list[str]) -> dict:
    matched, missing = [], []
    for item in recipe["ingredients"]:
        if any(ingredients_match(u, item) for u in user_ingredients):
            matched.append(item)
        else:
            missing.append(item)
    total = len(recipe["ingredients"])
    return {
        "recipe": recipe,
        "matched": matched,
        "missing": missing,
        "score": len(matched) / total if total else 0.0,
    }


def passes_filters(recipe: dict, protein: str, cuisine: str, diet: str) -> bool:
    return (
        (protein == ANY or recipe["protein"] == protein)
        and (cuisine == ANY or recipe["cuisine"] == cuisine)
        and (diet == ANY or diet in recipe["diets"])
    )


def find_recipes(
    recipes: list[dict],
    user_ingredients: list[str],
    protein: str = ANY,
    cuisine: str = ANY,
    diet: str = ANY,
    max_missing: int | None = None,
) -> list[dict]:
    """Filter by dropdowns, score by ingredients, and return best matches first.

    If ingredients were given, recipes that use none of them are left out.
    """
    results = []
    for recipe in recipes:
        if not passes_filters(recipe, protein, cuisine, diet):
            continue
        result = score_recipe(recipe, user_ingredients)
        if user_ingredients and not result["matched"]:
            continue
        if max_missing is not None and len(result["missing"]) > max_missing:
            continue
        results.append(result)

    results.sort(key=lambda r: (-r["score"], len(r["missing"]), r["recipe"]["time_minutes"]))
    return results


def diet_conflict(protein: str, diet: str) -> str | None:
    """Explain when the chosen protein and diet can't both be true."""
    if diet in {"Vegetarian", "Vegan"} and protein in MEAT_AND_SEAFOOD:
        return f"{protein} isn't {diet.lower()}, so no recipes can match both. Try changing the protein or the diet."
    if diet == "Vegan" and protein in ANIMAL_PRODUCTS:
        return f"{protein} isn't vegan, so no recipes can match both. Try tofu or beans & lentils instead."
    if diet == "Dairy-Free" and protein == "Paneer":
        return "Paneer is a dairy product, so no recipes can match both."
    return None
