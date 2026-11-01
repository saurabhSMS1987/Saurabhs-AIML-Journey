# Decorators: My Advanced Python Notes

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Decorators** lecture from the **CodeBasics Advanced Python course**. `functools.wraps` and `functools.lru_cache` come from the [Python `functools` documentation](https://docs.python.org/3/library/functools.html).

## Where I started

The lecture began with a familiar annoyance: two functions, `get_square` and `get_cube`, each with the **same timing code** copied into it: record the start time, do the work, record the end time, print the difference. A **decorator** removes that repetition. You write the extra behaviour once and attach it to any function with a single `@` line, without touching the function's own logic.

## The code in brief

The examples squared and cubed numbers: a 5-item list, and then `range(100000)`, so the timings were large enough to see. For 100,000 numbers, each function took roughly **12–15 milliseconds** in the lecture's run.

## What I learnt

**Without a decorator,** the timing logic is mixed into every function:

```python
def get_square(numbers):
    start = time.time()
    result = [n * n for n in numbers]
    end = time.time()
    print(f"get_square took {(end - start) * 1000} ms")
    return result
# get_cube repeats the same four timing lines
```

**With a decorator,** the timing logic lives in one place:

```python
import time

def timer(func):                          # takes a function...
    def wrapper(*args, **kwargs):         # ...builds a new one around it...
        start = time.time()
        result = func(*args, **kwargs)    # ...runs the original...
        end = time.time()
        print(f"Function {func.__name__} took {(end - start) * 1000} ms")
        return result                     # ...and passes its result back
    return wrapper

@timer                                    # same as: get_square = timer(get_square)
def get_square(numbers):
    return [n * n for n in numbers]
```

**How it fits together:**

| Piece | Role |
| --- | --- |
| `timer(func)` | The decorator: a function that takes a function and returns a new one |
| `wrapper(*args, **kwargs)` | The new function: accepts any arguments and passes them on |
| `@timer` | Shorthand for `get_square = timer(get_square)` |
| `return result` | Keeps the original function's output |

Multiplying by 1,000 turns seconds into **milliseconds**, so I've labelled the output "ms". The lecture printed "seconds", but the numbers are milliseconds.

**Where decorators are commonly used,** from the lecture:

1. Measuring how long a function takes
2. Logging
3. Access control
4. Caching

**One addition worth making:** wrap `wrapper` with `@functools.wraps(func)`. Without it, the decorated function's name and docstring are replaced by the wrapper's, so `get_square.__name__` would say `"wrapper"`. The snippets below use it.

## How this shows up in financial statement audit work

All four common uses map onto audit work: timing tests, keeping an audit trail, enforcing preconditions and avoiding repeated lookups. These snippets use small sample data built in the code.

**1. An automatic audit trail for every test.** A logging decorator records what ran, with which parameters, how many exceptions it found and when. That's documentation the reviewer gets for free:

```python
import functools
from datetime import datetime

audit_log = []

def log_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        audit_log.append({"test": func.__name__, "parameters": kwargs,
                          "exceptions": len(result), "run_at": datetime.now().strftime("%Y-%m-%d %H:%M")})
        return result
    return wrapper

journal_entries = [
    {"je": "JE01", "amount": 4_200,   "approver": "K. Wong", "weekday": 2},
    {"je": "JE02", "amount": 98_000,  "approver": None,      "weekday": 5},
    {"je": "JE03", "amount": 125_000, "approver": "D. Smith", "weekday": 6},
    {"je": "JE04", "amount": 9_950,   "approver": "K. Wong", "weekday": 1},
]

@log_test
def large_entries(entries, threshold=50_000):
    return [e["je"] for e in entries if e["amount"] > threshold]

@log_test
def missing_approver(entries):
    return [e["je"] for e in entries if not e["approver"]]

large_entries(journal_entries, threshold=50_000)
missing_approver(journal_entries)
for record in audit_log:
    print(record["test"], record["parameters"], record["exceptions"])
# large_entries {'threshold': 50000} 2
# missing_approver {} 1
```

**2. A precondition check before any test runs** (the "access control" idea). This decorator refuses to run a test on a ledger that doesn't balance, because testing an incomplete population gives misleading results:

```python
def requires_balanced(func):
    @functools.wraps(func)
    def wrapper(lines, *args, **kwargs):
        difference = round(sum(lines), 2)
        if difference != 0:
            raise ValueError(f"{func.__name__} stopped: ledger out of balance by {difference:,.2f}")
        return func(lines, *args, **kwargs)
    return wrapper

@requires_balanced
def total_debits(lines):
    return sum(x for x in lines if x > 0)

print(total_debits([5_000, -3_000, -2_000]))            # 5000
try:
    total_debits([5_000, -3_000, -1_500])
except ValueError as e:
    print(e)                                            # total_debits stopped: ledger out of balance by 500.00
```

**3. Timing a full-population test.** This is the lecture's `timer`, used to show how long a test takes as the data grows:

```python
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {(time.perf_counter() - start) * 1000:.1f} ms")
        return result
    return wrapper

@timer
def round_amount_test(amounts):
    return [a for a in amounts if a >= 10_000 and a % 1_000 == 0]

flagged = round_amount_test(list(range(0, 2_000_000, 7)))
print(len(flagged))                                     # 284: round amounts of 10,000 or more
```

`time.perf_counter()` is more precise than `time.time()` for measuring short durations.

**4. Caching repeated lookups.** Python's built-in `functools.lru_cache` is a ready-made caching decorator. Here it stops an exchange-rate lookup from being repeated for every transaction in the same currency:

```python
lookups = 0

@functools.lru_cache(maxsize=None)
def fx_rate(currency):
    global lookups
    lookups += 1                                        # imagine a slow call to a rates file or API
    return {"USD": 0.79, "EUR": 0.85, "GBP": 1.0}[currency]

transactions = [("USD", 1_000), ("EUR", 2_500), ("USD", 400), ("USD", 7_200), ("EUR", 300)]
gbp_total = sum(amount * fx_rate(ccy) for ccy, amount in transactions)
print(round(gbp_total, 2), lookups)                     # 9174.0 2: five conversions, but only two lookups
```

## My reflection

Decorators felt abstract at first, a function that takes a function and returns a function. The `@timer` example made it concrete: the **what** (squaring numbers) stays separate from the **how it's monitored** (timing it).

The audit trail decorator is the one I'll actually use. Every test I write can record its own parameters, its results and when it ran, without me remembering to do it each time. That's exactly the kind of consistent, reviewable evidence a workpaper needs.
