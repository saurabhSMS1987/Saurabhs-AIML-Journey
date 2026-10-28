# Python Tuples and Dictionaries: My Lecture 8 Notes

*Oct 26, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Tuples and Dictionaries** lecture from the **CodeBasics Python course**.

## Where I started

So far, lists have held everything I worked with. This lecture showed where they fall short. Finding Joey's phone number in a list meant looping through every contact until I reached him, which is slow with 10,000 records. A dictionary finds him instantly by name. It felt like the difference between scrolling through a claims register and typing a claim number into the system.

## What I learnt

### Tuples

A tuple groups related values in round brackets, such as a point: `point = (5, 6)`.

- Read items by position, like a list: `point[0]` gives 5.
- Tuples are **immutable**. `point[1] = 7` raised a `TypeError`. Their fixed size also makes them more memory-efficient than lists.
- They are handy for **returning several values from a function**:

```python
def find_pe_and_pb(price, eps, book_value):
    return price / eps, price / book_value

pe_ratio, pb_ratio = find_pe_and_pb(100, 2, 4)   # 50.0, 25.0
```

### Dictionaries

A dictionary stores **key: value** pairs: `d = {'rachel': 8887771111, 'joey': 3332229999}`.

| Task | Code | Note |
| --- | --- | --- |
| Look up | `d['joey']` | Instant, whatever the size of the dictionary (O(1)) |
| Missing key | `d['satya']` | Raises a `KeyError` |
| Safe lookup | `d.get('satya')` | Returns `None` instead of an error |
| Add or update | `d['satya'] = 2228764555` | The same syntax does both |
| Delete | `del d['satya']` | |
| Check | `'rachel' in d` | `True` or `False` |
| Loop | `for name, number in d.items()` | Key and value together |
| Keys or values only | `d.keys()`, `d.values()` | |

**Nested dictionaries** hold a dictionary as a value. `appl_revenues["India"]["iPad"]` gave 4, and a loop inside a loop printed every country and product.

## How this shows up in insurance audit work

Policies and claims have IDs, and IDs are natural dictionary keys. Here is how these tools fit insurance audit.

**1. Several ratios from one function, as a tuple.**

```python
def underwriting_ratios(claims, expenses, premiums):
    loss_ratio = claims / premiums * 100
    expense_ratio = expenses / premiums * 100
    return loss_ratio, expense_ratio

loss, expense = underwriting_ratios(620000, 330000, 1000000)
print(f"Combined ratio: {loss + expense}%")   # 95.0%: below 100 means an underwriting profit
```

**2. Claims against unknown policies.** `.get()` catches a claim whose policy isn't in the policy master, a classic fictitious-claim red flag.

```python
sum_insured = {"P101": 50000, "P102": 250000, "P103": 100000}

for policy in ["P101", "P999"]:
    if sum_insured.get(policy) is None:
        print(f"{policy}: no such policy. Investigate the claim")
```

**3. Comparing claim files with policy limits.** A nested dictionary works like a claim file.

```python
claims = {
    "CL-01": {"policy": "P101", "amount": 42000},
    "CL-02": {"policy": "P102", "amount": 260000},
}

for claim_id, info in claims.items():
    limit = sum_insured[info["policy"]]
    if info["amount"] > limit:
        print(f"{claim_id}: {info['amount']} exceeds the sum insured of {limit}")
```

**4. Spotting policies with frequent claims.** A dictionary is a quick counter.

```python
claim_policies = ["P101", "P102", "P101", "P103", "P101"]
counts = {}
for policy in claim_policies:
    counts[policy] = counts.get(policy, 0) + 1

for policy, n in counts.items():
    if n >= 3:
        print(f"{policy}: {n} claims, so review for claim frequency")
```

## My reflection

Dictionaries are the first tool that feels like a real database lookup, and I can already see them replacing many of my VLOOKUPs. The `KeyError` vs `.get()` difference also matters for audit. A missing key isn't just a coding problem: it can be the finding itself, like a claim with no matching policy. So I'd rather catch it and report it than let the script crash.

Next, I want to practise:

- [ ] Build a policy-to-sum-insured dictionary and check claims against it
- [ ] Count claims per policy and flag high-frequency policies
- [ ] Write a function that returns loss, expense and combined ratios as a tuple
