"""Recipe Finder: suggest recipes from the ingredients you have."""
import math

import streamlit as st

import recipe_engine as engine

st.set_page_config(page_title="Recipe Finder", page_icon="🍳", layout="wide")


@st.cache_data
def get_recipes() -> list[dict]:
    return engine.load_recipes()


recipes = get_recipes()
options = engine.get_options(recipes)

st.title("🍳 Recipe Finder")
st.caption("Tell us what's in your kitchen and we'll suggest what to cook.")

# ---------------- Inputs ----------------
ingredients_text = st.text_input(
    "Ingredients you have (separate with commas)",
    placeholder="e.g. tomato, onion, garlic, rice",
    help="Salt, pepper, oil, water and sugar are assumed, so you don't need to enter them. Press Enter to search.",
)
user_ingredients = engine.parse_ingredients(ingredients_text)
if user_ingredients:
    st.caption("Searching with: " + " · ".join(user_ingredients))

col1, col2, col3 = st.columns(3)
protein = col1.selectbox("Protein", options["protein"])
cuisine = col2.selectbox("Cuisine", options["cuisine"])
diet = col3.selectbox("Diet type", options["diet"])

with st.expander("More options"):
    limit_missing = st.checkbox("Only show recipes I'm close to making")
    max_missing = (
        st.slider("Maximum missing ingredients", 0, 8, 3) if limit_missing else None
    )

st.divider()

# ---------------- Results ----------------
conflict = engine.diet_conflict(protein, diet)
if conflict:
    st.warning(conflict)
    st.stop()

results = engine.find_recipes(recipes, user_ingredients, protein, cuisine, diet, max_missing)

if not results:
    st.info(
        "No recipes match these choices. Try setting one of the dropdowns to “Any”, "
        "adding more ingredients, or allowing more missing ingredients."
    )
    st.stop()

PAGE_SIZE = 12
pages = math.ceil(len(results) / PAGE_SIZE)

heading = f"{len(results)} recipe{'s' if len(results) != 1 else ''} found"
st.subheader(heading + (" · best matches first" if user_ingredients else ""))

page = 1
if pages > 1:
    # The key changes whenever the search changes, so a new search always starts on page 1.
    search_key = f"{ingredients_text}|{protein}|{cuisine}|{diet}|{max_missing}"
    page = st.number_input(
        f"Page (of {pages})", min_value=1, max_value=pages, value=1, step=1,
        key=f"page_{hash(search_key)}",
    )
first = (page - 1) * PAGE_SIZE
page_results = results[first : first + PAGE_SIZE]
if pages > 1:
    st.caption(f"Showing {first + 1} to {first + len(page_results)} of {len(results)}")

for i in range(0, len(page_results), 2):
    cols = st.columns(2)
    for col, result in zip(cols, page_results[i : i + 2]):
        recipe = result["recipe"]
        with col.container(border=True):
            st.markdown(f"### {recipe['name']}")
            st.caption(
                f"{recipe['cuisine']} · {recipe['protein']} · ⏱ {recipe['time_minutes']} min · "
                f"🍽 serves {recipe['servings']}"
            )
            if recipe["diets"]:
                st.markdown(" ".join(f"`{d}`" for d in recipe["diets"]))

            if user_ingredients:
                have, total = len(result["matched"]), len(recipe["ingredients"])
                st.progress(result["score"], text=f"You have {have} of {total} ingredients")
                if result["matched"]:
                    st.markdown("✅ **You have:** " + ", ".join(result["matched"]))
                if result["missing"]:
                    st.markdown("🛒 **You need:** " + ", ".join(result["missing"]))
                else:
                    st.success("You have everything for this one!")

            with st.expander("Show recipe"):
                st.markdown("**Ingredients**")
                st.markdown("\n".join(f"- {item}" for item in recipe["ingredients"]))
                st.caption("Plus pantry basics: salt, pepper, oil and water.")
                st.markdown("**Steps**")
                st.markdown(
                    "\n".join(f"{n}. {step}" for n, step in enumerate(recipe["steps"], start=1))
                )
