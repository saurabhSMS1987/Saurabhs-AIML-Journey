# Working with JSON in Python: My Advanced Python Notes

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Working With JSON** lecture from the **CodeBasics Advanced Python course**.

## Where I started

Most of the data I've read so far came in tables: CSV files and Excel sheets. But APIs, web apps and many modern systems send data as **JSON**: text that looks almost exactly like a Python dictionary, with nested lists and objects inside. This lecture showed how to turn JSON into Python data, how to write Python data back out as JSON, and what happens when the JSON is broken.

## The data in brief

- **A JSON string** describing one employee, Maulik: name, age, an employee flag, a list of skills and a nested address.
- **`output.json`:** a record for Bob, written to a file by the notebook.
- **`products.json`:** a list of **5 products** (wireless mouse, mechanical keyboard, USB-C charger, Bluetooth speaker and smartphone stand) with prices from $14.99 to $89.99. Four are in stock, across 3 categories.
- **A books response:** 3 books inside a `"books"` list, plus a `"status_code": 200`, shaped like a typical API reply.
- **A broken JSON string,** missing one comma, used to show error handling.

## What I learnt

**The four functions.** The `s` on the end stands for **string**:

| Function | Direction | Works with |
| --- | --- | --- |
| `json.loads(text)` | JSON → Python | A string |
| `json.dumps(obj)` | Python → JSON | A string |
| `json.load(file)` | JSON → Python | A file |
| `json.dump(obj, file)` | Python → JSON | A file |

```python
import json

record = json.loads(json_string)           # text -> dict
record["name"]                             # 'Maulik'

data_str = json.dumps(data)                # dict -> text

with open("output.json", "w") as file:
    json.dump(data, file, indent=4)        # indent=4 writes it neatly, one item per line

with open("products.json", "r") as file:
    products = json.load(file)             # a list of 5 dictionaries
products[1]["price"]                       # 89.99
```

**JSON and Python types map neatly:**

| JSON | Python |
| --- | --- |
| object `{...}` | `dict` |
| array `[...]` | `list` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |
| number | `int` or `float` |
| string | `str` |

**Picking fields from an API-style response:** the books list sat inside `data["books"]`, and a list comprehension kept only each book's title and author.

**Error handling:** one missing comma made `json.loads` fail with `JSONDecodeError: Expecting ',' delimiter: line 5 column 5`. Wrapping the call in `try` / `except json.JSONDecodeError` turns a crash into a clear message, and the error even points to the exact line and column.

## How this shows up in financial statement audit work

JSON is increasingly how audit evidence arrives: bank APIs, payment gateways, ERP exports and e-invoicing systems. These snippets use small sample data built in the code.

**1. Reading a bank API response and agreeing it to the ledger.**

```python
import json

bank_response = '''
{"account": "GB29-0001", "currency": "GBP", "status_code": 200,
 "transactions": [
    {"date": "2026-09-30", "ref": "RCPT-881", "amount": 12500.00},
    {"date": "2026-09-30", "ref": "PAY-412",  "amount": -4300.00},
    {"date": "2026-09-30", "ref": "PAY-413",  "amount": -860.50}
 ]}
'''

bank = json.loads(bank_response)
bank_movement = round(sum(t["amount"] for t in bank["transactions"]), 2)
ledger_movement = 7339.50

print(bank_movement, bank_movement == ledger_movement)   # 7339.5 True: the day's cash movement agrees
```

**2. Checking a nested invoice: does the header total match its lines?** ERP and e-invoicing exports nest the line items inside each invoice:

```python
invoices = json.loads('''
[{"invoice": "INV101", "total": 1500.00, "lines": [{"item": "Audit fee", "amount": 1500.00}]},
 {"invoice": "INV102", "total": 2400.00, "lines": [{"item": "Licence", "amount": 1800.00},
                                                    {"item": "Support", "amount": 500.00}]}]
''')

mismatches = [
    {"invoice": inv["invoice"], "header": inv["total"], "lines": sum(l["amount"] for l in inv["lines"])}
    for inv in invoices
    if inv["total"] != sum(l["amount"] for l in inv["lines"])
]
print(mismatches)   # [{'invoice': 'INV102', 'header': 2400.0, 'lines': 2300.0}]: lines are 100 short
```

**3. Loading a batch of records without one bad record stopping everything.** This is the lecture's `try` / `except`, applied record by record so the good ones still load and the bad ones are logged:

```python
raw_records = [
    '{"je_id": "JE01", "amount": 4200}',
    '{"je_id": "JE02" "amount": 98000}',          # missing comma
    '{"je_id": "JE03", "amount": 650}',
]

loaded, rejected = [], []
for line_no, text in enumerate(raw_records, start=1):
    try:
        loaded.append(json.loads(text))
    except json.JSONDecodeError as e:
        rejected.append(f"Record {line_no}: {e.msg}")

print(len(loaded), rejected)   # 2 ["Record 2: Expecting ',' delimiter"]: report this to the client
```

**4. Saving test parameters and results for the audit file.** Writing the thresholds used and the exceptions found to a JSON file makes the test easy to re-run and review. Dates aren't JSON types, so `default=str` converts them to text:

```python
from datetime import date

audit_run = {
    "test": "Large manual journal entries",
    "run_date": date(2026, 11, 1),
    "parameters": {"threshold": 50_000, "period": "FY2026"},
    "exceptions": ["JE02", "JE04"],
}

with open("je_test_results.json", "w") as f:
    json.dump(audit_run, f, indent=4, default=str)   # without default=str: TypeError for the date

with open("je_test_results.json") as f:
    print(json.load(f)["exceptions"])                 # ['JE02', 'JE04']
```

## My reflection

JSON turned out to be familiar territory. Once loaded, it's just the dictionaries and lists I already know, and the four functions are easy to remember once you know the `s` means "string". What I'll use most is the error handling: client data won't always be clean, and catching a bad record, logging it and carrying on is far better than having the whole test stop at record 2.

The nested-invoice check also showed something useful. JSON keeps related data together, an invoice and its lines in one place, which makes completeness checks like "do the lines add up to the header?" very natural to write.
