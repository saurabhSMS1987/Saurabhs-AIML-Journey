# Assignment 1: Variables, Numbers and Strings

*Oct 25, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Python course**, covering the Variables, Numbers and Strings lectures.

This assignment pulled the first three lectures together in 10 short tasks.

## Results at a glance

| Task | What I did | Result |
| --- | --- | --- |
| 1 | Stored `pi = 22/7` and checked its type | `3.142857142857143`, a `float` |
| 2 | Tried `for = 4` | `SyntaxError`, because `for` is a reserved keyword |
| 3 | Simple interest on 567.00 at 5.6% for 3 years | Interest 95.256, total 662.256 |
| 4 | Area of a pond with an 84 m radius (pi = 3.14) | 22,155.84 m² |
| 5 | Water in the pond at 2,000 litres per m² | 44,311,680 litres |
| 6 | Speed crossing 490 m in 7 minutes | 1.17 m/s |
| 7 | f-string with daily fruit and vegetable counts | `I eat 4 vegetables and 2 fruits daily` |
| 8 | Sliced the Himalayas sentence | `The Himalayas`, `mountain range`, `The Himalayas on the planet.` |
| 9 | Fixed "9 planets" with `replace()` | `There are 8 planets in the solar system` |
| 10 | Daily sales summary for three products | Total sales: $890.0 |

## Key code

**Simple interest (Task 3).** Python printed `95.25599999999999`, the float precision quirk from Lecture 2.

```python
principal_amount = 567.00
rate_of_interest = 5.6
time = 3

simple_interest = principal_amount * rate_of_interest * time / 100
total_amount = principal_amount + simple_interest
print(round(simple_interest, 2), round(total_amount, 2))   # 95.26 662.26
```

**Unit conversion and rounding (Task 6).**

```python
speed = 490 / (7 * 60)    # convert minutes to seconds first
print(round(speed, 2))    # 1.17
```

**Formatted sales summary (Task 10).**

```python
product1_total = 20.0 * 15
product2_total = 35.0 * 10
product3_total = 12.0 * 20
day_total = product1_total + product2_total + product3_total

print("Daily Sales Summary:")
print(f"- Product 1: Sold 15 units at $20.0 each, Total: ${product1_total}")
print(f"- Product 2: Sold 10 units at $35.0 each, Total: ${product2_total}")
print(f"- Product 3: Sold 20 units at $12.0 each, Total: ${product3_total}")
print(f"Total Sales for the Day: ${day_total}")   # $890.0
```

## What stuck with me

Task 10 felt closest to my day job: quantity × price for each line, a total, and a clear summary someone else can check. Task 3 was a good reminder to round money before reporting it, since raw floats can carry tiny precision errors.
