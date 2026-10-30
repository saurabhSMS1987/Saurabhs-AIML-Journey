# NumPy Matrix Operations: My Lecture 16 Notes

*Oct 29, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **NumPy Matrix Operations** lecture from the **CodeBasics Python course**.

## Where I started

The lecture used a sales table, with products as rows and regions as columns, and did the full revenue analysis on whole tables at once: growth, revenue, discounts and net revenue, each in a single line. Then it introduced the dot product, which combines rows of data with a set of weights. That idea maps directly onto risk scoring in audit.

## What I learnt

**Element-wise arithmetic.** When two tables have the same shape, `+`, `-`, `*` and `/` work cell by cell:

```python
q1 + q2                  # combined sales for each product and region
q2 - q1                  # unit growth
(q2 - q1) * 100 / q1     # % growth, e.g. Product B in region 2: 6.67%
q1_revenue = q1 * prices # units × price, cell by cell
```

**Working with a single number.** `q1_revenue * 0.02` applies a 2% discount to every cell, and `q1_revenue - q1_discounts` gives net revenue. `np.sum(q1_discounts)` totalled the discounts at 564.2.

Note that `*` here is **element-wise**, not matrix multiplication from maths class. Each cell is multiplied only by the matching cell.

**Dot product.** `np.dot` multiplies each row by a set of weights and adds the results. The house-price example:

```python
features = np.array([[2000, 3],      # house 1: square feet, bedrooms
                     [1800, 2]])     # house 2
weights = np.array([150, 50000])     # $ per sq ft, $ per bedroom

np.dot(features, weights)            # [450000, 370000]
# house 1: 2000×150 + 3×50000 = 450,000
```

**Cross product.** `np.cross([1, 2, 3], [4, 5, 6])` gives `[-3, 6, -3]`. It's mostly used in geometry and physics, so I don't expect to need it often in audit.

| Operation | What it does | Typical use |
| --- | --- | --- |
| `a * b` | Multiplies matching cells | Units × price |
| `a * 0.02` | Applies one number to every cell | A discount or rate |
| `np.sum(a)` | Totals everything | Total discounts |
| `np.dot(a, w)` | Weighted sum of each row | Pricing or scoring models |

## How this shows up in healthcare audit work

Healthcare billing is full of tables: procedures × providers, volumes × contracted rates. These snippets recalculate and score them the same way.

**1. Expected vs actual billing.** Procedure volumes × contracted rates gives what *should* have been billed.

```python
import numpy as np

# rows: City Hospital, Lakeside Clinic | columns: MRI, X-ray, ECG
volumes = np.array([[120, 300, 450],
                    [ 80, 260, 390]])
rates   = np.array([[900,  60,  45],
                    [850,  55,  40]])
actual_billed = np.array([[108000, 18000, 20250],
                          [ 76500, 14300, 15600]])

expected = volumes * rates
print(actual_billed - expected)   # [[   0    0    0]
                                  #  [8500    0    0]]: Lakeside overbilled MRIs by $8,500
```

**2. Growth in claim volumes by provider and department.**

```python
q1_claims = np.array([[200, 150], [180, 90]])   # rows: providers | columns: cardiology, orthopaedics
q2_claims = np.array([[210, 156], [185, 140]])

growth_pct = (q2_claims - q1_claims) * 100 / q1_claims
print(np.round(growth_pct, 1))   # [[ 5.   4. ]
                                 #  [ 2.8 55.6]]: provider 2 orthopaedics needs analytical review
```

**3. Risk-scoring claims with a dot product.** Each claim gets 1 or 0 for each red flag, and the weights reflect how serious each flag is.

```python
# columns: out-of-network, weekend admission, high-cost drug, duplicate patient ID
red_flags = np.array([[1, 0, 1, 0],    # claim 1
                      [0, 0, 0, 0],    # claim 2
                      [1, 1, 1, 1]])   # claim 3
weights = np.array([20, 10, 30, 40])

risk_scores = np.dot(red_flags, weights)
print(risk_scores)   # [ 50   0 100]: review claim 3 first
```

**4. Contractual discounts and total variance.** Payers agree a discount off gross charges, so I recalculate the expected payment and total the gap.

```python
gross_charges = np.array([[10000, 4500], [8200, 12000]])   # rows: payer A, payer B
paid = np.array([[8500, 3825], [7380, 10800]])

expected_paid = gross_charges * (1 - 0.15)   # 15% contractual discount
variance = paid - expected_paid
print(variance)            # [[  0.   0.] [410. 600.]]: second payer paid at 10%, not 15%
print(np.sum(variance))    # 1010.0 overpaid in total
```

## My reflection

The dot product was the surprise of this lecture. Something I thought of as maths homework turns out to be a simple risk-scoring tool: flag each claim, weight the flags and rank the results. That is how audit teams decide where to look first. The element-wise examples also showed me how quickly re-performance becomes possible. Recalculating every provider's billing against its contracted rates takes one line, and the differences show up straight away.

Next, I want to practise:

- [ ] Recalculate expected billing from volumes and contracted rates, then compare to actual
- [ ] Build a red-flag matrix for a sample of claims and rank them with `np.dot`
- [ ] Check contractual discounts on a set of payments and total the variance
