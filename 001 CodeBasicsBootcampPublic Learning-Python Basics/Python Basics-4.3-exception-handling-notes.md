# Python Exception Handling: Notes

*Oct 28, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Exception Handling** lecture from the **CodeBasics Python course**.

## Where I started

So far, any error stopped my code dead: a `ValueError` here, a `KeyError` there, and the whole script crashed. This lecture taught me to expect errors and handle them gracefully. I can also raise my own errors when a business rule is broken. It felt like the shift from hoping the data is clean to planning for when it isn't, which is exactly how audit work goes.

## What I learnt

**try / except.** The risky code goes in `try`, and the response to each type of error goes in its own `except`:

```python
try:
    z = int(x) / int(y)
except ZeroDivisionError as ze:   # specific errors first
    print("Exception occurred:", ze)
    z = 0
except TypeError as te:
    print("Exception occurred:", te)
    z = 0
except Exception as e:            # catch-all last
    print("Generic exception occurred:", e)
    z = 0
```

Python checks the `except` blocks in order, so the specific ones come first and the generic `Exception` comes last as a safety net. `as e` captures the error message so I can report it.

**finally** always runs, whether an error happened or not. It's used for clean-up, such as closing a file.

**Raising exceptions.** `raise` stops the code on purpose when a rule is broken:

```python
if amount <= 0:
    raise ValueError("Amount must be positive")
```

**Custom exceptions.** Inheriting from `Exception` (Lecture 12) creates my own error type with a meaningful name:

```python
class InsufficientFunds(Exception):
    pass

raise InsufficientFunds(f"Not enough funds. Current balance {balance}")
```

In the lecture's bank example, the deposits of 10 and 7 worked, but withdrawing 50 raised `InsufficientFunds: Not enough funds. Current balance 17`. Nothing caught it, so the script stopped before printing the balance.

**Common built-in exceptions:**

| Exception | When it happens |
| --- | --- |
| `ZeroDivisionError` | Dividing by zero |
| `TypeError` | Mixing incompatible types, such as `'baby yoda' + 56` |
| `ValueError` | Right type, wrong value, such as `int("abc")` |
| `FileNotFoundError` | Opening a file that doesn't exist |

**Two bugs I found in the lecture files**, both worth learning from:

1. `exception_tutorial.py` has a stray backtick in `print("Generic exception occured: ",e`)`. That's a `SyntaxError`, so the file doesn't run at all. No `try` can catch a syntax error, because Python reads the whole file before running any of it.
2. The `finally: file.close()` block breaks when the file is missing. `open()` failed, so `file` was never created, and `finally` then raises a `NameError`. Using `with open(...)` avoids this, because it closes the file safely on its own.

## How this shows up in insurance audit work

Real claims extracts always have bad rows, zero values and missing files. Exception handling keeps one bad record from stopping the whole test, while still recording it.

**1. Loading amounts without crashing on bad rows.**

```python
raw_amounts = ["12000", "4500", "N/A", "30000", ""]
clean, rejected = [], []

for row, value in enumerate(raw_amounts, start=1):
    try:
        clean.append(int(value))
    except ValueError:
        rejected.append(row)           # keep a record for the data quality finding

print(clean)      # [12000, 4500, 30000]
print(rejected)   # [3, 5]: rows to raise with the client
```

**2. Loss ratios when premium is zero.**

```python
def loss_ratio(claims, premium):
    try:
        return round(claims / premium * 100, 1)
    except ZeroDivisionError:
        return "No premium: check for unearned or cancelled policy"

print(loss_ratio(640000, 1000000))   # 64.0
print(loss_ratio(85000, 0))          # No premium: check ...
```

**3. A custom exception for a broken business rule.** The payment function refuses to pay above the sum insured.

```python
class ExceedsSumInsured(Exception):
    pass

def approve_payment(claim_id, amount, sum_insured):
    if amount > sum_insured:
        raise ExceedsSumInsured(f"{claim_id}: {amount} exceeds the sum insured of {sum_insured}")
    return f"{claim_id}: approved"

for claim_id, amount, limit in [("CL-01", 42000, 50000), ("CL-02", 260000, 250000)]:
    try:
        print(approve_payment(claim_id, amount, limit))
    except ExceedsSumInsured as e:
        print("Exception:", e)
```

**4. A missing extract, handled safely.**

```python
try:
    with open("claims_q3.csv", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("claims_q3.csv not received: follow up with the client")
```

## My reflection

This lecture changed how I see errors. In audit, an exception is often the finding itself: a non-numeric amount, a policy with zero premium, a payment above the limit. So the goal isn't to hide errors. It's to catch them, keep the test running and **record** what went wrong. Finding the two bugs in the lecture files also showed me something: error handling only helps if the code around it is correct too. A `finally` block can cause its own error.
