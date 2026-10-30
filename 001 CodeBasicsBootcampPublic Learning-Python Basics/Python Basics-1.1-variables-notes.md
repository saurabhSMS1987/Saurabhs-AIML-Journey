# Python Variables: My Lecture 1 Notes

*Oct 25, 2026 · Saurabh S*

## Source
 
These notes are based on the Variables lecture from the CodeBasics Python course.

## Where I started

Lecture 1 was about variables: the labelled boxes Python uses to hold data. The course compared a variable to a soda can, a container that holds something, and that picture stuck with me. Once I could name a value, I could check its type, combine it with others and test it against a rule. That last part felt very familiar from audit work.

## What I learnt

A variable is created with `=` and can be overwritten at any time. When `can = "soda"` became `can = "beans"`, the old value was simply replaced.

Python has four basic types, and `type()` tells me which one I am holding:

| Type | What it holds | Example from the lecture |
| --- | --- | --- |
| `str` | Text | `can = "soda"` |
| `int` | Whole numbers | `pizza = 100` |
| `float` | Numbers with decimals | `samosa = 20.5` |
| `bool` | True or False | `total > 200` gives `True` |

Adding an `int` to a `float` gave a `float` (100 + 20.5 + 100 = 220.5). Comparing a number to a threshold produced a `bool`, which is the seed of every exception test.

Everything in Python is an object. `bar = foo` made both names point to the same object, so `id()` returned the same number. Reassigning `bar` pointed it at a new object and left `foo` untouched.

Naming rules, which Python enforces with a `SyntaxError`:

1. No reserved keywords such as `True` or `def`.
2. No special characters such as `$` or `^`.
3. Start with a letter or `_`, never a digit (`4you` fails).
4. Use only letters, digits and `_` after that.

## How this shows up in audit work

The same four types already sit in every ledger I review. Seeing them as variables makes each audit test easier to write and explain.

**1. Threshold test (the `bool` I learnt).** Flagging items above a materiality limit is the lecture's `total > 200` with a new name.

```python
invoice_amount = 75000.00
approval_limit = 50000
needs_review = invoice_amount > approval_limit
print(needs_review)   # True
```

**2. Checking data types before testing.** Amounts exported as text break calculations, so I confirm the type first.

```python
amount = "12500.75"           # came in as text from the export
print(type(amount))           # <class 'str'>
amount = float(amount)
print(type(amount))           # <class 'float'>
```

**3. Reconciling totals.** Mixing `int` and `float` works like pizza + samosa: the result is a `float`.

```python
ledger_total = 125000
subledger_total = 124998.50
difference = ledger_total - subledger_total
reconciled = difference == 0
print(difference, reconciled)   # 1.5 False
```

**4. Clear names make working papers readable.** The naming rules matter when a reviewer reads my script later.

```python
vendor_name = "ABC Supplies"   # valid and clear
_tax_rate = 0.18               # underscore start is allowed
# 2023_sales = 500             # SyntaxError: starts with a digit
# net$amount = 900             # SyntaxError: special character
```

## My reflection

This lecture made Python feel less like a new language and more like a new way to write audit procedures I already do by hand. A small thing I noticed: the notebook spells it `above_thresold`. Python accepted it without complaint, which reminded me that the code only checks syntax, not judgment. That part is still my job.


