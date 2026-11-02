# Takeaways: Advanced Python: Comprehensions, Sets, PEP 8 and Debugging

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Advanced: Comprehensions, Sets – Takeaways* from the **CodeBasics Advanced Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the first Advanced Python module, kept handy for quick revision.

## Sets and frozensets

- A **set** is a mutable collection of **unique** values, with fast membership checks, additions and deletions.
- Sets change through `add()`, `remove()` and `update()`.
- A **frozenset** is an immutable set. It has no methods that change its contents, so it's **hashable** and can be a dictionary key or a set element.
- Both support **union** (`|`), **intersection** (`&`), **difference** (`-`) and **symmetric difference** (`^`).
- They're the right choice whenever you need non-repeating values and fast lookups.

## List, dict and set comprehensions

- A **list comprehension** builds a list by running a `for` loop in a single line.
- **Dictionary** and **set** comprehensions work the same way, and a set comprehension removes duplicates automatically.
- Comprehensions are generally **more readable and faster** than building a collection with a loop.
- All comprehensions can include a condition to **filter** items.

## PEP 8 naming conventions

| Name type | Style | Example |
| --- | --- | --- |
| Class | `CamelCase` | `JournalEntry` |
| Function or variable | `lowercase_with_underscores` | `calculate_total`, `total_amount` |
| Constant | `ALL_CAPS` | `APPROVAL_LIMIT` |

Following one standard makes code easier for others to read and maintain. Teams often enforce it through code reviews and linters.

## Debugging with PyCharm

- Debugging lets you **watch the code as it runs**, to find bugs and troubleshoot issues.
- Most IDEs, including **PyCharm**, have a built-in debugger.
- A **conditional breakpoint** pauses only when a condition is true.

## All together

```python
APPROVAL_LIMIT = 10_000                                   # constant: ALL_CAPS

def flag_large_entries(entries):                          # function: lowercase_with_underscores
    return [je for je, amount in entries if amount > APPROVAL_LIMIT]   # list comprehension with a filter

entries = [("JE1", 4_200), ("JE2", 25_000), ("JE3", 9_800)]
q1_vendors = {"V01", "V02", "V03"}
q2_vendors = {"V02", "V03", "V04"}

print(flag_large_entries(entries))        # ['JE2']
print(sorted(q1_vendors ^ q2_vendors))    # ['V01', 'V04']: vendors used in only one quarter
print({je: amt for je, amt in entries})   # dictionary comprehension
```
