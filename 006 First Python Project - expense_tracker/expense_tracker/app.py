"""Expense Tracker — log expenses by category, date and currency, then analyze them."""
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

import database as db

st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")
db.init_db()

CHART_COLORS = ["#2F5D62", "#5E8B7E", "#A7C4BC", "#C9A227", "#8C5E58",
                "#4A6FA5", "#9C89B8", "#D17A22", "#6B8F71", "#B5838D"]
CURRENCY_CODES = list(db.CURRENCIES)


def symbol(code: str) -> str:
    return db.CURRENCIES.get(code, (f"{code} ", ""))[0]


def money(x: float, code: str) -> str:
    return f"{symbol(code)}{x:,.2f}"


def currency_label(code: str) -> str:
    sym, name = db.CURRENCIES.get(code, (code, code))
    return f"{code} ({sym.strip()}) · {name}"


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("category")["amount"]
        .agg(Total="sum", Entries="count", Average="mean")
        .sort_values("Total", ascending=False)
        .reset_index()
        .rename(columns={"category": "Category"})
    )
    summary["Share"] = summary["Total"] / summary["Total"].sum() * 100
    return summary


def show_category_breakdown(df: pd.DataFrame, code: str, key: str) -> None:
    """Metrics, charts and table for one currency's expenses."""
    summary = category_summary(df)
    top = summary.iloc[0]
    sym = symbol(code)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total spent", money(df["amount"].sum(), code))
    c2.metric("Highest category", top["Category"], money(top["Total"], code))
    c3.metric("Number of expenses", len(df))

    left, right = st.columns(2)
    with left:
        fig = px.bar(summary, x="Total", y="Category", orientation="h",
                     color="Category", color_discrete_sequence=CHART_COLORS,
                     title="Spending by category",
                     labels={"Total": f"Total ({code})"})
        fig.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch", key=f"{key}_bar")
    with right:
        fig = px.pie(summary, names="Category", values="Total", hole=0.45,
                     color_discrete_sequence=CHART_COLORS, title="Share of total")
        st.plotly_chart(fig, width="stretch", key=f"{key}_pie")

    st.dataframe(
        summary,
        hide_index=True,
        width="stretch",
        column_config={
            "Total": st.column_config.NumberColumn(format=f"{sym}%.2f"),
            "Average": st.column_config.NumberColumn(format=f"{sym}%.2f"),
            "Share": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100),
        },
    )


def pick_analysis_currency(key: str) -> str | None:
    """Let the user choose which currency to analyze. Returns None if no data."""
    used = db.get_used_currencies()
    if not used:
        return None
    if len(used) == 1:
        st.caption(f"Amounts shown in {currency_label(used[0])}")
        return used[0]
    code = st.selectbox(
        "Currency to analyze",
        used,
        format_func=currency_label,
        key=key,
        help="Amounts in different currencies aren't added together, so each currency is analyzed on its own.",
    )
    return code


# ---------------- Sidebar: default currency ----------------
with st.sidebar:
    st.header("Settings")
    default_currency = st.selectbox(
        "Default currency for new expenses",
        CURRENCY_CODES,
        index=CURRENCY_CODES.index(db.DEFAULT_CURRENCY),
        format_func=currency_label,
        key="default_currency",
    )

st.title("💸 Expense Tracker")
st.caption("Log what you spend, then see where your money goes.")

tab_add, tab_history, tab_categories, tab_range = st.tabs(
    ["➕ Add expense", "📋 History", "📊 By category", "📅 Date range analysis"]
)

# ---------------- Add expense ----------------
with tab_add:
    st.subheader("Log a new expense")
    categories = db.get_categories()

    with st.form("add_expense", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 2, 3])
        expense_date = col1.date_input("Date", value=date.today(), max_value=date.today())
        amount = col2.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")
        currency = col3.selectbox(
            "Currency",
            CURRENCY_CODES,
            index=CURRENCY_CODES.index(default_currency),
            format_func=currency_label,
        )

        col4, col5 = st.columns(2)
        category = col4.selectbox("Category", categories + ["➕ New category…"])
        new_category = col5.text_input("New category name", placeholder="Only if you chose “New category…”")

        note = st.text_input("Note (optional)", placeholder="e.g. Lunch with team")
        submitted = st.form_submit_button("Save expense", type="primary", width="stretch")

    if submitted:
        final_category = new_category.strip() if category == "➕ New category…" else category
        if amount <= 0:
            st.error("Enter an amount greater than zero.")
        elif not final_category:
            st.error("Type a name for the new category.")
        else:
            db.add_expense(expense_date, final_category, amount, currency, note)
            st.success(
                f"Saved {money(amount, currency)} under {final_category} on {expense_date:%d %b %Y}."
            )

# ---------------- History ----------------
with tab_history:
    st.subheader("All expenses")
    df_all = db.get_expenses()

    if df_all.empty:
        st.info("No expenses yet. Add your first one in the “Add expense” tab.")
    else:
        shown = df_all.copy()
        shown["Amount"] = [money(a, c) for a, c in zip(shown["amount"], shown["currency"])]
        st.dataframe(
            shown[["id", "expense_date", "category", "Amount", "currency", "note"]].rename(
                columns={"id": "ID", "expense_date": "Date", "category": "Category",
                         "currency": "Currency", "note": "Note"}
            ),
            hide_index=True,
            width="stretch",
        )

        col_a, col_b = st.columns([3, 1])
        with col_a:
            def describe(i: int) -> str:
                r = df_all.loc[df_all["id"] == i].iloc[0]
                return f"#{i} · {r.expense_date} · {r.category} · {money(r.amount, r.currency)}"

            to_delete = st.selectbox("Delete an expense", df_all["id"], format_func=describe)
        with col_b:
            st.write("")
            st.write("")
            if st.button("Delete", width="stretch"):
                db.delete_expense(to_delete)
                st.rerun()

        st.download_button("Download as CSV", df_all.to_csv(index=False), "expenses.csv", "text/csv")

# ---------------- By category (all time) ----------------
with tab_categories:
    st.subheader("Where you spend the most (all time)")
    code = pick_analysis_currency(key="cat_currency")
    if code is None:
        st.info("Add some expenses to see the category breakdown.")
    else:
        show_category_breakdown(db.get_expenses(currency=code), code, key="alltime")

# ---------------- Date range analysis ----------------
with tab_range:
    st.subheader("Analyze a date range")

    code = pick_analysis_currency(key="range_currency")
    presets = {
        "Last 7 days": (date.today() - timedelta(days=6), date.today()),
        "Last 30 days": (date.today() - timedelta(days=29), date.today()),
        "This month": (date.today().replace(day=1), date.today()),
        "This year": (date.today().replace(month=1, day=1), date.today()),
        "Custom": None,
    }
    preset = st.radio("Quick range", list(presets), horizontal=True, index=1)

    if preset == "Custom":
        c1, c2 = st.columns(2)
        start = c1.date_input("From", value=date.today() - timedelta(days=29), key="from")
        end = c2.date_input("To", value=date.today(), key="to")
    else:
        start, end = presets[preset]
        st.caption(f"{start:%d %b %Y} to {end:%d %b %Y}")

    if code is None:
        st.info("Add some expenses to analyze a date range.")
    elif start > end:
        st.error("The “From” date must be on or before the “To” date.")
    else:
        df_range = db.get_expenses(start, end, currency=code)
        if df_range.empty:
            st.info(f"No {code} expenses in this date range. Try a wider range or another currency.")
        else:
            show_category_breakdown(df_range, code, key="range")

            st.markdown("#### Daily spending by category")
            daily = df_range.groupby(["expense_date", "category"])["amount"].sum().reset_index()
            fig = px.bar(daily, x="expense_date", y="amount", color="category",
                         color_discrete_sequence=CHART_COLORS,
                         labels={"expense_date": "Date", "amount": f"Amount ({code})",
                                 "category": "Category"})
            st.plotly_chart(fig, width="stretch", key="range_daily")

            with st.expander("See expenses in this range"):
                st.dataframe(
                    df_range.drop(columns=["id", "currency"]).rename(columns={
                        "expense_date": "Date", "category": "Category",
                        "amount": "Amount", "note": "Note"}),
                    hide_index=True,
                    width="stretch",
                    column_config={"Amount": st.column_config.NumberColumn(format=f"{symbol(code)}%.2f")},
                )
