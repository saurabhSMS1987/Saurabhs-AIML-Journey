# Python Modules: My Lecture 9 Notes

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Modules** lecture from the **CodeBasics Python course**.

## Where I started

In Lecture 7, I learnt to write my own functions. This lecture showed that I don't have to write everything myself. Python comes with ready-made toolkits called modules, and thousands more can be installed. With one `import` line, I can borrow code that experts have already written and tested. It felt like picking up the firm's standard audit templates instead of building every workpaper from scratch.

## What I learnt

**Built-in modules** come with Python. I just import them:

| Code | Result |
| --- | --- |
| `math.sqrt(16)` | `4.0` |
| `math.pow(5, 3)` | `125.0` |
| `math.log10(1000)` | `3.0` |
| `math.pi` | `3.141592653589793` |
| `calendar.month(2022, 1)` | A printed calendar for January 2022 |
| `calendar.isleap(2024)` | `True` |

`dir(module)` lists everything a module offers, and it's the quickest way to explore a new one.

**External modules** are built by others and installed first, for example with `pip install numpy`. The lecture used **NumPy**, which handles tables of numbers (arrays) in one step:

```python
import numpy as np

q1 = np.array([[200, 220, 250], [150, 180, 210], [300, 330, 360]])
q2 = np.array([[209, 231, 259], [155, 192, 222], [310, 340, 375]])

q1 + q2   # half-year sales for every product and region at once
q2 - q1   # growth in every cell, with no loop needed
```

`import numpy as np` gives the module a short nickname, which is the standard convention.

## How this shows up in insurance audit work

These modules already cover several everyday insurance calculations.

**1. Sample sizes with `math.ceil`.** A sample size must always round up, never down.

```python
import math

population_value = 4_830_000
sampling_interval = 250_000
sample_size = math.ceil(population_value / sampling_interval)
print(sample_size)   # 20, not 19
```

**2. Earned premium with `calendar`.** Leap years change the daily premium rate, which is easy to get wrong in a manual check.

```python
import calendar

annual_premium = 36600
days_in_year = 366 if calendar.isleap(2024) else 365
days_in_force = calendar.monthrange(2024, 2)[1]   # 29 days in Feb 2024
earned = annual_premium / days_in_year * days_in_force
print(round(earned, 2))   # 2900.0
```

**3. Claims movement by line and region with NumPy.** This works like the lecture's sales example, using claims counts instead.

```python
import numpy as np

# rows: motor, property, health | columns: North, South, West
q1_claims = np.array([[120, 95, 80], [40, 35, 30], [210, 190, 175]])
q2_claims = np.array([[126, 97, 112], [42, 34, 31], [215, 260, 180]])

growth_pct = (q2_claims - q1_claims) / q1_claims * 100
print(np.round(growth_pct, 1))
print(growth_pct > 25)   # True marks cells for analytical review
```

**4. Loss ratios for every line in one line of code.**

```python
claims = np.array([640000, 1150000, 820000])
premiums = np.array([1000000, 900000, 1100000])
loss_ratios = np.round(claims / premiums * 100, 1)
print(loss_ratios)   # [ 64.  127.8  74.5]
```

## My reflection

NumPy was the eye-opener. The growth table that took a nested loop in earlier lectures took one line here. With claims data, that means I can compare whole quarters across every line and region at once and spend my time on the cells that stand out. I'm also learning that knowing what already exists, by exploring with `dir()` and reading the docs, is a skill in itself.

Next, I want to practise:

- [ ] Use `dir()` to explore the `statistics` module and find something useful for audit
- [ ] Recalculate a sample of earned premiums with `calendar`, including a leap year
- [ ] Build a NumPy table of claims by line and region and flag big movements
