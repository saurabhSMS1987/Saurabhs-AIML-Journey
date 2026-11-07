# Key Takeaways

What this project teaches about building small data apps in Python.

## 1. Streamlit re-runs the whole script on every interaction
Instead of writing event handlers, you write a top-to-bottom script, and widgets return their current values each run. This makes simple apps very quick to build. The trade-off is that you have to think about what runs on each re-run, which is why the add-expense inputs sit inside `st.form`: a form waits for the submit button rather than re-running on every change.

## 2. Separate storage from presentation
All SQL lives in `database.py` and all interface code lives in `app.py`. Each file is easier to read and test on its own, and either side could be replaced (for example, SQLite with PostgreSQL) without rewriting the other.

## 3. SQLite is enough for personal apps
SQLite comes with Python, needs no server, and stores everything in a single file. For a single-user app it's simple and reliable, and backing up your data is as easy as copying `expenses.db`.

## 4. Always use parameterized queries
Values are passed to SQL with `?` placeholders rather than pasted into the query string. This prevents SQL injection and avoids bugs when a note contains an apostrophe, like "Mom's birthday".

## 5. Let the database enforce rules too
The `CHECK (amount > 0)` rule means a bad amount can't be saved even if the interface's validation is bypassed. Checking in both places gives friendly error messages in the app and a safety net in the data.

## 6. Plan for schema changes from the start
Adding the currency column could have broken existing databases. Checking the table's columns with `PRAGMA table_info` and adding what's missing with `ALTER TABLE` lets people upgrade the app without losing any data. Real apps change over time, and their stored data has to come along.

## 7. Don't add up values that aren't the same unit
₹100 plus $50 isn't 150 of anything. Analyzing each currency separately keeps every total accurate. The same principle applies to mixing units, time zones or measurement scales in any data project.

## 8. pandas `groupby` does the heavy lifting
One line, `groupby("category")["amount"].agg(...)`, produces totals, counts and averages for every category. Sorting the result makes the top spending category simply the first row.

## 9. Filter in the database, summarize in pandas
Date range and currency filters run in SQL, so only the needed rows are loaded. pandas then handles the summarizing and reshaping it does best. Using each tool for what it's good at keeps the code short and fast.

## 10. Reuse one function for similar views
The all-time view and the date range view both call `show_category_breakdown()`. One function means the two views always look the same, and a fix or improvement only has to be made once.

## 11. Store dates in a sortable format
Saving dates as `YYYY-MM-DD` text means alphabetical order matches date order, so `BETWEEN` queries and sorting work without any conversion.

## 12. Empty states and errors guide the user
Every view handles the "no data yet" case with a message telling the user what to do next, and errors say exactly what to fix ("Enter an amount greater than zero."). Small touches like these make an app feel finished.

## 13. Test the app, not just the syntax
Streamlit's built-in `AppTest` can run the app without a browser, click buttons, and check what appears on screen. During development it flagged outdated Streamlit arguments and confirmed that the database upgrade worked.
