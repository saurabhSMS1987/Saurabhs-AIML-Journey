# Simple Linear Regression: My Regression: Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Simple Linear Regression** lecture notebook and the **Simple Linear Regression Exercise** solution from my data science course. The code uses `statsmodels`, following the course notebooks.

## Where I started

So far, I've used Python to describe data: totals, averages and filters. This lecture was the first step into *modelling*, which means using one variable to predict another. The question was simple: do students with higher SAT scores tend to get higher college GPAs, and by how much? The answer came as a straight line through a scatter plot.

## The data in brief

- **Lecture:** students' **SAT scores** (the independent variable, *x*) and their college **GPA** (the dependent variable, *y*). The fitted line in the notebook is:

  **GPA ≈ 0.275 + 0.0017 × SAT**

  So each extra **100 SAT points** goes with about **0.17 more GPA**.

- **Exercise:** a real estate dataset with house **price** (*y*) and **size** (*x*). The solution's line is:

  **price ≈ 101,900 + 223.18 × size**

  So each extra unit of size adds about **223** to the price, on top of a starting value of about 101,900.

The notebooks were shared without their outputs, so these figures come from the regression lines written in the code.

## What I learnt

**The regression equation:**

```text
y = b0 + b1 × x
        b0 = intercept (the constant): the predicted y when x is 0
        b1 = slope (the coefficient): how much y changes when x rises by 1
```

**The workflow, which was the same in the lecture and the exercise:**

```python
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

y = data["GPA"]                    # dependent variable: what we want to explain
x1 = data["SAT"]                   # independent variable: what we explain it with

plt.scatter(x1, y)                 # 1. look at the relationship first
x = sm.add_constant(x1)            # 2. add a column of 1s so the model can estimate the intercept
results = sm.OLS(y, x).fit()       # 3. fit with ordinary least squares
results.summary()                  # 4. read the results table
```

**OLS (ordinary least squares)** picks the line that makes the squared vertical distances between the points and the line as small as possible.

**`add_constant` matters:** without it, the line is forced through zero, so a student with an SAT score of 0 would have to have a GPA of 0. The intercept would be missing.

**Reading `results.summary()`:** the parts I'll use most are below.

| Item | What it tells me |
| --- | --- |
| `coef` for `const` | The intercept, *b0* |
| `coef` for the *x* variable | The slope, *b1* |
| `P>\|t\|` | Whether the coefficient is statistically significant (below 0.05 is the usual cut-off) |
| `R-squared` | The share of the variation in *y* that the model explains, from 0 to 1 |
| `std err` | How precise each coefficient estimate is |

**A small habit to improve:** both notebooks type the coefficients into the plotting line by hand, as `yhat = 0.0017*x1 + 0.275`. That rounds them, and the line breaks if the data changes. Using `results.params` keeps it exact:

```python
b0, b1 = results.params            # intercept, slope straight from the model
yhat = b0 + b1 * x1
```

**Correlation isn't causation.** The exercise notes that house prices have an almost certain *causal* link to size. SAT and GPA are better described as related, because both reflect other things, like how hard a student works.

## How this shows up in financial statement audit work

Regression is a recognised technique for **substantive analytical procedures**. You build an *expectation* of what a balance should be from a related driver, then investigate significant differences. Payroll against headcount is a classic case. The snippets use 24 months of sample data.

**1. Build the model on a period you trust.** Fitting on the prior year, which has already been audited, keeps any current-year misstatement out of the expectation itself:

```python
import pandas as pd
import statsmodels.api as sm

prior = pd.DataFrame({
    "headcount": [118, 120, 121, 123, 122, 125, 127, 128, 130, 129, 131, 133],
    "payroll":   [611800, 617800, 625900, 633500, 632600, 644300,
                  656200, 657600, 670300, 666900, 673900, 685500],
})

model = sm.OLS(prior["payroll"], sm.add_constant(prior["headcount"])).fit()
print(model.params.round(0).to_dict())   # {'const': 24606.0, 'headcount': 4964.0}: about 4,964 per employee per month
print(round(model.rsquared, 3))          # 0.995: headcount explains almost all of payroll
print(model.pvalues["headcount"] < 0.05) # True: the relationship is significant
```

A high R-squared and a significant slope mean the expectation is **precise enough to rely on**. With a weak model, the procedure provides little audit evidence.

**2. Set the expectation and investigate differences.**

```python
current = pd.DataFrame({
    "month":     pd.period_range("2026-01", periods=12, freq="M").astype(str),
    "headcount": [134, 135, 137, 136, 138, 140, 141, 143, 142, 144, 145, 147],
    "payroll":   [689100, 696400, 703300, 702100, 709600, 721000,
                  722700, 780800, 731500, 738800, 745600, 754700],
})

b0, b1 = model.params
current["expected"] = (b0 + b1 * current["headcount"]).round(0)
current["difference"] = current["payroll"] - current["expected"]

threshold = 15_000   # the amount of difference the audit team accepts without further work
print(current[current["difference"].abs() > threshold][["month", "payroll", "expected", "difference"]])
# 2026-08  780800  734485.0  46315.0: payroll about 46k above expectation, so ask why
```

August stands out. It could be a bonus run, a duplicate payment or a ghost employee, so it gets followed up with corroborating evidence.

**3. Check the expectation over the whole year.**

```python
print(current["payroll"].sum() - current["expected"].sum())   # 50568.0: most of it is August
```

## My reflection

This lecture connected statistics to audit work faster than I expected. I've done analytical procedures for years, but usually with a simple "last year plus inflation" expectation. A regression builds the expectation from an actual driver like headcount, and `R-squared` and the p-value show how far it can be trusted. That's exactly what's needed to document a substantive analytical procedure properly.

Two habits I'm taking forward: plot the data before fitting anything, because the scatter plot shows whether a straight line even makes sense; and fit on a period I trust. A model trained on data that already contains the error will simply learn the error.
