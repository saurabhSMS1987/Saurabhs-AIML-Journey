# Python Loops: My Lecture 6 Notes

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Loops** lecture from the **CodeBasics Python course**.

## Where I started

The lecture began by adding four monthly expenses by hand: `expenses[0] + expenses[1] + ...`. That is fine for four values but impossible for a full claims register. Loops fixed this by repeating the same step for every item. Together with last lecture's if conditions, I can now apply an audit test to every row of a dataset, not just one.

## What I learnt

**for loop.** Goes through a list one item at a time. With `+=`, it builds a running total:

```python
total_expense = 0
for expense in expenses:
    total_expense += expense   # same as total_expense = total_expense + expense
```

**Ways to loop:**

| Tool | What it gives me | Example |
| --- | --- | --- |
| `for x in list` | Each item | `for expense in expenses` |
| `range(len(list))` | Each position, so I index the list myself | `for i in range(len(expenses))` |
| `enumerate(list)` | Position and item together | `for i, expense in enumerate(expenses)` |
| `zip(list1, list2)` | Matching items from two lists | `for sales, month in zip(monthly_sales, months)` |

`enumerate` starts at 0, which is why the lecture printed `Month {i+1}`.

**break** stops the loop entirely. The sales example stopped at the first month below the threshold (33 in March) and never checked April to June.

**continue** skips the rest of the current pass and moves to the next item. `if i % 2 == 0: continue` printed only odd numbers from `range(1, 11)`.

**while loop.** Repeats for as long as a condition stays true. `while n <= 10` printed 0 to 10. I must update `n` inside the loop, or it never ends.

## How this shows up in insurance audit work

Loops turn a one-off check into a test of the whole population. These snippets apply them to claims data.

**1. Total claims paid on a policy.**

```python
claims_paid = [12000, 4500, 30000, 8200]
total_paid = 0
for claim in claims_paid:
    total_paid += claim
print("Total claims paid:", total_paid)   # 54700
```

**2. Flagging large claims, skipping nil claims.** `enumerate` gives the row number for my working papers, and `continue` skips claims closed without payment.

```python
claims = [0, 15000, 72000, 0, 95000]
for i, amount in enumerate(claims):
    if amount == 0:
        continue
    if amount > 50000:
        print(f"Row {i+1}: claim of {amount} needs senior review")
```

**3. Claims paid above the sum insured.** `zip` pairs each claim with its policy limit, so overpayments stand out.

```python
policy_ids = ["P101", "P102", "P103"]
claims = [40000, 260000, 90000]
sums_insured = [50000, 250000, 100000]

for policy, claim, limit in zip(policy_ids, claims, sums_insured):
    if claim > limit:
        print(f"{policy}: paid {claim}, over the sum insured of {limit}")
```

**4. Finding one policy and stopping.** `break` ends the search at the first match, so the rest of the register isn't read for nothing.

```python
policy_register = ["P201", "P202", "P203", "P204"]
for policy in policy_register:
    if policy == "P203":
        print("Found P203: pulling the policy file")
        break
```

**5. When the aggregate limit runs out.** A `while` loop processes claims until the policy's annual aggregate is used up.

```python
claims = [30000, 45000, 20000, 25000]
aggregate_limit = 100000
paid = 0
i = 0
while i < len(claims) and paid + claims[i] <= aggregate_limit:
    paid += claims[i]
    i += 1
print(f"{i} claims paid ({paid}). Claim {i+1} would breach the aggregate limit.")
```

## My reflection

This lecture changed how I think about sampling. With a loop, testing all 10,000 claims takes no more effort than testing 25. I also need to think about `break` carefully. The sales example stopped at the first problem and never looked at the later months. In an audit, I usually want every exception, not just the first one. So I'll use `break` for searches and keep looping through everything for exception testing.
