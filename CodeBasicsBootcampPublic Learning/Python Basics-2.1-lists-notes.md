# Python Lists: My Lecture 4 Notes

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Lists** lecture from the **CodeBasics Python course**.

## Where I started

The lecture opened with a shopping list stored as four separate variables: `item1`, `item2`, `item3`, `item4`. That works for four items, but not for four thousand invoices. A list keeps everything under one name, in order, and lets me add, remove, sort and search. It felt like moving from sticky notes to a spreadsheet column.

## What I learnt

A list holds several values in square brackets: `items = ["bread", "pasta", "fruits", "veggies"]`.

**Reading items** works like string indexing:

| Code | Result |
| --- | --- |
| `items[0]` | `'bread'` |
| `items[-1]` | `'veggies'` |
| `items[:2]` | `['bread', 'pasta']` |
| `len(items)` | `4` |

**Lists are mutable.** Unlike strings, I can change a list in place with `items[1] = "cheese"`.

**Adding and removing:**

- `append("butter")` adds to the end.
- `insert(1, "butter")` adds at a chosen position.
- `remove("pasta")` deletes the first match. Removing an item that isn't there (`"fan"`) raises a `ValueError`.

**Other tools:**

- `"bread" in items` checks membership and returns `True` or `False`.
- `sort()` puts `[30, 1200, 45, 300]` in order as `[30, 45, 300, 1200]`.
- `+` joins two lists, and `reverse()` flips the order.
- `dir(list)` shows every method, including `count`, `index`, `pop` and `extend`.
- A list can mix types: `["car", 4.5, True]`.

One thing caught me out: `items[2:4] = ["almonds"]` replaced **two** items with **one**, so the list got shorter. Slice assignment doesn't need to match in size.

## How this shows up in audit work

Most audit populations are lists: invoices, vendors, journal entries. These snippets use the lecture's tools on audit-style data.

**1. Checking against an approved vendor list.** `in` is a quick check against the vendor master.

```python
approved_vendors = ["ABC Supplies", "Delta Traders", "Nova Logistics"]
vendor = "Quick Cash Ltd"
print(vendor in approved_vendors)   # False: unapproved vendor
```

**2. Spotting duplicate invoices with `count()`.**

```python
invoice_ids = ["INV101", "INV102", "INV103", "INV102"]
print(invoice_ids.count("INV102"))   # 2: possible duplicate payment
```

**3. Picking the largest items for testing.** Sorting and then slicing from the end gives the top values.

```python
payments = [1200, 45000, 300, 98000, 7500]
payments.sort()
print(payments[-2:])   # [45000, 98000]: high-value items to test
```

**4. Combining populations and building an exception list.**

```python
q1_entries = [5000, 120000, 800]
q2_entries = [64000, 2500]
population = q1_entries + q2_entries
print(len(population))        # 5

exceptions = []
exceptions.append(120000)     # add each item that fails a test
exceptions.append(64000)
print(exceptions)             # [120000, 64000]
```

## My reflection

Lists feel like the bridge between single values and real audit data. The `ValueError` from removing a missing item reminded me of a good audit habit: confirm something exists before acting on it. That is what `in` is for. I also noticed that `sort()` changes the original list. With source data, I'd want to keep an untouched copy first.
