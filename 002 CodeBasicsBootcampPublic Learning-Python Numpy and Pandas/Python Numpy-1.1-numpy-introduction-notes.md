# NumPy Introduction and Benefits: My Lecture 14 Notes

*Oct 29, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **NumPy Introduction & Benefits** lecture from the **CodeBasics Python course**.

## Where I started

I met NumPy briefly in the Modules lecture. This lecture explained *why* it matters by putting a NumPy array side by side with a Python list. Both hold a sequence of numbers, but the array uses less memory, runs much faster and makes the maths simpler. For someone who works with large claims and premium datasets, those three benefits are the whole reason to learn it.

## What I learnt

**Creating arrays.** `np.array([1, 2, 3])` turns a list into an array, and `np.arange(100)` creates the numbers 0 to 99 directly, like `range()`.

**Benefit 1: less memory.** For 100 numbers:

| Structure | Memory |
| --- | --- |
| Python list | About 2,400 bytes (24 bytes per number, from `sys.getsizeof`) |
| NumPy array | 400 bytes (from `.nbytes`) |

A list stores each number as a separate Python object. An array stores plain numbers packed tightly together. The exact figures depend on the computer and Python version: on my test machine, the array used 800 bytes, because each number took 8 bytes instead of 4. The array is still several times smaller.

**Benefit 2: speed.** Adding two collections of 1 million numbers:

| Method | Time in the lecture |
| --- | --- |
| Python list (`[x + y for x, y in zip(l1, l2)]`) | About 0.052 seconds |
| NumPy array (`n1 + n2`) | About 0.002 seconds, roughly 25 times faster |

The list version is a *list comprehension*, a one-line loop that builds a new list. NumPy skips the Python loop entirely and works on the whole array at once.

**Benefit 3: convenience.** The same operator means different things:

```python
l1 + l2     # lists:  [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]  (joined end to end)
n1 + n2     # arrays: [0, 2, 4, 6, 8]                 (added item by item)
n1 * n2     # arrays: [0, 1, 4, 9, 16]                (multiplied item by item)
```

With arrays, the maths reads exactly like the formula, with no loop needed.

## How this shows up in insurance audit work

Insurance populations run into hundreds of thousands of policies and claims. NumPy turns whole-population recalculations into single lines of code.

**1. The `+` trap when adding two months of claims.** This is a silent error that would be easy to miss in a review.

```python
import numpy as np

jan = [12000, 4500, 30000]
feb = [8000, 6500, 15000]
print(jan + feb)                       # [12000, 4500, 30000, 8000, 6500, 15000]: joined, not added!
print(np.array(jan) + np.array(feb))   # [20000 11000 45000]: correct totals by line
```

**2. Recalculating net claims payable.** Claim minus deductible, for every claim at once:

```python
claims = np.array([12000, 4500, 30000, 95000])
deductibles = np.array([1000, 500, 2500, 5000])
net_payable = claims - deductibles
print(net_payable)                     # [11000  4000 27500 90000]
```

**3. Re-performing a premium rate change.** A 5% rate increase applied to every policy can be checked against the system's figures. `np.isclose` avoids false mismatches caused by tiny float rounding errors:

```python
old_premiums = np.array([10000, 25000, 18000])
system_new = np.array([10500, 26250, 18950])

expected_new = old_premiums * 1.05
print(np.isclose(expected_new, system_new))   # [ True  True False]: third policy is wrong
```

**4. Full-population testing instead of sampling.** One million claims are totalled in a fraction of a second:

```python
all_claims = np.full(1_000_000, 2500)  # 1 million claims of 2,500 each
print(all_claims.sum())                # 2500000000
```

## My reflection

The `l1 + l2` example will stay with me. Python gave a perfectly reasonable-looking answer that was completely wrong for my purpose, with no error at all. In audit terms, that's the most dangerous kind of mistake, so I'll convert amount lists to arrays before doing any maths. The speed test also made full-population testing feel realistic. If recalculating every claim takes a fraction of a second, there's often no reason to sample.

Next, I want to practise:

- [ ] Recalculate net payable (claim minus deductible) for a full claims extract
- [ ] Re-perform a premium rate change and flag every policy that doesn't match
- [ ] Time a list loop against NumPy on a large dataset myself
