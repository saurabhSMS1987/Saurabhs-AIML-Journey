# Takeaways: Lists, If Conditions and For Loops

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Basics: List, If Condition, For Loop – Takeaways* from the **CodeBasics Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the second module, kept handy for quick revision.

## Lists

- Lists store **sequential** data, and they are **ordered**: each item keeps its position unless I change it.
- Lists are **heterogeneous**, so one list can mix types: `["car", 4.5, True]`.
- Lists are **mutable**: items can be added, removed or changed in place.
- Slicing uses `list[start:end:step]`. For example, `scores[::2]` takes every second item.

## If conditions

- `if` runs a block only when its condition is true.
- `elif` adds further checks when the first one fails.
- `else` is the fallback when every condition above it is false.
- `and`, `or` and `not` combine conditions.
- A **nested if**, one `if` inside another, checks conditions in layers.

## For loops

- A `for` loop runs a block once for each item in a list, tuple or string.
- `range()` produces a sequence of numbers, so a loop can repeat a set number of times.
- `break` exits the loop, and `continue` skips to the next pass.
- `enumerate()` gives both the position and the item.

## All three together

```python
claims = [0, 15000, 72000, 3000, 95000]

for i, amount in enumerate(claims):
    if amount == 0:
        continue                        # skip nil claims
    if amount > 50000:
        if amount > 90000:              # nested if
            print(f"Row {i+1}: {amount} needs committee review")
        else:
            print(f"Row {i+1}: {amount} needs senior review")

print(claims[1::2])                     # [15000, 3000]: every second claim from position 1
```
