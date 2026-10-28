# Assignment 3: Functions, Dictionaries, Tuples and File Handling

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Python course**, covering the Functions, Tuples and Dictionaries, and File Handling lectures.

As Peter Pandey, I built a small customer loyalty program that reads spending from a file and gives each customer a reward level.

## Tasks at a glance

| Task | What I did | Tools |
| --- | --- | --- |
| 1 | Read `customers.txt` into a dictionary of name and amount | `with open()`, `strip()`, `split()`, `int()` |
| 2 | Wrote `calculate_rewards()` to return a reward level | `def`, `if` / `elif` / `else`, `return` |
| 3 | Built a summary dictionary of name and (amount, level) | Dictionary loop, tuples |
| 4 | Combined everything into `process_customer_data(file_name)` | One reusable function |

Reward levels: **Gold** for $500 and above, **Silver** for $200 to $499, **Bronze** for $100 to $199, and **None** below $100.

## Final code

```python
def calculate_rewards(total):
    if total >= 500:
        return "Gold"
    elif total >= 200:
        return "Silver"
    elif total >= 100:
        return "Bronze"
    else:
        return "None"


def process_customer_data(file_name):
    customer_summary = {}
    with open(file_name, "r") as f:
        for line in f:
            name, amount = line.strip().split(",")
            amount = int(amount)
            customer_summary[name] = (amount, calculate_rewards(amount))
    return customer_summary


print(process_customer_data("customers.txt"))
```

Output with the 7 customers in `customers.txt`:

```
{'Srinivas': (120, 'Bronze'), 'John': (250, 'Silver'), 'Maria': (150, 'Bronze'),
 'Smith': (510, 'Gold'), 'Anjali': (45, 'None'), 'Navin': (100, 'Bronze'),
 'Santosh': (99, 'None')}
```

Navin (exactly 100) and Santosh (99) are useful edge cases, since they sit on either side of the Bronze boundary.

## What I fixed in the solution

The solution's Task 4 function created a `rewards_data` dictionary but never used it. Instead, it wrote into `customers_dict` from Task 1, which lives outside the function. That only works if Task 1 has already run, and reading a second file would mix two customer lists together. My version keeps everything inside the function, so it works on its own for any file.

## What stuck with me

This is the full shape of an audit test: read the data, apply a rule, and return a labelled result. Replace the reward levels with claim authority bands, and it's the same code. The boundary cases (99 vs 100) are exactly where I'd focus testing in a real control.
