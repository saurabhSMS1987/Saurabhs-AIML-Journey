# Takeaways: Variables, Numbers and Strings

*Oct 25, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Basics: Variables, Numbers & Strings – Takeaways* from the **CodeBasics Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the first module, kept handy for quick revision.

## Variables

Variables are containers that store data in a program. Naming rules:

- No reserved words such as `def` or `True`.
- Start with a letter or `_`.
- No spaces or special characters (`@`, `#`, `$`, `%`).
- `_` is allowed anywhere in the name.

## Numbers

| Concept | Example | Result |
| --- | --- | --- |
| `int`: whole number | `57` | `int` |
| `float`: has a decimal part | `57.23` | `float` |
| Check the type | `type(57.23)` | `float` |
| Division | `10 / 3` | `3.333...` |
| Floor division (integer part) | `10 // 3` | `3` |
| Modulo (remainder) | `10 % 3` | `1` |
| Power | `10 ** 3` | `1000` |
| Type casting | `float("10.2")` | `10.2` |

`int()`, `float()` and `str()` convert between types. The `math` module adds functions such as `sqrt`, `floor` and `ceil`.

## Strings

- Strings are **immutable**: they can't be changed once created.
- Indexing and slicing pick out parts: `name[0]`, `name[1:5]`.
- f-strings make text easy to build: `f"{variable}"`.
- Built-in methods include `.upper()`, `.lower()`, `.split()` and `.strip()`.

```python
name = "  Mohan Sharma "
clean = name.strip()
print(clean[0], clean[0:5], clean.upper())   # M Mohan MOHAN SHARMA
print(f"Hello, {clean.split()[0]}!")         # Hello, Mohan!
```
