# Takeaways: Functions, Dictionaries, Tuples, Modules and File Handling

*Oct 27, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Basics: Functions, Dictionaries, Tuples, File Handling – Takeaways* from the **CodeBasics Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the third module, kept handy for quick revision.

## Functions

- `def name(parameters):` creates a function. Parameters make it reusable with different inputs.
- `return` sends a result back and exits the function.
- **Default parameters** give arguments a fallback value: `def f(x, limit=50000)`.
- Arguments can be **positional** (`f(75000, 100000)`) or **keyword** (`f(x=75000, limit=100000)`).
- `lambda` defines a small function in one line: `square = lambda x: x ** 2`.

## Tuples and dictionaries

- **Tuples** are immutable: items can't be changed, added or removed.
- **Dictionaries** are mutable **key: value** stores with fast lookup by key. They are Python's version of a hashmap.
- Dictionary keys must be **unique** and **immutable**: strings, numbers or tuples.
- Both support accessing items and looping over them.

## Modules and pip

- Modules organise code so it can be reused across programs.
- `import module_name` brings in built-in modules (like `math`) or external ones from [pypi.org](https://pypi.org/).
- `pip install package_name` installs external packages.

## File handling

`open(filename, mode)` is the key function. The modes are:

| Mode | Meaning | If the file... |
| --- | --- | --- |
| `"r"` | Read (default) | doesn't exist, it raises an error |
| `"a"` | Append | doesn't exist, it's created |
| `"w"` | Write (overwrites) | doesn't exist, it's created |
| `"x"` | Create | already exists, it raises an error |

Use `with open(...) as f:` so the file closes properly, even if an error happens.

## All together

```python
needs_review = lambda amount, limit=50000: amount > limit      # lambda with a default

claims = {"CL-01": 42000, "CL-02": 95000}                      # dictionary
flagged = []
for claim_id, amount in claims.items():
    if needs_review(amount):
        flagged.append(claim_id)

with open("review_list.txt", "w") as f:                        # file handling
    f.write(", ".join(flagged))                                # CL-02
```
