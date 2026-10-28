# Python Functions: My Lecture 7 Notes

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Functions** lecture from the **CodeBasics Python course**.

## Where I started

In the last lecture, I wrote a loop to total one person's expenses. This lecture asked: what happens when Sergey and Sundar both need totals? Copying the loop twice works, but it's messy and easy to get wrong. A function lets me write the logic once, give it a name, and reuse it on any data. It felt like turning a one-off workpaper into a standard audit program.

## What I learnt

**Defining and calling a function.** `def` creates it, and `return` sends back the answer:

```python
def find_total(expenses):
    '''Takes a list of expenses and returns their total.'''
    total = 0
    for expense in expenses:
        total += expense
    return total

find_total([30, 45, 70, 90])   # 235
find_total([40, 23, 10, 85])   # 158
```

**Docstrings.** The text in triple quotes explains what the function does, what it takes and what it returns. It's documentation that travels with the code.

**`return` vs `print`.** `print` only shows a value on screen, while `return` hands it back so I can store or reuse it. The cylinder example did both, so the volume appeared twice.

**Default arguments.** In `def find_cylinder_volume(radius, height=7)`, `height` is optional. If I leave it out, Python uses 7.

**Flexible arguments:**

| Syntax | What it accepts | Lecture example |
| --- | --- | --- |
| `*args` | Any number of values, received as a tuple | `sum_all(1, 2, 3, 4, 5)` gives 15 |
| `**kwargs` | Any number of named values, received as a dictionary | `company_info(ticker='AAPL', ceo='Tim Cook')` |

With `**kwargs`, I check `if 'ceo' in kwargs` before using a value, so missing details don't cause errors.

## How this shows up in insurance audit work

Audit tests get run again and again, across policies, branches and periods. Functions make each test reusable and consistent.

**1. A reusable loss ratio test.** I write it once and use it on every line of business.

```python
def loss_ratio(claims_paid, premiums_earned):
    '''Returns claims paid as a percentage of premiums earned.'''
    return round(claims_paid / premiums_earned * 100, 1)

print(loss_ratio(640000, 1000000))   # 64.0 (motor)
print(loss_ratio(1150000, 900000))   # 127.8 (property): investigate
```

**2. Authority check with a default limit.** The standard adjuster limit is the default, and senior staff can pass a higher one.

```python
def needs_escalation(claim_amount, authority_limit=50000):
    return claim_amount > authority_limit

print(needs_escalation(75000))           # True: standard adjuster
print(needs_escalation(75000, 100000))   # False: senior adjuster
```

**3. Total of any number of claims with `*args`.**

```python
def total_claims(*amounts):
    total = 0
    for amount in amounts:
        total += amount
    return total

print(total_claims(12000, 4500, 30000))   # 46500
```

**4. Claim summaries with optional details, using `**kwargs`.** Not every claim file has every field, so the function prints only what is there.

```python
def claim_summary(**details):
    for field in ["claim_id", "policy", "adjuster", "reserve"]:
        if field in details:
            print(f"{field}: {details[field]}")

claim_summary(claim_id="CL-1042", policy="P203", reserve=85000)
```

## My reflection

Functions feel like the point where my code becomes something I can share. A well-named function with a docstring is like a documented audit procedure: a colleague can run it without knowing how it works inside. The `return` vs `print` difference also clicked for me. A test that only prints a result is like a finding nobody wrote down. Returning the value means I can collect it, total it and report on it.

Next, I want to practise:

- [ ] Write a loss ratio function and run it for three lines of business
- [ ] Add docstrings to every function I write
- [ ] Turn the Lecture 6 claim-flagging loop into a reusable function
