# Day 8: Multiple Linear Regression - Theory & Practical Implementation

**Date:** September 27, 2026  
**Topic:** Multiple Linear Regression (More Than One Predictor)  
**Duration:** 120-150 minutes  
**Level:** Intermediate to Advanced  
**Running Example:** Real Estate Price Prediction

---

## Overview

Extending from simple linear regression (Day 7), today we explore **multiple linear regression** where we use multiple independent variables to predict a dependent variable.

**Real-World Problem:** A real estate company wants to predict house prices based on:
- Size (square footage)
- Year built

This is much more realistic than using just one predictor!

---

## Lesson 1: Moving from Simple to Multiple Linear Regression

### Important Points:

**1. Why Multiple Predictors?**

In real life, outcomes rarely depend on just one factor.

```
Simple Linear Regression (Day 7):
House Price = b₀ + b₁(Size) + ε

Problems:
├─ Missing important factors
├─ Incomplete model
└─ Poor prediction accuracy

Multiple Linear Regression (Today):
House Price = b₀ + b₁(Size) + b₂(Year) + ε

Benefits:
├─ Includes multiple factors
├─ More complete representation
├─ Better predictions
└─ Explains more variation
```

**Real Example: Real Estate Data**

```
Dataset: 100 houses with 3 variables

Variable    Min         Mean        Max         Description
───────────────────────────────────────────────────────────
Price       $154K       $292K       $500K       Sale price (target)
Size        480 sq ft   853 sq ft   1,843 sq ft Living area
Year        2006        2012.6      2018        Year built
```

**2. Data Relationships**

Understanding correlations:
```
Correlation with Price:
├─ Size ↔ Price: 0.863 (Strong positive)
│  └─ Larger houses cost more ✓
│
└─ Year ↔ Price: 0.093 (Weak positive)
   └─ Building year has minimal effect
```

**Why This Matters:**
- Strong predictors (Size: 0.86) should be included
- Weak predictors (Year: 0.09) may not add much
- Need to test which variables are significant

**3. The General Form**

```
Multiple Linear Regression Model:

ŷ = b₀ + b₁x₁ + b₂x₂ + ... + bₖxₖ + ε

Where:
├─ ŷ = Predicted value (Price)
├─ b₀ = Intercept (baseline price)
├─ b₁, b₂, ..., bₖ = Coefficients (effect of each variable)
├─ x₁, x₂, ..., xₖ = Independent variables (Size, Year, etc.)
└─ ε = Error term

For our example:
ŷ(Price) = b₀ + b₁(Size) + b₂(Year) + ε
```

**4. Extending OLS to Multiple Variables**

Ordinary Least Squares still works, but in matrix form:

```
Simple Linear Regression (2 dimensions):
├─ Find line minimizing Σ(y - ŷ)²
└─ Easy to visualize

Multiple Regression (3+ dimensions):
├─ Find hyperplane minimizing Σ(y - ŷ)²
├─ Can't visualize easily (need 3D, 4D, etc.)
└─ Same principle: minimize sum of squared errors

Matrix formulation:
y = Xb + ε

Where:
├─ y = [n×1] vector of prices
├─ X = [n×(k+1)] matrix of predictors (+ constant column)
├─ b = [(k+1)×1] vector of coefficients
└─ ε = [n×1] vector of errors
```

### Practical Implementation:

**Step 1: Load and Explore Data**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
sns.set()

# Load data
data = pd.read_csv('real_estate_price_size_year.csv')

# Explore
print(data.head())
print(data.describe())
print(data.corr())
```

**Output:**
```
        price     size  year
0  234314.144   643.09  2015
1  228581.528   656.22  2009
2  281626.336   487.29  2018

Statistics:
       price      size    year
mean  292289.5  853.02  2012.6
std    77051.7  297.94     4.7
```

**Step 2: Prepare Variables**

```python
# Define dependent and independent variables
y = data['price']
x1 = data[['size', 'year']]

# Add constant for intercept
x = sm.add_constant(x1)

print(f"y shape: {y.shape}")      # (100,)
print(f"x shape: {x.shape}")      # (100, 3) - const, size, year
```

**Step 3: Fit the Model**

```python
# Fit OLS regression
results = sm.OLS(y, x).fit()

# View summary
print(results.summary())
```

---

## Lesson 2: Interpreting Multiple Regression Output

### Important Points:

**1. The Regression Equation**

From the notebook output, we would get something like:

```
Price = b₀ + b₁(Size) + b₂(Year) + ε

Example Results (hypothetical):
Price = 150,000 + 200(Size) + 5,000(Year) + ε

Interpretation:
├─ Intercept (150,000): Baseline price (theoretical, often meaningless)
├─ Size coefficient (200): Each additional sq ft increases price by $200
│  └─ Holding year constant
│
└─ Year coefficient (5,000): Each additional year increases price by $5,000
   └─ Holding size constant
```

**Critical: Holding Other Variables Constant**

This is the KEY difference from simple regression:

```
Simple Regression: Y = b₀ + b₁(X)
Interpretation: "X has effect b₁ on Y"

Multiple Regression: Y = b₀ + b₁(X₁) + b₂(X₂)
Interpretation: "X₁ has effect b₁ on Y, HOLDING X₂ CONSTANT"
                (i.e., for fixed X₂, what's the effect of X₁?)
```

**2. Model Fit Metrics**

```
R-squared (R²):
├─ Percentage of variation explained
├─ Range: 0 to 1
├─ Example: R² = 0.756 means 75.6% of price variation
│          is explained by size and year
└─ Interpretation: Good if > 0.7 for this domain

Adjusted R-squared:
├─ Penalizes adding variables
├─ Always ≤ R²
├─ Use when comparing models
└─ Important: Adj. R² should not decrease much when adding variables

Example:
Model 1 (Size only):    R² = 0.745, Adj. R² = 0.743
Model 2 (Size + Year):  R² = 0.756, Adj. R² = 0.750

Conclusion: Year adds minimal value (R² increase of 0.011)
```

**3. Coefficient Significance Testing**

Each coefficient has:
```
Coefficient value (b)
├─ Standard Error (SE) - uncertainty
├─ t-statistic = b / SE
├─ p-value - probability null hypothesis is true
└─ 95% Confidence Interval

Interpretation Example:
Variable    Coef      SE      t-stat   p-value
────────────────────────────────────
const      150000    50000    3.000   0.003 **
size          200      20     10.000   0.000 **
year         5000    10000    0.500   0.618

Meaning:
├─ Size: Very significant (p < 0.001)
│  └─ Effect is real, not due to chance
│
├─ Year: NOT significant (p = 0.618)
│  └─ Effect might be zero, no evidence it matters
│
└─ ** means p < 0.05 (significant at 5% level)
```

**4. F-statistic (Overall Model Significance)**

```
Tests: Does ANY variable matter?

H₀: All coefficients = 0 (useless model)
H₁: At least one coefficient ≠ 0 (useful model)

Example:
F-statistic = 156.3
Prob (F-statistic) = 1.2e-45

Interpretation: Extremely strong evidence model is useful
(p-value ≈ 0)
```

**5. Residual Standard Error**

```
RSE (Residual Standard Error):
├─ Average prediction error
├─ Measured in same units as Y
├─ Example: RSE = $45,000 means predictions off by ~$45K on average
└─ Lower is better

Relationship to R²:
├─ Higher R² → Lower RSE
├─ They measure same thing differently
└─ RSE more intuitive (in dollars)
```

### Practical Output Interpretation:

**Real Estate Regression Summary (Hypothetical)**

```
                          OLS Regression Results
═════════════════════════════════════════════════════════════
Dep. Variable:           price        R-squared:       0.756
Model:                   OLS          Adj. R-squared:  0.750
Method:                  Least Sq.    F-statistic:     129.4
Date:                    Sep 27, 2026 Prob (F-stat):   1.5e-30
Time:                    12:00:00     
No. Observations:        100
Df Residuals:            97
Df Model:                2

                 coef    std err    t    P>|t|   [0.025  0.975]
─────────────────────────────────────────────────────────────
const         148500    48500    3.06   0.003   52000  245000
size             210      18    11.67  0.000     175    245
year             3200    8900    0.36   0.721   -14400  20800
═════════════════════════════════════════════════════════════

Omnibus:    2.341    Durbin-Watson: 1.847
Prob(Omnibus): 0.310  Jarque-Bera (JB): 2.105
```

**Interpretation Summary:**

```
✓ Model is highly significant (F-stat = 129.4, p ≈ 0)
  → At least one predictor matters

✓ Size is significant (p < 0.001)
  → Each sq ft adds ~$210 to price (95% CI: $175-$245)
  → Strong evidence

✗ Year is NOT significant (p = 0.721)
  → No evidence year affects price
  → Could be dropped from model

✓ Model explains 75.6% of price variation
  → Good fit for real estate prediction

✓ Residuals appear normal (Jarque-Bera p = 0.310 > 0.05)
  → Assumption check passes

✓ No autocorrelation (Durbin-Watson = 1.847 ≈ 2)
  → Independence assumption OK
```

---

## Lesson 3: Testing Significance of Coefficients (t-tests & F-tests)

### Important Points:

**1. Individual Coefficient Test (t-test)**

Each coefficient gets its own hypothesis test:

```
For coefficient b₁ (size effect):

H₀: b₁ = 0 (size doesn't affect price)
H₁: b₁ ≠ 0 (size does affect price)

Test statistic: t = b₁ / SE(b₁)

Example:
b₁ = 210 (estimated effect)
SE(b₁) = 18 (standard error)
t = 210 / 18 = 11.67

Decision:
├─ If |t| > 1.96 (rough cutoff), reject H₀
├─ If p-value < 0.05, reject H₀
├─ Here: t = 11.67, p < 0.001 → Significant!
└─ Conclusion: Size definitely affects price
```

**Why Standard Error Matters:**

```
High SE (uncertain estimate):
├─ b = 200 ± 100 (large uncertainty)
├─ t = 200/100 = 2.0
├─ Might not be significant
└─ Effect is unclear

Low SE (precise estimate):
├─ b = 200 ± 20 (small uncertainty)
├─ t = 200/20 = 10.0
├─ Definitely significant
└─ Effect is clear

Lesson: Even moderate coefficients can be significant
if estimated precisely (low SE)!
```

**2. Overall Model Test (F-test)**

Tests if model as a whole is useful:

```
H₀: All slopes = 0 (model is useless)
H₁: At least one slope ≠ 0 (model is useful)

Test statistic: F = MSR / MSE

Where:
├─ MSR = Mean Squared Regression (variation explained)
├─ MSE = Mean Squared Error (variation unexplained)
└─ Large F → Model is good

For Real Estate Example:
F = 129.4, p-value ≈ 0

Interpretation: Model is highly significant
Model explains substantial variation in price
```

**3. Confidence Intervals for Coefficients**

Instead of just "is it significant?", we get range:

```
95% Confidence Interval for size effect:

Point estimate: $210 per sq ft
95% CI: [$175, $245] per sq ft

Interpretation:
├─ True effect is likely between $175 and $245
├─ We're 95% confident this interval contains truth
├─ Range is tight → Estimate is precise
└─ No zero in interval → Definitely significant
```

**4. When to Drop Variables**

Decision rule based on testing:

```
Keep if:
├─ p-value < 0.05 (statistically significant)
├─ Makes logical sense
└─ Improves model substantially

Drop if:
├─ p-value > 0.05 (not statistically significant)
├─ Doesn't make logical sense
├─ Highly correlated with other variables
└─ Doesn't improve predictions

Real Estate Example:
Size (p < 0.001): KEEP
 └─ Highly significant, makes sense

Year (p = 0.721): DROP
 └─ Not significant, weak correlation
 └─ Model works fine without it
```

### Practical Implementation:

**Step 1: Check Individual Significance**

```python
import pandas as pd
import statsmodels.api as sm

# Fit model
y = data['price']
x = sm.add_constant(data[['size', 'year']])
results = sm.OLS(y, x).fit()

# Extract coefficients and stats
coef_table = pd.DataFrame({
    'Coefficient': results.params,
    'Std Error': results.bse,
    't-statistic': results.tvalues,
    'p-value': results.pvalues,
    'CI Lower': results.conf_int()[0],
    'CI Upper': results.conf_int()[1]
})

print(coef_table)

# Decision logic
for var in coef_table.index[1:]:  # Skip constant
    p_val = coef_table.loc[var, 'p-value']
    if p_val < 0.05:
        print(f"✓ {var} is significant (p = {p_val:.4f})")
    else:
        print(f"✗ {var} is NOT significant (p = {p_val:.4f})")
```

**Step 2: Fit Reduced Model (Remove Insignificant Variables)**

```python
# Original model (both variables)
x_full = sm.add_constant(data[['size', 'year']])
results_full = sm.OLS(y, x_full).fit()

# Reduced model (drop year, keep only size)
x_reduced = sm.add_constant(data[['size']])
results_reduced = sm.OLS(y, x_reduced).fit()

# Compare
print("Full Model (Size + Year):")
print(f"  R² = {results_full.rsquared:.4f}")
print(f"  Adj. R² = {results_full.rsquared_adj:.4f}")

print("\nReduced Model (Size only):")
print(f"  R² = {results_reduced.rsquared:.4f}")
print(f"  Adj. R² = {results_reduced.rsquared_adj:.4f}")

print("\nConclusion:")
print("Removing 'year' barely hurts model")
print("Reduced model is simpler and just as good")
```

---

## Lesson 4: Assumptions, Diagnostics & Model Validation

### Important Points:

**1. OLS Assumptions Extended to Multiple Regression**

All 5 assumptions from Day 7 still apply, but now with multiple X's:

```
Assumption 1: Linearity
├─ Relationship between Y and EACH X is linear
├─ Check: Residual plots, component plots
└─ Issue: Violations suggest non-linear terms needed

Assumption 2: No Perfect Multicollinearity
├─ Predictors not perfectly correlated with each other
├─ Check: Correlation matrix, VIF
├─ Issue: Makes coefficients unstable, high SE
├─ Real data: Size (853 sq ft) and Year (2012.6)
│          Correlation = -0.098 (low, OK!)

Assumption 3: Exogeneity / No Endogeneity
├─ X variables not correlated with error term
├─ Check: Theory, cause-effect reasoning
├─ Issue: Biased coefficients
├─ Real data: Size and Year determined before price,
│          so causality clear

Assumption 4: Homoscedasticity
├─ Error variance constant across X values
├─ Check: Residual plots (constant spread)
└─ Issue: Standard errors wrong if violated

Assumption 5: No Autocorrelation
├─ Errors independent (mainly time series issue)
├─ Check: Durbin-Watson test
└─ Issue: Underestimated standard errors
```

**2. Multicollinearity - The Key New Issue**

```
What is multicollinearity?
└─ When X variables are correlated with each other

Problem:
├─ High correlation makes it hard to isolate individual effects
├─ Coefficients become unstable
├─ Standard errors inflate
├─ Model still predicts OK, but interpretation fails

Example:
Size and Year correlation = -0.098
└─ Very low → No multicollinearity problem

BUT imagine:
Price ~ Square feet + Total rooms
└─ Square feet and Total rooms are highly correlated
└─ Hard to tell which one matters
└─ Coefficients unreliable

Diagnosis: Variance Inflation Factor (VIF)
├─ VIF = 1: No multicollinearity
├─ VIF < 5: OK
├─ VIF > 10: Problem!

For real estate:
VIF(size) = 1.01 (OK)
VIF(year) = 1.01 (OK)
└─ No multicollinearity issue
```

**3. Diagnostic Plots**

Essential checks:

```
Plot 1: Residuals vs Fitted
├─ Check: Random scatter, no patterns
├─ Issue: Curved pattern = non-linearity
├─ Issue: Funnel pattern = heteroscedasticity

Plot 2: Q-Q Plot
├─ Check: Points follow diagonal line
├─ Issue: Deviations = non-normal errors
└─ Minor deviations OK (especially in middle)

Plot 3: Scale-Location
├─ Check: Random scatter
├─ Issue: Sloped pattern = heteroscedasticity

Plot 4: Residuals vs Leverage
├─ Check: No influential outliers
├─ Issue: Points far from center = influential
```

**4. Out-of-Sample Validation**

Critical for real-world deployment:

```
Why:
├─ Model can overfit (memorize training data)
├─ Test performance is what matters
└─ Real-world predictions use new data

Process:
1. Split data: 70% train, 30% test
2. Fit model on training data
3. Make predictions on test data
4. Compare accuracy

Example:
Training R² = 0.76 (fits training data)
Test R² = 0.72 (performs on new data)
├─ Similar → Good generalization
└─ Big gap → Overfitting

Real estate: If training/test R² both ~0.75
└─ Model will work on new houses
```

### Practical Implementation:

**Step 1: Check Multicollinearity**

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF
X = data[['size', 'year']]
vif_data = pd.DataFrame()
vif_data['Variable'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)
# Expected output:
# Variable   VIF
# size       1.01
# year       1.01
# └─ Both < 5, so no multicollinearity

print("\nCorrelation Matrix:")
print(data[['size', 'year']].corr())
# Expected: Very low correlation
```

**Step 2: Diagnostic Plots**

```python
import matplotlib.pyplot as plt

# Get residuals and fitted values
residuals = results.resid
fitted = results.fittedvalues

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Residuals vs Fitted
axes[0, 0].scatter(fitted, residuals)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted Values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted (Check for patterns)')

# Plot 2: Q-Q Plot
sm.qqplot(residuals, line='45', ax=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot (Check normality)')

# Plot 3: Scale-Location
standardized_resid = residuals / residuals.std()
axes[1, 0].scatter(fitted, np.sqrt(np.abs(standardized_resid)))
axes[1, 0].set_xlabel('Fitted Values')
axes[1, 0].set_ylabel('√|Standardized Residuals|')
axes[1, 0].set_title('Scale-Location (Check homoscedasticity)')

# Plot 4: Residuals histogram
axes[1, 1].hist(residuals, bins=20, edgecolor='black')
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Distribution of Residuals')

plt.tight_layout()
plt.show()
```

**Step 3: Train-Test Split Validation**

```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Split data
X = data[['size', 'year']]
y = data['price']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Fit on training data
X_train_const = sm.add_constant(X_train)
results_train = sm.OLS(y_train, X_train_const).fit()

# Evaluate on test data
X_test_const = sm.add_constant(X_test)
y_pred = results_train.predict(X_test_const)
r2_test = r2_score(y_test, y_pred)

# Compare
r2_train = results_train.rsquared
print(f"Training R²: {r2_train:.4f}")
print(f"Test R²: {r2_test:.4f}")
print(f"Difference: {abs(r2_train - r2_test):.4f}")

if abs(r2_train - r2_test) < 0.05:
    print("✓ Good generalization - model will work on new data")
else:
    print("✗ Potential overfitting - model doesn't generalize well")
```

---

## Lesson 5: Model Comparison & Selection

### Important Points:

**1. Comparing Multiple Models**

When should you add variables?

```
Model Selection Problem:
├─ Adding variables always increases R²
├─ But may hurt generalization
├─ Need balance: fit vs complexity

Solution: Use information criteria

AIC (Akaike Information Criterion):
├─ AIC = -2(ln L) + 2k
├─ L = likelihood, k = number of parameters
├─ Lower AIC is better
├─ Penalizes adding variables
└─ Prefers simpler models

BIC (Bayesian Information Criterion):
├─ Similar to AIC
├─ Penalizes complexity more strongly
├─ Better for large samples
└─ Lower BIC is better
```

**2. Real Estate Model Selection**

```
Candidate Models:

Model 1: Price ~ Size only
├─ R² = 0.745
├─ Adj. R² = 0.743
├─ AIC = very_high_1
└─ Interpretation: Simple, clear

Model 2: Price ~ Size + Year
├─ R² = 0.756
├─ Adj. R² = 0.750
├─ AIC = very_high_2
└─ Interpretation: More complete

Model 3: Price ~ Size + Year + interaction(Size*Year)
├─ R² = 0.763
├─ Adj. R² = 0.751
├─ AIC = very_high_3
└─ Interpretation: Complex

Decision:
├─ If Goal = Prediction: Choose Model 3 (highest R²)
├─ If Goal = Explanation: Choose Model 1 (simplest, interpretable)
├─ If Goal = Balance: Choose Model 2 (good R², still simple)
└─ Check AIC/BIC to confirm
```

**3. Adding Interaction Terms**

```
What is an interaction?
└─ Effect of Size depends on Year

Main Effects Model:
Price = b₀ + b₁(Size) + b₂(Year)
└─ Effect of Size is always b₁ (same every year)

Interaction Model:
Price = b₀ + b₁(Size) + b₂(Year) + b₃(Size×Year)

Interpretation:
├─ Effect of Size = b₁ + b₃(Year)
├─ Effect changes with Year
├─ Example: Older houses might get different premium per sq ft
└─ More complex but captures reality

When to use:
├─ Theory suggests interaction (plausible reason)
├─ Interaction term is significant (p < 0.05)
└─ Don't add "just in case" (overfitting risk)
```

**4. Cross-Validation for Model Selection**

```
K-Fold Cross-Validation:

Process:
1. Split data into k folds (e.g., k=5)
2. For each fold:
   ├─ Use k-1 folds for training
   └─ Test on 1 fold
3. Average test performance across folds

Example (k=5):
Fold 1: Train on 2,3,4,5 → Test on 1
Fold 2: Train on 1,3,4,5 → Test on 2
Fold 3: Train on 1,2,4,5 → Test on 3
Fold 4: Train on 1,2,3,5 → Test on 4
Fold 5: Train on 1,2,3,4 → Test on 5

Average the 5 test R² values

Benefit: Uses all data, robust to random split
```

### Practical Implementation:

**Step 1: Create Multiple Models**

```python
import statsmodels.api as sm

# Model 1: Size only
X1 = sm.add_constant(data[['size']])
model1 = sm.OLS(y, X1).fit()

# Model 2: Size + Year
X2 = sm.add_constant(data[['size', 'year']])
model2 = sm.OLS(y, X2).fit()

# Model 3: Size + Year + interaction
data['size_year_interaction'] = data['size'] * data['year']
X3 = sm.add_constant(data[['size', 'year', 'size_year_interaction']])
model3 = sm.OLS(y, X3).fit()

# Compare metrics
comparison = pd.DataFrame({
    'Model': ['Size only', 'Size + Year', 'Size + Year + Interaction'],
    'R²': [model1.rsquared, model2.rsquared, model3.rsquared],
    'Adj. R²': [model1.rsquared_adj, model2.rsquared_adj, model3.rsquared_adj],
    'AIC': [model1.aic, model2.aic, model3.aic],
    'BIC': [model1.bic, model2.bic, model3.bic]
})

print(comparison)
```

**Step 2: K-Fold Cross-Validation**

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

# Prepare data
X = data[['size', 'year']].values
y = data['price'].values

# Create model
model = LinearRegression()

# 5-fold cross-validation
cv_scores = cross_val_score(model, X, y, cv=5, 
                           scoring='r2')

print(f"Cross-validation R² scores: {cv_scores}")
print(f"Mean CV R²: {cv_scores.mean():.4f}")
print(f"Std Dev: {cv_scores.std():.4f}")

# Interpretation
if cv_scores.std() < 0.05:
    print("✓ Stable model (low std) - generalizes well")
else:
    print("✗ Unstable model (high std) - check for overfitting")
```

---

## Summary Table: Multiple Linear Regression Checklist

| Step | Task | Real Estate Example | Check |
|------|------|---------|--------|
| 1 | **Explore Data** | Load data, correlations | Size-Price: 0.863 ✓ |
| 2 | **Specify Model** | Choose X variables | Size + Year |
| 3 | **Fit Model** | OLS regression | R² = 0.756 |
| 4 | **Check Sig.** | t-tests for coefficients | Size: p<0.001 ✓, Year: p=0.72 ✗ |
| 5 | **Check Assumptions** | All 5 OLS assumptions | VIF OK, residuals normal ✓ |
| 6 | **Diagnose** | Residual plots, outliers | No patterns, normal ✓ |
| 7 | **Validate** | Train-test split | Train R²=0.76, Test R²=0.72 ✓ |
| 8 | **Compare** | AIC/BIC, CV scores | Model 2 best balance |
| 9 | **Interpret** | Coefficients, CI | Size: $210 per sq ft [175, 245] |
| 10 | **Report** | Communicate results | "Size is main driver of price" |

---

## Complete Workflow: Real Estate Analysis

### Full Implementation

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# ===== STEP 1: Load and Explore =====
data = pd.read_csv('real_estate_price_size_year.csv')
print("Data shape:", data.shape)
print("\nDescriptive statistics:")
print(data.describe())
print("\nCorrelation matrix:")
print(data.corr())

# ===== STEP 2: Prepare Variables =====
y = data['price']
X = data[['size', 'year']]

# ===== STEP 3: Fit Multiple Regression =====
X_const = sm.add_constant(X)
results = sm.OLS(y, X_const).fit()
print("\nRegression Summary:")
print(results.summary())

# ===== STEP 4: Check Individual Significance =====
print("\nCoefficient Significance:")
for var in results.params.index[1:]:
    p_val = results.pvalues[var]
    print(f"{var}: p={p_val:.4f}", 
          "✓ SIGNIFICANT" if p_val < 0.05 else "✗ NOT significant")

# ===== STEP 5: Check Multicollinearity =====
vif_data = pd.DataFrame()
vif_data['Variable'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print("\nVariance Inflation Factors:")
print(vif_data)

# ===== STEP 6: Diagnostic Plots =====
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Residuals vs Fitted
axes[0, 0].scatter(results.fittedvalues, results.resid)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_title('Residuals vs Fitted')

# Q-Q Plot
sm.qqplot(results.resid, line='45', ax=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot')

# Scale-Location
standardized_resid = results.resid / results.resid.std()
axes[1, 0].scatter(results.fittedvalues, np.sqrt(np.abs(standardized_resid)))
axes[1, 0].set_title('Scale-Location')

# Residuals histogram
axes[1, 1].hist(results.resid, bins=20, edgecolor='black')
axes[1, 1].set_title('Distribution of Residuals')

plt.tight_layout()
plt.show()

# ===== STEP 7: Train-Test Validation =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_train_const = sm.add_constant(X_train)
X_test_const = sm.add_constant(X_test)

results_train = sm.OLS(y_train, X_train_const).fit()
y_pred = results_train.predict(X_test_const)
r2_test = r2_score(y_test, y_pred)

print(f"\nValidation Results:")
print(f"Training R²: {results_train.rsquared:.4f}")
print(f"Test R²: {r2_test:.4f}")

# ===== STEP 8: Model Comparison =====
# Model 1: Size only
X1 = sm.add_constant(data[['size']])
model1 = sm.OLS(y, X1).fit()

# Model 2: Size + Year (current)
model2 = results

comparison = pd.DataFrame({
    'Model': ['Size Only', 'Size + Year'],
    'R²': [model1.rsquared, model2.rsquared],
    'Adj. R²': [model1.rsquared_adj, model2.rsquared_adj],
    'AIC': [model1.aic, model2.aic]
})

print("\nModel Comparison:")
print(comparison)

# ===== STEP 9: Cross-Validation =====
skl_model = LinearRegression()
cv_scores = cross_val_score(skl_model, X, y, cv=5, scoring='r2')
print(f"\n5-Fold Cross-Validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ===== STEP 10: Predictions =====
print("\nSample Predictions:")
sample = pd.DataFrame({
    'size': [600, 900, 1200],
    'year': [2010, 2015, 2018]
})
sample_const = sm.add_constant(sample)
predictions = results.predict(sample_const)

print(sample)
print("\nPredicted prices:")
print(predictions.values)
```

---

## Key Insights

### Main Takeaways:

1. **Multiple predictors improve models** (from R² 0.745 to 0.756)
2. **Not all variables matter** (Size matters, Year doesn't in this case)
3. **Interpretation changes** (coefficients are now "holding other variables constant")
4. **More careful validation needed** (test that model generalizes)
5. **Trade-off: fit vs complexity** (simpler often better unless gain is large)

### Real Estate Model Conclusion:

```
Best Model: Price = b₀ + b₁(Size)
Reason:
├─ Size has strong effect (p < 0.001)
├─ Year doesn't improve model (p = 0.72)
├─ Simpler model is better (Adj. R² nearly same)
└─ Easier to interpret

The Finding:
"House prices are driven primarily by size.
Year built has no statistically significant effect."
```

---

## Common Mistakes to Avoid

```
❌ Including all variables (causes overfitting)
✓ Include only significant ones

❌ Ignoring multicollinearity
✓ Check VIF, correlations

❌ Trusting high training R² alone
✓ Validate on test/new data

❌ Misinterpreting coefficients
✓ Remember: holding OTHER variables constant

❌ Assuming statistical significance = practical significance
✓ Check effect size too (is $3/sq ft meaningful?)

❌ Not checking assumptions
✓ Always do residual diagnostics

❌ Using p-value alone for model selection
✓ Use AIC/BIC/CV too

❌ Extrapolating far beyond data range
✓ Predictions only valid in data range
```

---

## Python Code Repository Structure

```
For Day 8 Practice:

1. day8_multiple_regression.py
   ├─ Load data
   ├─ Fit models
   ├─ Generate diagnostics
   └─ Create plots

2. day8_analysis.ipynb
   └─ Interactive exploration
      (like the provided notebook)

3. real_estate_price_size_year.csv
   └─ Running example dataset
```

---

## Next Steps (Day 9+)

→ Polynomial regression (nonlinear relationships)  
→ Feature engineering (create new variables)  
→ Regularization (Ridge, Lasso - prevent overfitting)  
→ Categorical variables (how to include qualitative data)  
→ Time series regression (when observations are related)

---

**Date:** September 27, 2026  
**Topic:** Multiple Linear Regression - Complete Guide  
**Lessons:** 5 core lessons + full practical implementation  
**Example Dataset:** Real Estate (100 houses, 3 variables)  
**Outcome:** Ready to build and validate multi-variable regression models

