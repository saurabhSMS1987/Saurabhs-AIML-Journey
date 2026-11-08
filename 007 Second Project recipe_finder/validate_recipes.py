"""Check recipes.json for mistakes before running the app.

Run:  python validate_recipes.py

It checks that every recipe has the required fields, that names are unique,
and that diet labels don't contradict the ingredients (for example, a
"Dairy-Free" recipe that uses butter).
"""
import sys
from collections import Counter

from recipe_engine import MEAT_AND_SEAFOOD, load_recipes

REQUIRED = {"name": str, "cuisine": str, "protein": str, "diets": list,
            "time_minutes": int, "servings": int, "ingredients": list, "steps": list}

DAIRY = {"butter", "cream", "cheese", "milk", "yogurt", "paneer", "parmesan", "mozzarella",
         "feta", "cheddar", "gruyere", "buttermilk", "blue cheese", "ghee"}
GLUTEN = {"flour", "soy sauce", "spaghetti", "penne", "bread", "baguette", "breadcrumbs", "panko",
          "tortillas", "pizza dough", "pie crust", "egg noodles", "wheat noodles", "udon noodles",
          "bulgur", "phyllo dough", "macaroni", "burger buns", "oyster sauce", "hoisin sauce",
          "worcestershire sauce", "beef broth", "gochujang", "miso paste"}
NOT_VEGETARIAN = {"fish sauce", "oyster sauce", "bacon", "anchovies", "dashi", "chicken broth",
                  "beef broth", "fish stock", "seafood stock", "pancetta", "ham", "chorizo", "kimchi"}
NOT_VEGAN = NOT_VEGETARIAN | DAIRY | {"eggs", "honey", "mayonnaise"}
HIGH_CARB_WORDS = {"rice", "potato", "pasta", "spaghetti", "bread", "flour", "noodle", "tortilla",
                   "honey", "corn", "bean", "lentil", "chickpea", "pea"}


def check(recipes: list[dict]) -> list[str]:
    problems = []
    for name, count in Counter(r.get("name") for r in recipes).items():
        if count > 1:
            problems.append(f"'{name}' appears {count} times")

    for r in recipes:
        name = r.get("name", "<no name>")
        for field, kind in REQUIRED.items():
            if not isinstance(r.get(field), kind):
                problems.append(f"{name}: '{field}' is missing or not a {kind.__name__}")
        if problems and problems[-1].startswith(name):
            continue

        ingredients = set(r["ingredients"])
        diets = set(r["diets"])
        if r["protein"] in MEAT_AND_SEAFOOD and diets & {"Vegetarian", "Vegan"}:
            problems.append(f"{name}: {r['protein']} can't be vegetarian or vegan")
        if "Vegan" in diets and r["protein"] in {"Eggs", "Paneer"}:
            problems.append(f"{name}: {r['protein']} isn't vegan")
        if "Vegan" in diets and not {"Vegetarian", "Dairy-Free"} <= diets:
            problems.append(f"{name}: vegan recipes should also be tagged Vegetarian and Dairy-Free")
        checks = [
            ("Dairy-Free", DAIRY), ("Gluten-Free", GLUTEN),
            ("Vegetarian", NOT_VEGETARIAN), ("Vegan", NOT_VEGAN),
        ]
        for diet, banned in checks:
            if diet in diets and ingredients & banned:
                problems.append(f"{name}: tagged {diet} but uses {', '.join(sorted(ingredients & banned))}")
        if "Keto/Low-Carb" in diets:
            carby = [i for i in ingredients if any(w in i.split() or w + "s" in i.split() for w in HIGH_CARB_WORDS)]
            if carby:
                problems.append(f"{name}: tagged Keto/Low-Carb but uses {', '.join(sorted(carby))}")
    return problems


if __name__ == "__main__":
    recipes = load_recipes()
    problems = check(recipes)
    print(f"Checked {len(recipes)} recipes.")
    print("Cuisines:", dict(Counter(r["cuisine"] for r in recipes)))
    if problems:
        print(f"\n{len(problems)} problem(s) found:")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("No problems found ✅")
