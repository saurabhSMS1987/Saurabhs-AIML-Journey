# How the Code Works: A Step-by-Step Guide

This guide follows the Recipe Finder from launch to the moment recipe cards appear on screen. The project is split into files with separate jobs:

| File | Job |
|------|-----|
| `recipes.json` | The data: every recipe, its tags, ingredients and steps. |
| `recipe_engine.py` | The logic: parsing ingredients, filtering, scoring and sorting. Contains no Streamlit code. |
| `app.py` | The interface: draws inputs and recipe cards, and calls the engine. |
| `validate_recipes.py` | A checker you run after editing `recipes.json`. Not used by the app itself. |

Keeping these apart means you can add recipes without touching code, and test the matching logic without opening a browser.

---

## Step 1: Understand how Streamlit runs your script

Every time you change an input (press Enter in the ingredients box, pick a dropdown option, move the slider), Streamlit **re-runs `app.py` from top to bottom**. Each widget call, such as `st.selectbox(...)`, draws the widget and returns its current value. Results update automatically, without a "Search" button.

## Step 2: Load the recipes once

```python
@st.cache_data
def get_recipes() -> list[dict]:
    return engine.load_recipes()
```

`load_recipes()` reads `recipes.json` (150 recipes across 12 cuisines) into a list of Python dictionaries. Each recipe looks like this:

```json
{
  "name": "Shakshuka",
  "cuisine": "Mediterranean",
  "protein": "Eggs",
  "diets": ["Vegetarian", "Gluten-Free", "Dairy-Free"],
  "time_minutes": 30,
  "servings": 3,
  "ingredients": ["eggs", "tomato", "bell pepper", "onion", "garlic", "cumin", "paprika"],
  "steps": ["Cook chopped onion and bell pepper...", "..."]
}
```

Because the script re-runs on every interaction, `@st.cache_data` is important: it keeps the loaded recipes in memory, so the file is only read the first time.

## Step 3: Build the dropdown options from the data

```python
options = engine.get_options(recipes)
```

`get_options()` collects every distinct cuisine, protein and diet found in the recipes, sorts them, and puts **"Any"** first. "No main protein" is placed last for protein.

Building the options from the data, rather than typing them into the code, means a new recipe with a new cuisine (say "Ethiopian") adds that cuisine to the dropdown automatically. It also guarantees there's never a dropdown option with no recipes behind it.

## Step 4: Read the ingredients the user types

```python
user_ingredients = engine.parse_ingredients(ingredients_text)
```

`parse_ingredients()` turns messy input into a clean list:

| Input | Output |
|-------|--------|
| `Tomatoes, garlic,, Onion , salt, eggs, Eggs` | `['tomato', 'garlic', 'onion', 'egg']` |

It does this in order:
1. **Splits on commas**, so you can enter several ingredients at once.
2. **Trims spaces and lowercases** everything, so "Onion " and "onion" are the same.
3. **Converts plurals to singular** with `_singular()` (tomatoes → tomato, berries → berry, eggs → egg). The same conversion is applied to recipe ingredients, so both sides always compare in the same form.
4. **Skips empty entries**, such as the gap in `garlic,,`.
5. **Removes duplicates**, keeping your original order.
6. **Drops pantry staples** (salt, pepper, oil, olive oil, water, sugar), since they're assumed and never listed in recipes.

The app then shows "Searching with: tomato · garlic · onion · egg", so you can see exactly what it understood.

## Step 5: Read the dropdowns and options

```python
protein = col1.selectbox("Protein", options["protein"])
cuisine = col2.selectbox("Cuisine", options["cuisine"])
diet = col3.selectbox("Diet type", options["diet"])
```

The three dropdowns sit side by side in `st.columns(3)`. Inside "More options", a checkbox reveals a slider for the maximum number of missing ingredients. If the checkbox is off, `max_missing` is `None`, meaning no limit.

## Step 6: Catch impossible combinations

```python
conflict = engine.diet_conflict(protein, diet)
if conflict:
    st.warning(conflict)
    st.stop()
```

Some choices can never match: Chicken with Vegetarian, Eggs with Vegan, or Paneer with Dairy-Free. Rather than showing a confusing "no results", `diet_conflict()` explains why, and `st.stop()` ends the run there.

## Step 7: Filter recipes by the dropdowns

```python
def passes_filters(recipe, protein, cuisine, diet):
    return (
        (protein == ANY or recipe["protein"] == protein)
        and (cuisine == ANY or recipe["cuisine"] == cuisine)
        and (diet == ANY or diet in recipe["diets"])
    )
```

Each filter is skipped when set to "Any". Diet uses `in` because a recipe can have several diet tags; a vegan recipe is also tagged Vegetarian, so it shows up for both.

## Step 8: Score each recipe against your ingredients

```python
def ingredients_match(user_item, recipe_item):
    user_words = set(normalize(user_item).split())
    recipe_words = set(normalize(recipe_item).split())
    return user_words <= recipe_words or recipe_words <= user_words
```

Two ingredients match if all the words of one appear in the other. This lets general and specific names find each other:

| You type | Recipe needs | Match? | Why |
|----------|--------------|--------|-----|
| `beef` | `ground beef` | ✅ | "beef" is inside "ground beef" |
| `ground beef` | `beef` | ✅ | works in the other direction too |
| `tomatoes` | `tomato` | ✅ | plurals are normalized |
| `onion` | `green onion` | ✅ | broad terms match specific ones |
| `chicken` | `chickpeas` | ❌ | whole words are compared, not letters |

`score_recipe()` then splits the recipe's ingredients into **matched** (you have them) and **missing** (you'd need to buy them), and calculates:

```
score = matched ingredients ÷ total ingredients
```

## Step 9: Sort and trim the results

`find_recipes()` brings Steps 7 and 8 together:

1. Skips recipes that fail the dropdown filters.
2. If you entered ingredients, skips recipes that use **none** of them.
3. If the "close to making" slider is on, skips recipes missing too many ingredients.
4. Sorts by: highest score first, then fewest missing ingredients, then shortest cooking time.

If you haven't typed any ingredients, every recipe that passes the filters is shown, so the dropdowns work on their own for browsing.

## Step 10: Split the results into pages

With 150 recipes, a broad search can return over 100 results. Drawing them all at once would make the page slow and long, so the results are shown **12 at a time**:

```python
PAGE_SIZE = 12
pages = math.ceil(len(results) / PAGE_SIZE)
page_results = results[first : first + PAGE_SIZE]
```

A **Page** number box appears only when there's more than one page, with a caption such as "Showing 13 to 24 of 102".

The page box's `key` is built from the current search (ingredients, dropdowns and slider). Streamlit treats a widget with a new key as a brand-new widget, so **every new search starts back on page 1** instead of staying on, say, page 9 of a search that now has only 2 pages.

## Step 11: Show the recipe cards

The results are laid out two per row with `st.columns(2)`. Each card, drawn inside `st.container(border=True)`, shows:

- The name, then cuisine, protein, cooking time and servings
- Diet tags
- A **progress bar**: "You have 4 of 7 ingredients"
- ✅ **You have** and 🛒 **You need** lists (a shopping list for that recipe)
- A **Show recipe** expander with the full ingredient list and numbered steps

If nothing matches, an info message suggests what to change instead of leaving an empty page.

## Step 12: Theme

`.streamlit/config.toml` sets warm kitchen colors. Streamlit applies it automatically at startup.

## Step 13: Check the recipe file (`validate_recipes.py`)

With 150 recipes, a wrong label is easy to miss: a "Dairy-Free" recipe that uses butter, or a "Vegan" one that uses fish sauce. Running `python validate_recipes.py` checks every recipe for:

- **Missing or wrongly typed fields**, such as `time_minutes` written as text
- **Duplicate names**
- **Diet labels that contradict the ingredients**, using lists of dairy, gluten, meat-based and high-carb ingredients
- **Impossible protein and diet pairs**, such as Lamb tagged Vegetarian

It prints each problem it finds, or "No problems found ✅". It also exits with an error code when there are problems, so it could run automatically on GitHub before changes are accepted.

---

## How data flows through the app

```
 recipes.json ──► load_recipes() (cached) ──► get_options() ──► dropdowns
                         │
 "Tomatoes, garlic"      │
        │                │
        ▼                │
 parse_ingredients()     │
  → ['tomato','garlic']  │
        │                ▼
        └──────► find_recipes()
                   ├─ passes_filters()   protein / cuisine / diet
                   ├─ score_recipe()     matched vs missing
                   ├─ max_missing check
                   └─ sort by best match
                         │
                         ▼
             12 per page → recipe cards in app.py
```
