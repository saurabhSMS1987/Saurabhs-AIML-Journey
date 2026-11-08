# Recipe Finder: Summary

A recipe suggestion app built with **Python** and **Streamlit**. Enter the ingredients you have, choose a protein, cuisine and diet type, and it ranks recipes by how many of your ingredients they use, showing what you have and what you'd still need to buy.

## What it does

- **Takes several ingredients at once**, separated by commas, and handles plurals, capitals and extra spaces
- **Filters by protein** (chicken, beef, pork, lamb, fish, shrimp, tofu, eggs, paneer, beans & lentils, or none)
- **Filters by cuisine** (American, Chinese, French, Indian, Italian, Japanese, Korean, Mediterranean, Mexican, Spanish, Thai, Vietnamese)
- **Filters by diet** (vegetarian, vegan, gluten-free, dairy-free, keto/low-carb, high-protein)
- **Ranks recipes** by match score, then fewest missing ingredients, then shortest cooking time
- **Shows a shopping list** for each recipe: what you have and what you need
- **Limits missing ingredients** with an optional slider, to find recipes you can make now
- **Warns about impossible combinations**, such as chicken with a vegan diet
- **Shows results in pages of 12**, so even broad searches stay fast
- **Works offline**, with 150 recipes stored in a simple JSON file
- **Checks its own data** with a validation script that catches wrong diet labels

## Tech stack

| Tool | Used for |
|------|----------|
| Python | Matching and filtering logic |
| Streamlit | Web interface |
| JSON | Recipe storage |

Streamlit is the only package to install; everything else comes with Python.

## Project structure

```
recipe_finder/
├── app.py                 # Interface and recipe cards
├── recipe_engine.py       # Parsing, filtering, scoring, sorting
├── recipes.json           # Recipe collection (150 recipes)
├── validate_recipes.py    # Checks recipes.json for mistakes
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Color theme
└── docs/
    ├── HOW_IT_WORKS.md    # Step-by-step code walkthrough
    ├── QUICK_REFERENCE.md # How to run the app
    ├── SUMMARY.md         # This file
    └── KEY_TAKEAWAYS.md   # What this project teaches
```

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for full setup steps and troubleshooting.

## Design choices

- **Data separate from code.** Recipes live in `recipes.json`, so anyone can add one without touching Python.
- **Dropdowns built from the data.** New cuisines, proteins and diets appear automatically, and every option has at least one recipe.
- **Logic separate from the interface.** `recipe_engine.py` has no Streamlit code, so it can be tested on its own.
- **Diet labels checked automatically.** `validate_recipes.py` compares every label with the ingredients, so a "Vegan" recipe can't quietly include fish sauce.
- **Forgiving ingredient matching.** Word-based matching lets "beef" find "ground beef" without "chicken" matching "chickpeas".

## Possible next steps

- Generate new recipes with an AI model when nothing in the collection fits
- Save favorite recipes
- Scale ingredient quantities to the number of servings
- Add nutrition information per serving
- Combine several recipes' missing ingredients into one shopping list
- Exclude ingredients you dislike or are allergic to
