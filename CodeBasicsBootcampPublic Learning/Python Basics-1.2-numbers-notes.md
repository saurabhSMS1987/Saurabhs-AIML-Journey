# Python Numbers: My Lecture 2 Notes

*Oct 25, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Numbers** lecture from the **CodeBasics Python course**.

## Where I started

Lecture 2 of the CodeBasics Python course was about numbers: how Python stores them and how to calculate with them. It opened with the area of a triangle, (1/2) × base × height, which gave 35.0. That `.0` was my first hint that division always returns a decimal. By the end, I was doing the kind of arithmetic I do in spreadsheets every week, just in code.

## What I learnt

Python has two kinds of numbers: `int` for whole numbers (`family_members = 5`) and `float` for decimals (`weight = 100.5`).

The arithmetic operators, using x = 10 and y = 3:

| Operator | Meaning | Result |
| --- | --- | --- |
| `x + y` | Add | 13 |
| `x - y` | Subtract | 7 |
| `x / y` | Divide (always a float) | 3.3333333333333335 |
| `x // y` | Floor divide (drop the remainder) | 3 |
| `x % y` | Remainder | 1 |
| `x ** y` | Power | 1000 |

Order of operations works as in school math: `10+2*3` is 16, while `(10+2)*3` is 36. Brackets make my intent clear.

Scientific notation is shorthand for very large or small numbers: `2.3e4` is 23000.0 and `2.3e-3` is 0.0023.

The lesson that surprised me most: numbers stored as text do not add up. `"120.34" + "500.67"` gave `'120.34500.67'`, two strings glued together. Wrapping each in `float()` fixed it and returned 621.01.

Other tools:

- `round(821.24)` gives 821.
- The `math` module adds `math.sqrt(16)` (4.0), `math.floor(3.7)` (3), `math.ceil(3.7)` (4) and `math.pi`.
- `dir(math)` lists everything the module offers.
- `format(5, 'b')` shows 5 in binary as `'101'`. The lecture also mentioned the IEEE floating point standard, which is why 10/3 ends in a stray 5.

## How this shows up in audit work

Most audit tests come down to arithmetic on amounts, and this lecture covered almost all of it. These snippets use the same tools on audit-style data.

**1. Totals from exported text.** Amounts from a CSV or ERP export often arrive as text. Without `float()` I would get the `'120.34500.67'` problem.

```python
amounts = ["1250.50", "980.25", "3100.00"]
total = float(amounts[0]) + float(amounts[1]) + float(amounts[2])
print(total)   # 5330.75
```

**2. Budget vs actual variance.** Brackets and `round()` give a clean percentage for analytical review.

```python
budget = 120000
actual = 134500
variance_pct = (actual - budget) / budget * 100
print(round(variance_pct, 2))   # 12.08
```

**3. Systematic sampling with `//` and `%`.** Floor division sets the interval, and the remainder picks every nth item.

```python
population = 1250
sample_size = 25
interval = population // sample_size   # 50
print(350 % interval == 0)            # True: item 350 is selected
```

**4. Rounding up and comparing decimals with `math`.** `math.ceil` never under-counts, and `math.isclose` avoids false reconciliation breaks caused by float precision.

```python
import math
total_value = 4_830_000
materiality = 250_000
print(math.ceil(total_value / materiality))   # 20, not 19.32

gl, tb = 0.1 + 0.2, 0.3
print(gl == tb)                # False, a float quirk
print(math.isclose(gl, tb))    # True
```

## My reflection

The text-plus-text moment stayed with me. Python did exactly what I told it to do and gave a confident, wrong-looking answer, with no error message. In audit, that is the most dangerous kind of mistake, so checking types before totalling is now a habit I want to keep.

Next, I want to practise:

- [ ] Total a column of exported amounts after converting them with `float()`
- [ ] Build a budget vs actual variance check with `round()`
- [ ] Pick a systematic sample using `//` and `%`
