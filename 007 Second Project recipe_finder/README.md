# 🍳 Recipe Finder (Streamlit)

Enter the ingredients you have, choose a protein, cuisine and diet type, and get recipe suggestions ranked by how many of your ingredients they use.

## Files
- `app.py` – the Streamlit app (inputs and recipe cards)
- `recipe_engine.py` – matching and filtering logic (no UI code)
- `recipes.json` – the recipe collection (150 recipes, 12 cuisines)
- `validate_recipes.py` – checks `recipes.json` for mistakes after you edit it
- `requirements.txt` – Python dependencies
- `.streamlit/config.toml` – color theme
- `docs/` – guides: how the code works, quick reference, summary, key takeaways

## Run it
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501.

## Features
- **Ingredients:** type several, separated by commas (e.g. `tomato, onion, garlic`)
- **Protein, cuisine and diet dropdowns**, each with an “Any” option
- **Match score** for each recipe, with what you have and what you still need
- **“Close to making” filter** to limit how many ingredients can be missing
- **Full recipe** with ingredients and steps for every result
- **Pages of 12 results**, so large result lists stay fast
- **Conflict warnings**, for example if you choose Chicken with a Vegan diet

## Add your own recipes
Add an entry to `recipes.json`, then run `python validate_recipes.py` to check it. New cuisines, proteins and diet types appear in the dropdowns automatically. See `docs/QUICK_REFERENCE.md` for the format.
