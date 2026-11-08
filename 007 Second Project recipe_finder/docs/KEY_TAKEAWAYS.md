# Key Takeaways

What this project teaches about building small, data-driven apps in Python.

## 1. Keep data, logic and interface separate
Recipes live in `recipes.json`, matching rules live in `recipe_engine.py`, and display code lives in `app.py`. Each piece can change without breaking the others: adding a recipe needs no code, and redesigning the cards doesn't touch the matching logic.

## 2. Streamlit re-runs the whole script on every interaction
There's no search button or event handler: changing any input re-runs the script, and the results update. This makes the app feel live with very little code. The trade-off is that slow work would repeat on every change, which leads to the next point.

## 3. Cache anything that doesn't need to be repeated
`@st.cache_data` means `recipes.json` is read once, not on every click. Caching is the main tool for keeping Streamlit apps fast as they grow.

## 4. Build options from the data, not by hand
The cuisine, protein and diet dropdowns are created from whatever is in the recipe file. Lists can't drift out of sync with the data, and there's never a dropdown option with no recipes behind it.

## 5. Clean user input before using it
People type `Tomatoes, garlic,, Onion `. Splitting on commas, trimming spaces, lowercasing, converting plurals and removing duplicates turns that into `tomato, garlic, onion`. Most matching bugs come from skipping this step.

## 6. Normalize both sides of a comparison
The same `normalize()` function is applied to what the user types and to the recipe's ingredients. If only one side were cleaned, "Tomatoes" and "tomato" would still fail to match.

## 7. Compare whole words, not letters
A simple text search would match "chicken" to "chickpeas". Comparing sets of words lets "beef" match "ground beef" while avoiding false matches. Python's set operators (`<=` for "is contained in") make this one line.

## 8. A good ranking uses tie-breakers
Sorting by match score alone leaves many ties. Adding "fewest missing ingredients" and then "shortest cooking time" as tie-breakers puts the most useful recipes first. Python sorts by tuples, so this is a single `key=` function.

## 9. Explain empty results instead of just showing them
"No recipes found" leaves people stuck. The app explains impossible combinations (chicken with a vegan diet) and suggests what to change when nothing matches. Good empty states make an app feel helpful rather than broken.

## 10. Small assumptions improve the experience
Treating salt, pepper, oil, water and sugar as always available removes noise from every "You need" list. Deciding what to assume is a design choice, and it's worth making it clearly in one place (`STAPLES`).

## 11. Logic without UI code is easy to test
Because `recipe_engine.py` doesn't import Streamlit, its functions can be checked directly in Python: does "eggs" become "egg", does "beef" find "ground beef", does Tofu + Vegan return only vegan tofu dishes? The whole app was also tested with Streamlit's `AppTest`, which runs the page without a browser.

## 12. Check your data automatically
With 150 recipes, mistakes in labels are easy to make and hard to spot by eye. `validate_recipes.py` checks every diet label against the ingredients in under a second. The more data an app has, the more an automatic check is worth.

## 13. Plan for more data than you start with
Showing every result was fine with 33 recipes but not with 150. Splitting results into pages of 12 keeps the page fast, and giving the page box a key based on the search sends each new search back to page 1. Ask how a feature behaves when the data grows.

## 14. Simple matching has limits
Word matching is fast and predictable but not perfect: "onion" also matches "green onion", and "beef" doesn't find "steak". Knowing a method's limits is part of choosing it. A synonym list or an AI model could handle these cases in a later version.
