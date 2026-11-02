# pandas Concat and Merge: Notes

*Oct 31, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **pandas Concat and Merge** lecture from the **CodeBasics Python course**. The `indicator` and `validate` options in the audit examples come from the [pandas `merge` documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html).

## Where I started

Real audit evidence never arrives in one table. It comes as monthly extracts, a subledger, a customer master and shipping records. This lecture covered the two ways to bring tables together: **`concat`**, which stacks tables that have the same shape, and **`merge`**, which matches rows by a shared key, like SQL joins or a VLOOKUP.

## The data in brief

The examples used small tables built in the notebook. There was no data file.

- **Weather for 3 Indian cities** (Mumbai, Delhi, Bangalore) and **3 US cities** (New York, Chicago, Orlando), with temperature and humidity.
- For the joins: **temperatures for 4 US cities** and **humidity for 3**. Only New York and Chicago appear in both tables.

## What I learnt

### `concat`: stack tables

```python
pd.concat([india_weather, us_weather])                           # 6 rows, but the index repeats 0, 1, 2, 0, 1, 2
pd.concat([india_weather, us_weather], ignore_index=True)        # renumbered 0 to 5
df = pd.concat([india_weather, us_weather], keys=["india", "us"])
df.loc["us"]                                                     # the keys label each source, so each can be pulled back out
```

**Side by side with `axis=1`:** rows line up by **index label**, not by position. The windspeed table listed Delhi first, but because it carried index labels `[1, 0]`, each value still landed on the right city. Bangalore had no windspeed, so it got `NaN`. The `city` column also appeared twice, which shows `concat` doesn't really *match* on columns; that's `merge`'s job.

### `merge`: match rows on a key

```python
pd.merge(df1, df2, on="city")      # matches by city, whatever order the rows are in
```

**The four join types,** using temperatures for 4 cities and humidity for 3:

| `how=` | Keeps | Rows | Result |
| --- | --- | --- | --- |
| `"inner"` (default) | Only keys in **both** tables | 2 | New York, Chicago |
| `"left"` | Every key in the **left** table | 4 | Orlando and Baltimore get `NaN` humidity |
| `"right"` | Every key in the **right** table | 3 | San Diego gets `NaN` temperature |
| `"outer"` | Every key in **either** table | 5 | Gaps shown as `NaN` on both sides |

The default inner join quietly **drops** anything without a match. In audit, the unmatched rows are often the most interesting ones.

## How this shows up in financial statement audit work: revenue and AR

These snippets use small sample data built in the code. They add two `merge` options from the pandas documentation that weren't in the lecture:

- `indicator=True` adds a `_merge` column saying where each row came from.
- `validate=` stops the merge if the keys aren't as unique as expected.

**1. Building the full-year revenue population and reconciling it to the GL.**

```python
import pandas as pd

q1 = pd.DataFrame({"invoice": ["INV101", "INV102"], "customer": ["C01", "C02"], "amount": [120_000, 85_000]})
q2 = pd.DataFrame({"invoice": ["INV201", "INV202"], "customer": ["C01", "C03"], "amount": [95_000, 140_000]})
q3 = pd.DataFrame({"invoice": ["INV301"],           "customer": ["C04"],        "amount": [60_000]})

sales_register = pd.concat([q1, q2, q3], keys=["Q1", "Q2", "Q3"]).reset_index(level=0, names="quarter")
gl_revenue = 500_000

print(sales_register["amount"].sum())                 # 500000
print(sales_register["amount"].sum() == gl_revenue)   # True: the population is complete
```

`keys` records which quarterly file each invoice came from, so any exception can be traced back to its source.

**2. Customers that don't exist in the customer master.** A left join with `indicator=True` shows invoices whose customer has no master record, a classic fictitious-revenue red flag:

```python
customer_master = pd.DataFrame({"customer": ["C01", "C02", "C03"],
                                "name": ["Acme Corp", "Beta Ltd", "Gamma Inc"]})

checked = sales_register.merge(customer_master, on="customer", how="left", indicator=True)
print(checked[checked["_merge"] == "left_only"][["invoice", "customer", "amount"]])
# INV301  C04  60000: revenue billed to a customer missing from the master file
```

An **inner** join here would have dropped INV301 without any warning. That's exactly the risk the lecture's join table shows.

**3. Invoices against shipping records, testing occurrence and completeness.** An outer join shows gaps on both sides:

```python
shipments = pd.DataFrame({"invoice": ["INV101", "INV102", "INV201", "INV202", "INV305"],
                          "ship_date": ["2026-02-10", "2026-03-05", "2026-05-12", "2026-06-30", "2026-09-29"]})

match = sales_register.merge(shipments, on="invoice", how="outer", indicator=True)
print(match[match["_merge"] == "left_only"]["invoice"].tolist())    # ['INV301']: billed, never shipped (occurrence)
print(match[match["_merge"] == "right_only"]["invoice"].tolist())   # ['INV305']: shipped, never billed (completeness)
```

**4. AR aging and subsequent cash receipts.** Matching year-end AR to cash received after year-end shows which balances still need alternative procedures:

```python
ar_aging = pd.DataFrame({"customer": ["C01", "C02", "C03", "C04"],
                         "balance":  [215_000, 85_000, 140_000, 60_000],
                         "days_past_due": [10, 95, 30, 150]})
receipts = pd.DataFrame({"customer": ["C01", "C03", "C03"],
                         "received": [215_000, 90_000, 50_000]})    # after year-end

paid = receipts.groupby("customer", as_index=False)["received"].sum()
ar = ar_aging.merge(paid, on="customer", how="left", validate="one_to_one").fillna({"received": 0})
ar["unpaid"] = ar["balance"] - ar["received"]
print(ar[ar["unpaid"] > 0][["customer", "unpaid", "days_past_due"]])
# C02  85000   95 | C04  60000  150: unpaid and overdue, so consider the allowance and confirmations
```

The receipts are summed per customer *before* merging, so each AR balance matches exactly one row.

**5. Catching duplicate keys before they inflate revenue.** If the customer master has a duplicate ID, a merge copies every matching invoice row, and revenue grows silently:

```python
dup_master = pd.concat([customer_master, pd.DataFrame({"customer": ["C01"], "name": ["Acme Corp (old)"]})])

inflated = sales_register.merge(dup_master, on="customer")
print(inflated["amount"].sum())           # 655000 instead of 440000: C01's invoices were counted twice

try:
    sales_register.merge(dup_master, on="customer", validate="many_to_one")
except pd.errors.MergeError as e:
    print("Stopped:", e)                  # the duplicate is caught before any totals are used
```

## My reflection

This lecture turned VLOOKUP-style matching into something I can control and document. The join table was the key idea. Choosing `inner`, `left`, `right` or `outer` is really choosing which exceptions you're willing to lose. In revenue and AR testing, the rows that *don't* match are usually the findings: invoices with no shipment, customers with no master record, balances with no subsequent receipt.

The duplicate-key example will stay with me. A single repeated customer ID silently inflated revenue by 49%, with no error. From now on, I'll use `indicator=True` to see what didn't match, `validate=` to protect the totals, and I'll reconcile row counts and amounts after every merge.
