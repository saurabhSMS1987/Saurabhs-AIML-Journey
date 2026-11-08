# Streamlit with Python --- Practical Cheat Sheet

**Last updated:** 8 November 2026\
**Purpose:** A practical, example-driven reference for building
interactive Python data apps with Streamlit. Examples use finance and
audit analytics scenarios such as journal-entry review, trial-balance
analysis, exception reporting, and reconciliation.

> Streamlit turns a regular Python script into an interactive web app.
> This guide is a coding reference, not a substitute for security, audit
> methodology, or production review.

------------------------------------------------------------------------

## 1. What is Streamlit?

Streamlit is an open-source Python framework for building data apps. You
write Python; Streamlit renders text, tables, charts, and interactive
controls in a browser.

**Core execution model:** Streamlit normally reruns the script from top
to bottom when a user interacts with a widget. Widget values are made
available on the rerun. Use Session State when values must persist
across reruns, and caching to avoid repeating expensive work.

------------------------------------------------------------------------

## 2. Install and run

### Install

``` bash
# Recommended: create and activate a virtual environment first
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install streamlit pandas numpy plotly openpyxl
```

### Run an app

``` bash
streamlit run app.py
```

Useful commands:

``` bash
streamlit --version
streamlit hello
streamlit config show
streamlit cache clear
```

Stop the local server with `Ctrl+C` in the terminal.

------------------------------------------------------------------------

## 3. Minimal app structure

Create `app.py`:

``` python
import streamlit as st

st.set_page_config(
    page_title="Audit Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Audit Analytics Workbench")
st.write("Explore financial data and investigate exceptions.")
st.success("The app is running.")
```

`st.set_page_config()` should normally be the first Streamlit command in
the script.

------------------------------------------------------------------------

## 4. Display text, data, and status

``` python
st.title("Main page title")
st.header("Section heading")
st.subheader("Smaller heading")
st.text("Monospaced plain text")
st.markdown("**Bold**, *italic*, and [a link](https://streamlit.io)")
st.caption("Small supporting note")
st.code("print('Hello, Streamlit')", language="python")
st.latex(r"\text{Debit} = \text{Credit}")
st.divider()

st.write("Flexible display:", 123, {"status": "complete"})
st.json({"period": "2026-Q3", "records": 12500})
```

Status messages:

``` python
st.info("Review the selected reporting period.")
st.success("Validation completed.")
st.warning("Some rows require investigation.")
st.error("The file could not be processed.")
```

------------------------------------------------------------------------

## 5. Input widgets

Widgets return values that can be used like ordinary Python variables.

``` python
period = st.selectbox(
    "Reporting period",
    ["2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4"]
)

minimum_amount = st.number_input(
    "Minimum journal amount",
    min_value=0.0,
    value=10000.0,
    step=1000.0
)

include_manual_entries = st.checkbox(
    "Include manual journal entries",
    value=True
)

risk_level = st.radio(
    "Risk level",
    ["All", "High", "Medium", "Low"],
    horizontal=True
)

selected_accounts = st.multiselect(
    "Accounts to review",
    ["Cash", "Revenue", "Accounts Receivable", "Expenses"]
)

reviewer_notes = st.text_area("Reviewer notes")
run_review = st.button("Run review")
```

Common widgets:

  Widget                   Typical use
  ------------------------ ------------------------------
  `st.button()`            Trigger an action
  `st.download_button()`   Download a generated file
  `st.checkbox()`          Yes/no filter
  `st.toggle()`            On/off setting
  `st.radio()`             Choose one option
  `st.selectbox()`         Dropdown selection
  `st.multiselect()`       Choose multiple options
  `st.slider()`            Select a numeric range/value
  `st.number_input()`      Enter a number
  `st.text_input()`        Short text
  `st.text_area()`         Longer text
  `st.date_input()`        Choose dates
  `st.file_uploader()`     Upload files
  `st.data_editor()`       Edit tabular data

Use a unique `key=` when similar widgets appear more than once or when
you need to access a widget value through Session State.

------------------------------------------------------------------------

## 6. Upload CSV and Excel files

``` python
import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader(
    "Upload a trial balance",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"Loaded {len(df):,} rows.")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Upload a CSV or Excel file to begin.")
```

For Excel files with multiple sheets:

``` python
uploaded_file = st.file_uploader("Upload workbook", type=["xlsx"])

if uploaded_file:
    excel_file = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select worksheet", excel_file.sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
    st.dataframe(df, use_container_width=True)
```

For large files, consider file-size limits, memory use, and whether the
data should be processed in a controlled backend rather than entirely in
the app process.

------------------------------------------------------------------------

## 7. Data preview, filtering, and editing

``` python
# Preview first 100 rows
st.dataframe(df.head(100), use_container_width=True)

# Basic filters
if "Account" in df.columns:
    accounts = sorted(df["Account"].dropna().astype(str).unique())
    chosen_accounts = st.multiselect("Filter accounts", accounts)

    if chosen_accounts:
        filtered_df = df[df["Account"].astype(str).isin(chosen_accounts)]
    else:
        filtered_df = df.copy()

    st.metric("Rows after filtering", f"{len(filtered_df):,}")
    st.dataframe(filtered_df, use_container_width=True)
```

Editable table:

``` python
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)
```

Treat edits as user input. Validate them before using them in
calculations or exporting results.

------------------------------------------------------------------------

## 8. Layout: columns, sidebar, tabs, and expanders

``` python
st.sidebar.header("Review filters")
period = st.sidebar.selectbox("Period", ["Q1", "Q2", "Q3", "Q4"])

col1, col2, col3 = st.columns(3)
col1.metric("Journal entries", "12,450")
col2.metric("Exceptions", "186", delta="-12")
col3.metric("Exception rate", "1.49%")

tab1, tab2, tab3 = st.tabs(["Overview", "Exceptions", "Methodology"])

with tab1:
    st.write("Summary KPIs and charts go here.")

with tab2:
    st.write("Detailed exception table goes here.")

with tab3:
    st.write("Document filters, assumptions, and test logic.")

with st.expander("Show calculation details"):
    st.write("Place supporting calculations or notes here.")
```

Other useful layout elements include `st.container()`, `st.popover()`,
`st.columns()`, and `st.tabs()`.

------------------------------------------------------------------------

## 9. Metrics and charts

### KPI cards

``` python
total_debits = df["Debit"].sum()
total_credits = df["Credit"].sum()
difference = total_debits - total_credits

a, b, c = st.columns(3)
a.metric("Total debits", f"${total_debits:,.2f}")
b.metric("Total credits", f"${total_credits:,.2f}")
c.metric("Difference", f"${difference:,.2f}")
```

### Built-in charts

``` python
# Requires a DataFrame with suitable numeric columns
st.line_chart(monthly_summary, x="Month", y="Amount")
st.bar_chart(account_summary, x="Account", y="Amount")
st.area_chart(monthly_summary, x="Month", y="Amount")
```

### Plotly chart

``` python
import plotly.express as px

fig = px.bar(
    account_summary,
    x="Account",
    y="Amount",
    title="Amount by account"
)
st.plotly_chart(fig, use_container_width=True)
```

Use charts that help answer a business or audit question. Label units,
explain filters, and avoid implying that an analytical flag is proof of
an error.

------------------------------------------------------------------------

## 10. Forms: submit several inputs together

A form batches widget input so the app processes it when the user
submits the form.

``` python
with st.form("journal_review_filters"):
    period = st.selectbox("Period", ["2026-Q2", "2026-Q3"])
    threshold = st.number_input("Absolute amount threshold", min_value=0, value=10000)
    include_weekends = st.checkbox("Include weekend postings")
    submitted = st.form_submit_button("Apply filters")

if submitted:
    st.write("Filters applied:", period, threshold, include_weekends)
```

Forms are useful when several selections should be applied together
rather than recalculating after every individual change.

------------------------------------------------------------------------

## 11. Session State: retain values across reruns

Ordinary Python variables are recreated when the script reruns. Session
State persists values for the current user session.

``` python
if "review_count" not in st.session_state:
    st.session_state.review_count = 0

if st.button("Record review"):
    st.session_state.review_count += 1

st.write("Reviews recorded:", st.session_state.review_count)
```

Example: retain a selected review period:

``` python
if "period" not in st.session_state:
    st.session_state.period = "2026-Q3"

st.selectbox(
    "Reporting period",
    ["2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4"],
    key="period"
)

st.write("Current selection:", st.session_state.period)
```

Session State is session-scoped; it is not a permanent database or a
substitute for saving records to an approved data store.

------------------------------------------------------------------------

## 12. Caching: improve performance

Use `st.cache_data` for data-returning functions such as reading files,
querying data, or transforming DataFrames.

``` python
@st.cache_data
def load_csv(file_bytes):
    import pandas as pd
    from io import BytesIO
    return pd.read_csv(BytesIO(file_bytes))

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = load_csv(uploaded_file.getvalue())
    st.dataframe(df)
```

Use `st.cache_resource` for shared resources such as a model or database
connection:

``` python
@st.cache_resource
def load_model():
    # Load and return a model object here
    return build_or_load_model()

model = load_model()
```

Do not cache user-specific or confidential information in a way that
could expose it across users. Understand cache scope and invalidation
before deploying.

------------------------------------------------------------------------

## 13. Download CSV and Excel outputs

### CSV

``` python
csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered data (CSV)",
    data=csv_bytes,
    file_name="filtered_journal_entries.csv",
    mime="text/csv"
)
```

### Excel

``` python
from io import BytesIO

output = BytesIO()

with pd.ExcelWriter(output, engine="openpyxl") as writer:
    filtered_df.to_excel(writer, index=False, sheet_name="Filtered Data")

st.download_button(
    label="Download Excel report",
    data=output.getvalue(),
    file_name="audit_review_output.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
```

For audit outputs, consider including run date/time, selected period,
filter criteria, row counts, data source identifier, and version of the
analysis logic.

------------------------------------------------------------------------

## 14. Validation and error handling

``` python
required_columns = ["Journal_ID", "Account", "Posting_Date", "Debit", "Credit"]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {', '.join(missing_columns)}")
    st.stop()

if df.empty:
    st.warning("The uploaded file contains no records.")
    st.stop()

try:
    df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce")
    df["Credit"] = pd.to_numeric(df["Credit"], errors="coerce")
except Exception as exc:
    st.exception(exc)
```

Prefer clear, user-friendly error messages. Avoid displaying secrets,
credentials, stack traces, or confidential record values to ordinary
users.

------------------------------------------------------------------------

## 15. Example mini-project: Journal Entry Exception Explorer

This example expects a CSV with columns `Journal_ID`, `Account`,
`Posting_Date`, `Debit`, `Credit`, and optionally `Created_By`.

Save as `app.py`:

``` python
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="JE Exception Explorer", layout="wide")
st.title("Journal Entry Exception Explorer")
st.caption("Illustrative analytics — flags require investigation, not automatic conclusions.")

uploaded = st.file_uploader("Upload journal-entry CSV", type=["csv"])

REQUIRED = ["Journal_ID", "Account", "Posting_Date", "Debit", "Credit"]

if uploaded is None:
    st.info("Upload a CSV file to start.")
    st.stop()

try:
    df = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Unable to read the CSV: {exc}")
    st.stop()

missing = [col for col in REQUIRED if col not in df.columns]
if missing:
    st.error(f"Required columns missing: {', '.join(missing)}")
    st.stop()

df["Posting_Date"] = pd.to_datetime(df["Posting_Date"], errors="coerce")
df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce").fillna(0)
df["Credit"] = pd.to_numeric(df["Credit"], errors="coerce").fillna(0)
df["Net_Amount"] = df["Debit"] - df["Credit"]
df["Absolute_Amount"] = df["Net_Amount"].abs()

st.sidebar.header("Filters")
threshold = st.sidebar.number_input(
    "Minimum absolute net amount",
    min_value=0.0,
    value=10000.0,
    step=1000.0
)

accounts = sorted(df["Account"].dropna().astype(str).unique())
selected_accounts = st.sidebar.multiselect(
    "Accounts",
    accounts,
    default=accounts
)

filtered = df[
    (df["Absolute_Amount"] >= threshold)
    & (df["Account"].astype(str).isin(selected_accounts))
].copy()

c1, c2, c3 = st.columns(3)
c1.metric("Uploaded rows", f"{len(df):,}")
c2.metric("Filtered rows", f"{len(filtered):,}")
c3.metric("Filtered net amount", f"${filtered['Net_Amount'].sum():,.2f}")

st.subheader("Filtered journal entries")
st.dataframe(filtered, use_container_width=True)

if not filtered.empty:
    chart_data = (
        filtered.groupby("Account", as_index=False)["Absolute_Amount"]
        .sum()
        .sort_values("Absolute_Amount", ascending=False)
    )
    fig = px.bar(
        chart_data,
        x="Account",
        y="Absolute_Amount",
        title="Absolute net amount by account"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No rows match the selected filters.")

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered exceptions",
    data=csv_data,
    file_name="je_filtered_exceptions.csv",
    mime="text/csv"
)
```

**Important:** This is a teaching example. It does not implement a
complete audit test, establish materiality, validate the source system,
or determine whether an entry is inappropriate. Define and document test
logic with the engagement team before using it for audit work.

------------------------------------------------------------------------

## 16. Multipage app structure

A simple directory-based multipage project can look like this:

``` text
audit-streamlit-app/
├── app.py
├── pages/
│   ├── 1_Trial_Balance.py
│   ├── 2_Journal_Entries.py
│   └── 3_Exceptions.py
├── utils/
│   ├── data_loader.py
│   └── validation.py
├── data/
│   └── sample_data.csv
├── requirements.txt
├── .gitignore
└── README.md
```

Run the app from the project root:

``` bash
streamlit run app.py
```

Streamlit discovers page scripts in the `pages/` folder. For more
customized navigation, review the current `st.navigation` and `st.Page`
APIs in the official documentation.

------------------------------------------------------------------------

## 17. Secrets and security

Never hard-code passwords, API keys, tokens, or database credentials in
Python files or commit them to GitHub.

For local development, Streamlit supports a secrets file such as
`.streamlit/secrets.toml`:

``` toml
# .streamlit/secrets.toml — keep this file out of Git
[database]
host = "your-host"
username = "your-user"
password = "your-password"
```

Read a value in Python:

``` python
import streamlit as st

db_host = st.secrets["database"]["host"]
```

Add this to `.gitignore`:

``` gitignore
.streamlit/secrets.toml
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

Use deployment-platform secrets for deployed apps. Follow your
organization's approved data classification, access control, retention,
and hosting requirements. Do not upload real client, employee, customer,
or financial data to a public repository or an unapproved hosting
service.

------------------------------------------------------------------------

## 18. requirements.txt and GitHub

Example `requirements.txt`:

``` text
streamlit
pandas
numpy
plotly
openpyxl
```

For reproducible deployments, pin versions after testing them in your
environment, for example `streamlit==<tested-version>`. Do not copy an
untested version number from an old tutorial.

Typical Git workflow:

``` bash
git init
git add .
git commit -m "Add Streamlit audit analytics app"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Before pushing, inspect the files being committed and confirm that no
secrets, credentials, or restricted data are included.

------------------------------------------------------------------------

## 19. Deployment overview

A common beginner path is Streamlit Community Cloud:

1.  Push the app code to a GitHub repository.
2.  Sign in to Streamlit Community Cloud.
3.  Create a new app and select the repository, branch, and entry-point
    file (for example, `app.py`).
4.  Add required secrets through the deployment settings, not in source
    code.
5.  Deploy and test the app using non-sensitive sample data.

Check the official deployment documentation for current account,
repository, and deployment requirements. Public hosting is not
appropriate for confidential audit/client data unless explicitly
approved and properly secured.

------------------------------------------------------------------------

## 20. Testing and troubleshooting

### Basic app test

Streamlit provides `AppTest` for automated tests:

``` python
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py")
at.run()

assert not at.exception
```

Build more tests for missing columns, empty files, invalid dates,
unexpected data types, filter behavior, and export results.

### Common issues

  -----------------------------------------------------------------------
  Symptom                             What to check
  ----------------------------------- -----------------------------------
  `streamlit` command not found       Activate the correct virtual
                                      environment; install Streamlit
                                      there

  `ModuleNotFoundError`               Install the missing package in the
                                      active environment

  App does not reflect changes        Save the file and rerun; inspect
                                      terminal errors

  Widget value resets                 Use a stable widget key and/or
                                      `st.session_state`

  App is slow                         Profile code; avoid repeated reads;
                                      consider `st.cache_data`

  Duplicate widget ID/key             Give each widget a unique key

  Excel read error                    Install `openpyxl`; verify file
                                      format

  Missing or wrong columns            Validate the uploaded schema before
                                      processing
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 21. Quick reference: frequently used commands

  Goal             Streamlit command
  ---------------- -----------------------------------------------
  Page title       `st.set_page_config()`
  Heading          `st.title()`, `st.header()`, `st.subheader()`
  Text             `st.write()`, `st.markdown()`, `st.caption()`
  Table            `st.dataframe()`
  Editable table   `st.data_editor()`
  KPI              `st.metric()`
  File upload      `st.file_uploader()`
  Download         `st.download_button()`
  Dropdown         `st.selectbox()`
  Multi-select     `st.multiselect()`
  Slider           `st.slider()`
  Checkbox         `st.checkbox()`
  Button           `st.button()`
  Form             `st.form()`
  Sidebar          `st.sidebar`
  Columns          `st.columns()`
  Tabs             `st.tabs()`
  Expander         `st.expander()`
  Persist state    `st.session_state`
  Cache data       `@st.cache_data`
  Cache resource   `@st.cache_resource`
  Show error       `st.error()`
  Stop execution   `st.stop()`
  Rerun app        `st.rerun()`

------------------------------------------------------------------------

## 22. Practical development checklist

-   [ ] Create and activate a virtual environment.
-   [ ] Install dependencies and record them in `requirements.txt`.
-   [ ] Define the purpose and intended users of the app.
-   [ ] Validate uploaded data and required columns.
-   [ ] Handle missing values, invalid dates, and unexpected data types.
-   [ ] Use clear labels, units, and explanations for filters and
    metrics.
-   [ ] Use Session State only where persistence across reruns is
    required.
-   [ ] Cache expensive data operations where appropriate.
-   [ ] Test empty, malformed, and unusually large files.
-   [ ] Test downloads and verify output contents.
-   [ ] Keep credentials and secrets out of source control.
-   [ ] Use synthetic/sample data in public GitHub repositories.
-   [ ] Obtain approval before processing or hosting confidential
    information.
-   [ ] Document assumptions, limitations, and test logic.

------------------------------------------------------------------------

## 23. Official sources and further learning

The examples and concepts in this guide are based primarily on the
official Streamlit documentation. Documentation evolves, so consult the
current API reference when a function's behavior or parameters matter.

1.  **Streamlit --- Get started**\
    https://docs.streamlit.io/get-started

2.  **Streamlit --- Basic concepts and execution model**\
    https://docs.streamlit.io/get-started/fundamentals/main-concepts

3.  **Streamlit --- Create an app tutorial**\
    https://docs.streamlit.io/get-started/tutorials/create-an-app

4.  **Streamlit --- API reference**\
    https://docs.streamlit.io/develop/api-reference

5.  **Streamlit --- Official API cheat sheet**\
    https://docs.streamlit.io/develop/quick-reference/cheat-sheet

6.  **Streamlit --- Caching and state**\
    https://docs.streamlit.io/develop/api-reference/caching-and-state

7.  **Streamlit --- Session State**\
    https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state

8.  **Streamlit --- Tutorials**\
    https://docs.streamlit.io/develop/tutorials

9.  **Streamlit --- App testing**\
    https://docs.streamlit.io/develop/concepts/app-testing

10. **Streamlit --- Community Cloud deployment**\
    https://docs.streamlit.io/deploy/streamlit-community-cloud

------------------------------------------------------------------------

## 24. Suggested GitHub repository description

**Repository name:** `streamlit-python-cheatsheet`

**Short description:** Practical Streamlit reference with Python
examples for building interactive data apps, including file uploads,
filters, charts, Session State, caching, downloads, validation, and
audit analytics use cases.

**Suggested repository files:**

-   `README.md` --- this cheat sheet
-   `app.py` --- the Journal Entry Exception Explorer example
-   `requirements.txt` --- Python dependencies
-   `.gitignore` --- excludes local environments and secrets
-   `data/sample_journal_entries.csv` --- synthetic sample data only

**License note:** Add a license only if you intend to grant others
permission to reuse, modify, and distribute the repository. Check your
employer's policies before publishing work-related code or examples.
