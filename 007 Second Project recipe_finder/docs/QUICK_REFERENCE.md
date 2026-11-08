# Quick Reference Guide: Running the Recipe Finder

## Requirements
- Python 3.10 or newer
- pip (comes with Python)

## First-time setup

| Step | macOS / Linux | Windows |
|------|---------------|---------|
| 1. Go to the project folder | `cd recipe_finder` | `cd recipe_finder` |
| 2. Create a virtual environment | `python3 -m venv venv` | `python -m venv venv` |
| 3. Activate it | `source venv/bin/activate` | `venv\Scripts\activate` |
| 4. Install packages | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| 5. Start the app | `streamlit run app.py` | `streamlit run app.py` |

The app opens automatically at **http://localhost:8501**.

## Every time after that

```bash
cd recipe_finder
source venv/bin/activate        # Windows: venv\Scripts\activate
streamlit run app.py
```

## Stop the app
Press **Ctrl + C** in the terminal.

## Required folder layout

```
recipe_finder/
├── app.py
├── recipe_engine.py
├── recipes.json
├── validate_recipes.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Using the app

| I want to… | Do this |
|------------|---------|
| Find recipes from what I have | Type ingredients separated by commas, then press **Enter** |
| Choose a protein | **Protein** dropdown |
| Choose a cuisine | **Cuisine** dropdown |
| Choose a diet | **Diet type** dropdown |
| Browse without ingredients | Leave the ingredients box empty and use the dropdowns |
| See only recipes I can almost make | **More options** → tick the box → set **Maximum missing ingredients** |
| See the full recipe | Click **Show recipe** on a card |
| See more results | Change the **Page** number above the cards |
| Clear a filter | Set the dropdown back to **Any** |

**Tips**
- No need to enter salt, pepper, oil, water or sugar; they're assumed.
- Plurals and capital letters don't matter: `Tomatoes` finds `tomato`.
- General names find specific ones: `beef` finds `ground beef`.

## Useful commands

| Task | Command |
|------|---------|
| Use a different port | `streamlit run app.py --server.port 8502` |
| Run without opening a browser | `streamlit run app.py --server.headless true` |
| Check the recipe file for mistakes | `python validate_recipes.py` |
| Check the file is valid JSON only | `python -c "import json; json.load(open('recipes.json')); print('OK')"` |

## Add a recipe

Add an entry inside the list in `recipes.json` (remember the comma between entries):

```json
{
  "name": "Your Recipe",
  "cuisine": "Korean",
  "protein": "Beef",
  "diets": ["Dairy-Free", "High-Protein"],
  "time_minutes": 30,
  "servings": 4,
  "ingredients": ["beef", "soy sauce", "garlic"],
  "steps": ["First step.", "Second step."]
}
```

- `protein` should be one of the existing proteins (Beans & Lentils, Beef, Chicken, Eggs, Fish, Lamb, Paneer, Pork, Shrimp, Tofu) or `"No main protein"`.
- `diets` can include Vegetarian, Vegan, Gluten-Free, Dairy-Free, Keto/Low-Carb and High-Protein. Vegan recipes should also list Vegetarian and Dairy-Free.
- Run `python validate_recipes.py` to check your new entry.
- Leave salt, pepper, oil and water out of `ingredients`.
- Restart the app, or open the app's **⋮** menu and choose **Clear cache**, to see the change.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `streamlit: command not found` | Activate the virtual environment, or run `python -m streamlit run app.py` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` with the environment active |
| `JSONDecodeError` on start | `recipes.json` has a typo, often a missing or extra comma. The error message gives the line number. |
| Validator reports a problem | Fix the recipe it names: remove the wrong diet label or change the ingredient |
| New recipe not showing | Open the **⋮** menu → **Clear cache**, or restart the app |
| "No recipes match" | Set a dropdown back to **Any**, add ingredients, or untick the missing-ingredients limit |
| `Port 8501 is already in use` | Close the other app, or use `--server.port 8502` |
| Theme colors not applied | Make sure `config.toml` is inside a folder named `.streamlit` |

## Customize

| Change | Where |
|--------|-------|
| Add or edit recipes | `recipes.json` |
| Change the assumed pantry staples | `STAPLES` in `recipe_engine.py` |
| Change diet conflict rules | `diet_conflict()` in `recipe_engine.py` |
| Change results per page | `PAGE_SIZE` in `app.py` |
| Change the theme | `.streamlit/config.toml` |
