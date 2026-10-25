# Python Strings: My Lecture 3 Notes

*Oct 25, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Strings** lecture from the **CodeBasics Python course**.

## Where I started

This lecture was about strings, Python's way of holding text. Numbers felt like my comfort zone. Text is where audit data gets messy: vendor names with extra spaces, descriptions typed in a hurry, IDs exported in odd formats. By the end, I had tools to clean, search and slice all of it.

## What I learnt

**Joining text.** `first + " " + last` gave `"Mohan Sharma"`. An f-string does the same job more neatly: `f'{first} {last} is {age} years old'`.

**Indexing and slicing.** Each character has a position, starting at 0. Negative positions count from the end.

| Code | Result | What it does |
| --- | --- | --- |
| `name[0]` | `'M'` | First character |
| `name[0:5]` | `'Mohan'` | Positions 0 to 4 (the end is excluded) |
| `name[6:]` | `'Sharma'` | From position 6 to the end |
| `name[-1]` | `'a'` | Last character |
| `len(name)` | `12` | Number of characters |

`name[12]` raised an `IndexError`, since the last valid position is 11.

**Strings are immutable.** `name[0] = 'S'` failed with a `TypeError`. To change text, I create a new string instead, for example with `replace()`.

**Quotes.** Double quotes let me use an apostrophe inside (`"dhaval's favourite food"`), and single quotes allow double quotes inside. Triple quotes hold text across several lines.

**Useful methods:**

- `"cardamom" in recipe` checks whether a word appears (`True` or `False`).
- `replace("100$", "50$")` swaps text, `upper()` changes the case, and `index('was')` finds a position.
- `'410'.isdigit()` is `True`, while `'410a'.isdigit()` is `False`.
- `split("|")` breaks `"AAPL|NVDA|RIL|GOGL"` into a list of four tickers.
- `strip()` removes spaces at the start and end.
- `endswith(".pdf")` checks a file type.
- `"my age is:" + 38` fails. `str(38)` converts the number first, so the join works.
- `\n` starts a new line, and `\t` adds a tab.

## How this shows up in audit work

Most data quality problems I meet are text problems. These snippets use the lecture's tools on audit-style data.

**1. Catching duplicate vendors.** The same vendor typed two ways looks like two vendors until I clean the text.

```python
vendor_a = "  ABC Supplies "
vendor_b = "abc supplies"
print(vendor_a == vendor_b)                                  # False
print(vendor_a.strip().lower() == vendor_b.strip().lower())  # True: possible duplicate
```

**2. Keyword scan of journal entry descriptions.** Words like "adjustment" or "override" are common red flags in journal testing.

```python
description = "Manual ADJUSTMENT per CFO request"
print("adjustment" in description.lower())   # True: flag for review
```

**3. Validating and slicing invoice numbers.** Slicing pulls out the year, and `isdigit()` confirms the serial is clean.

```python
invoice_id = "INV-2026-00153"
year = invoice_id[4:8]
serial = invoice_id[-5:]
print(year, serial, serial.isdigit())   # 2026 00153 True
```

**4. Splitting pipe-delimited exports.** Many systems export records with `|` between fields.

```python
record = "JE1042|2026-09-30|Revenue|125000"
fields = record.split("|")
print(fields[2], float(fields[3]))   # Revenue 125000.0
```

**5. Clear exception messages.** f-strings turn a test result into a sentence a reviewer can read.

```python
vendor = "ABC Supplies"
amount = 75000
print(f"Exception: {vendor} invoice of {amount} exceeds the approval limit")
```

## My reflection

The duplicate-vendor example made this lecture click for me. To Python, `"ABC Supplies "` and `"abc supplies"` are different until I tell it otherwise, and most of my data cleaning is exactly that kind of telling. I also liked that strings cannot be changed in place. That feels a bit like an audit trail: the original stays as it was, and every change becomes a new version.

Next, I want to practise:

- [ ] Clean a vendor master list with `strip()` and `lower()`, then look for duplicates
- [ ] Scan a set of journal entry descriptions for red-flag keywords
- [ ] Split a pipe-delimited export and convert the amount field with `float()`
