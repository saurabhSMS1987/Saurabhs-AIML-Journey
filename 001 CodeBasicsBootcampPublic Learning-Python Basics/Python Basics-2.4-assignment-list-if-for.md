# Assignment: Lists, If Conditions and For Loops

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Python course**, covering the Lists, If Condition and Loops lectures.

In this assignment, I worked as Peter Pandey on eight tasks that combined lists, if conditions and loops.

## Results at a glance

| Task | What I did | Result |
| --- | --- | --- |
| 1 | Counted the Avengers with `len()` | 6 members |
| 2 | Added Spider-Man with `append()` | 7 members, with Spider-Man last |
| 3 | Moved Captain America to the front with `pop()` and `insert()` | Captain America leads the list |
| 4 | Moved Black Widow between Hulk and Thor | `['Captain America', 'Iron Man', 'Hulk', 'Black Widow', 'Thor', ...]` |
| 5 | Indexed and sliced student scores | First 92, last 84, first three `[92, 85, 76]`, roll 3 to 5 `[76, 58, 89]` |
| 6 | Appended a new score of 83 | 9 scores |
| 7 | Counted grades with a loop and `elif` | A: 2, B: 4, C: 2, D: 0, F: 1 |
| 8 | Built a reorder list for low-stock items | Pears, Grapes |

## Key code

**Moving an item with `pop()` and `insert()` (Task 3).** `pop()` removes an item by position and returns it, so I can put it somewhere else.

```python
avengers = ['Iron Man', 'Captain America', 'Black Widow', 'Hulk', 'Thor', 'Hawkeye', 'Spider-Man']
captain = avengers.pop(1)
avengers.insert(0, captain)
print(avengers[:2])   # ['Captain America', 'Iron Man']
```

**Counting grades (Task 7).** Checking from the highest band down means each `elif` only needs a lower bound.

```python
scores = [92, 85, 76, 58, 89, 91, 73, 84, 83]
grade_A = grade_B = grade_C = grade_D = grade_F = 0

for score in scores:
    if score >= 90:
        grade_A += 1
    elif score >= 80:
        grade_B += 1
    elif score >= 70:
        grade_C += 1
    elif score >= 60:
        grade_D += 1
    else:
        grade_F += 1

print(grade_A, grade_B, grade_C, grade_D, grade_F)   # 2 4 2 0 1
```

**Reorder list (Task 8).** The solution looped with `range(len())`. `zip()` from Lecture 6 does the same job and reads more clearly.

```python
product_names = ["Apples", "Bananas", "Oranges", "Pears", "Grapes"]
stock_levels = [20, 50, 15, 5, 8]
minimum_stock = 10

reorder_list = []
for product, stock in zip(product_names, stock_levels):
    if stock < minimum_stock:
        reorder_list.append(product)

print("Items to Reorder:")
for product in reorder_list:
    print(f"- {product}")   # Pears, Grapes
```

## What stuck with me

Tasks 7 and 8 follow the pattern I'll use most in audit work: loop through every record, test it against a rule, and collect the exceptions in a list. Replace the grades with claim bands and the stock levels with policy limits, and it's the same code.
