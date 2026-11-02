# Takeaways: Advanced Python: JSON, Generators and Decorators

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Advanced: Generators, Decorators, JSON – Takeaways* from the **CodeBasics Advanced Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the second Advanced Python module, kept handy for quick revision.

## Working with JSON

- **JSON** (JavaScript Object Notation) is a lightweight format widely used to exchange data between servers and web applications.
- Python's `json` module converts both ways:

| Function | Direction | Works with |
| --- | --- | --- |
| `json.dumps()` | Python → JSON (encode) | A string |
| `json.loads()` | JSON → Python (decode) | A string |
| `json.dump()` | Python → JSON (serialize) | A file |
| `json.load()` | JSON → Python (deserialize) | A file |

- JSON supports basic types (strings, numbers, lists and dictionaries), which makes it flexible for storing and sending data.
- Catch `json.JSONDecodeError` when parsing, especially with data from untrusted sources.

## Generators and iterators

- An **iterator** is an object with `__iter__()` and `__next__()` methods. That's what lets a `for` loop step through it.
- A **generator** is a simple way to build an iterator: a function that **yields** values instead of returning one.
- `yield` pauses the function and saves its state until the next value is needed.
- Generators hold **one item at a time** in memory, while a list stores every element.
- They suit large datasets, infinite sequences and pipelines that transform data step by step.

## Decorators

- A **decorator** is a function that changes the behaviour of another function, method or class without permanently changing the original.
- It's applied with the clean `@decorator_name` syntax, just above the function definition.
- The takeaways also repeat a note from the first module: most IDEs, such as **PyCharm**, have built-in debugging support.

## All together

```python
import functools
import json

def log_call(func):                                   # decorator
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def large_entries(records, threshold):                # generator
    for r in records:
        if r["amount"] > threshold:
            yield r["je"]

raw = '[{"je": "JE1", "amount": 4200}, {"je": "JE2", "amount": 98000}, {"je": "JE3", "amount": 125000}]'
try:
    records = json.loads(raw)                         # JSON -> Python
    print(json.dumps(list(large_entries(records, 50_000))))   # Running large_entries / ["JE2", "JE3"]
except json.JSONDecodeError as e:
    print(f"Bad JSON: {e}")
```
