# Debugging Python Code: My Advanced Python Notes

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Debugging** lecture from the **CodeBasics Advanced Python course**. The `pdb` commands come from the [Python `pdb` documentation](https://docs.python.org/3/library/pdb.html).

## Where I started

Until now, when my code gave a wrong answer, I added `print()` statements and guessed. This lecture showed a better way: **pause the program while it runs**, step through it one line at a time, and watch each variable change. It felt like the difference between reading a finished report and sitting with the preparer while they build it.

## The code in brief

The lecture used one short script, `debugging_tutorial.py`. It adds up four prices and subtracts a discount:

```python
def calculate_total(prices, discount):
    total = 0
    for price in prices:
        total += price
    total -= discount
    return total


if __name__ == "__main__":
    prices = [10.99, 5.49, 3.99, 2.49]
    discount = 2.00
    total_price = calculate_total(prices, discount)
    print(f"Total price after discount: ${total_price:.2f}")   # $20.96
```

Stepping through the loop shows `total` grow from 0 to 10.99, 16.48, 20.47 and 22.96. The $2.00 discount then brings it to **$20.96**.

## What I learnt

**Debugging means finding where the code does something different from what you expect.** A debugger lets you check that at every step instead of only at the end.

**Key debugger ideas:**

| Idea | What it does |
| --- | --- |
| **Breakpoint** | Pauses the program at a chosen line |
| **Step over** | Runs the current line, then pauses on the next one |
| **Step into** | Goes inside a function call, such as `calculate_total`, to follow it line by line |
| **Continue** | Runs until the next breakpoint |
| **Inspect variables** | Shows the current value of `price`, `total` and so on |
| **Conditional breakpoint** | Pauses only when a condition is true, such as a value above a limit |

**Python's built-in debugger.** Code editors show these as buttons, but Python also has a built-in debugger, `pdb`. Writing `breakpoint()` in the code starts it at that line:

| Command | Meaning |
| --- | --- |
| `n` (next) | Step over |
| `s` (step) | Step into |
| `c` (continue) | Run to the next breakpoint |
| `p total` | Print a variable |
| `l` (list) | Show the code around the current line |
| `q` (quit) | Stop debugging |

**`if __name__ == "__main__":`** marks the code that runs only when the file is run directly. That keeps `calculate_total` reusable: another file can import it without the test values running.

## How this shows up in financial statement audit work

Debugging is close to how I already review a spreadsheet: trace the calculation step by step until the number stops making sense. These snippets use small sample data built in the code.

**1. A classic bug: a discount applied on every line instead of once.** One extra indent puts the rebate inside the loop. Revenue is then understated with no error at all, and stepping through the loop with a debugger shows `total` dropping on every pass:

```python
def net_invoice_buggy(lines, rebate):
    total = 0
    for amount in lines:
        total += amount
        total -= rebate          # indented by mistake: runs 4 times
    return total

def net_invoice(lines, rebate):
    total = 0
    for amount in lines:
        total += amount
    total -= rebate              # runs once, after the loop
    return total

lines = [12_000, 4_500, 8_200, 3_300]
print(net_invoice_buggy(lines, 1_000), net_invoice(lines, 1_000))   # 24000 27000: a 3,000 understatement
```

**2. Assertions as built-in sanity checks.** An `assert` stops the program the moment a rule is broken, which points the debugger straight at the problem:

```python
def post_journal(lines):
    debits = sum(a for a in lines if a > 0)
    credits = -sum(a for a in lines if a < 0)
    assert round(debits - credits, 2) == 0, f"Entry out of balance by {debits - credits:,.2f}"
    return debits

print(post_journal([5_000, -3_000, -2_000]))   # 5000: balanced

try:
    post_journal([5_000, -3_000, -1_900])
except AssertionError as e:
    print(e)                                   # Entry out of balance by 100.00
```

**3. A conditional breakpoint for exceptions only.** When testing thousands of entries, pause only on the ones that matter:

```python
journal_entries = [("JE01", 4_200), ("JE02", 98_000), ("JE03", 650)]

for je_id, amount in journal_entries:
    if amount > 50_000:
        print(f"Would pause here to inspect {je_id}")   # replace this line with breakpoint() to debug
```

**4. Investigating a reconciliation that's out by a fraction of a cent.** Stepping through and inspecting the running total shows that floating-point numbers can't store some decimals exactly. That's why totals should be rounded, or calculated with `Decimal`, before comparing them:

```python
from decimal import Decimal

amounts = [0.10, 0.20]
print(sum(amounts))                                                 # 0.30000000000000004
print(sum(amounts) == 0.30)                                         # False
print(round(sum(amounts), 2) == 0.30)                               # True
print(sum(Decimal(str(a)) for a in amounts) == Decimal("0.30"))     # True: exact decimal arithmetic
```

## My reflection

This lecture changed how I'll approach wrong answers. Instead of guessing and adding prints, I'll pause the code and look, much as I'd ask for the supporting workings when a balance doesn't tie. The rebate example is the one that worries me most: a single indent changed the answer by 3,000 with no warning. That's exactly the kind of silent error a debugger, or an assertion, is there to catch.
