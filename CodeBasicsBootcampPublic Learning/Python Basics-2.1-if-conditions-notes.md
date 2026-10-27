# Python If Conditions: My Lecture 5 Notes

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **If Condition** lecture from the **CodeBasics Python course**.

## Where I started

Until now, my code ran every line from top to bottom. This lecture taught it to make decisions: do one thing if a condition is true and something else if it isn't. That is how an audit test works: if the claim breaks a rule, flag it; otherwise, move on. This was the first lecture where my code started to feel like an audit procedure.

## What I learnt

**`input()` always returns text.** Typing `10` gave `'10'`, a string, so I had to convert it with `int(n)` before doing any math.

**if / else.** The odd-or-even check uses the remainder operator from Lecture 2:

```python
if n % 2 == 0:
    print("Number is even")
else:
    print("Number is odd")
```

Indentation matters: the indented lines are the ones that belong to each branch.

**Comparison operators** all return `True` or `False`:

| Operator | Example | Result |
| --- | --- | --- |
| `==` (equal) | `3 == 4` | `False` |
| `>` (greater than) | `10 > 9` | `True` |
| `<` (less than) | `4 < 4` | `False` |
| `<=` (less than or equal) | `4 <= 4` | `True` |
| `not` (reverses a result) | `not 4 == 4` | `False` |

**`and` joins conditions.** `n > 10 and n % 2 == 0` is true only when both parts are true, so `n = 8` gave `"Nope"`.

**elif for several outcomes.** The dish-and-cuisine program checks each list in turn with `in`. The `else` catches anything unknown, such as `"asdf"`.

**The ternary operator** fits a simple if/else on one line:

```python
message = "Number is even" if n % 2 == 0 else "Number is odd"
```

## How this shows up in insurance audit work

Insurance audit is full of rules: authority limits, coverage terms, grace periods and red flags. Each one becomes an if condition.

**1. Claim authority limits.** Claims above an adjuster's limit need senior approval.

```python
claim_amount = 85000
adjuster_limit = 50000

if claim_amount > adjuster_limit:
    print("Escalate: claim exceeds adjuster authority")
else:
    print("Within adjuster authority")
```

**2. Early claim red flag with `and`.** A large claim soon after a policy starts is a classic fraud indicator.

```python
days_since_inception = 21
claim_amount = 120000

if days_since_inception < 30 and claim_amount > 100000:
    print("Red flag: large claim within 30 days of policy start")
```

**3. Coverage check with `elif`.** This works like the cuisine program, using covered and excluded perils instead of dishes.

```python
covered_perils = ["fire", "theft", "storm"]
excluded_perils = ["flood", "war", "wear and tear"]
peril = "flood"

if peril in covered_perils:
    print(f"{peril}: covered")
elif peril in excluded_perils:
    print(f"{peril}: excluded, so check why the claim was paid")
else:
    print(f"{peril}: not listed, so review the policy wording")
```

**4. Policy status with the ternary operator.** After the grace period, an unpaid policy lapses, and claims on it should be questioned.

```python
days_premium_overdue = 45
grace_period = 30
status = "Lapsed" if days_premium_overdue > grace_period else "Active"
print(status)   # Lapsed
```

## My reflection

The `input()` surprise connected straight back to Lecture 2. Data often looks like a number but arrives as text, so converting it comes before any test. I also liked how the `else` branch works as a safety net. In audit, the cases that match none of my rules are often the most interesting ones, so I want my code to report them instead of skipping them.

Next, I want to practise:

- [ ] Flag claims above an authority limit
- [ ] Combine two red-flag conditions with `and`
- [ ] Classify a list of perils as covered, excluded or unknown
