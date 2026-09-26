# Simple Linear Regression Notebook: Quick Breakdown

**Goal:** Predict GPA from SAT scores using linear regression

---

## Step-by-Step Walkthrough

### **Step 1: Import Libraries**

```python
import numpy as np           # Numerical computations
import pandas as pd          # Data manipulation
import matplotlib.pyplot as plt  # Plotting
import statsmodels.api as sm # Statistical modeling (regression)
```

**What it does:** Sets up tools for data analysis and regression.

---

### **Step 2: Load Data**

```python
data = pd.read_csv('1.01. Simple linear regression.csv')
data.describe()  # Show summary statistics
```

**What it does:** 
- Reads CSV file into DataFrame
- Shows mean, std, min, max of each column
- Helps understand the data before modeling

---

### **Step 3: Define Variables**

```python
y = data['GPA']      # Dependent variable (what we predict)
x1 = data['SAT']     # Independent variable (predictor)
```

**What it does:** Separate Y (outcome) from X (input).

---

### **Step 4: Explore with Scatter Plot**

```python
plt.scatter(x1, y)           # Plot points
plt.xlabel('SAT', fontsize=20)
plt.ylabel('GPA', fontsize=20)
plt.show()
```

**What it does:** Visualize relationship between SAT and GPA.
- If points trend upward → positive relationship ✓
- If points are scattered → weak relationship

---

### **Step 5: Fit the Regression Model**

```python
x = sm.add_constant(x1)        # Add column of 1s (for intercept)
results = sm.OLS(y, x).fit()   # Fit OLS regression
results.summary()              # Print statistics
```

**What it does:**
1. `add_constant()` → Adds intercept term (b₀)
2. `OLS(y, x).fit()` → Finds best-fit line minimizing errors
3. `summary()` → Shows:
   - Coefficients (b₀, b₁)
   - R-squared (model fit)
   - P-values (significance)

**Output reveals:**
- **Intercept (b₀):** 0.275
- **Slope (b₁):** 0.0017
- **Equation:** `GPA = 0.275 + 0.0017*SAT`

**Interpretation:**
- Base GPA: 0.275
- Each point on SAT → +0.0017 GPA increase
- 100 points SAT gain → +0.17 GPA increase

---

### **Step 6: Plot Regression Line**

```python
plt.scatter(x1, y)                          # Actual data
yhat = 0.0017*x1 + 0.275                   # Predicted values
plt.plot(x1, yhat, lw=4, c='orange')       # Plot line
plt.xlabel('SAT', fontsize=20)
plt.ylabel('GPA', fontsize=20)
plt.show()
```

**What it does:** Overlay regression line on scatter plot.
- Shows how well line fits data
- Visually confirms model quality

---

## The Complete Process

```
1. Load Data
   ↓
2. Separate Y and X
   ↓
3. Visualize (Scatter plot)
   ↓
4. Fit Model (OLS regression)
   ↓
5. Check Results (Summary)
   ↓
6. Plot Regression Line
   ↓
7. Make Predictions
```

---

## Key Outputs from results.summary()

```
Coefficient of SAT:      0.0017  (How much GPA changes per SAT point)
Intercept:               0.275   (Baseline GPA)
R-squared:               0.406   (Model explains 40.6% of GPA variation)
P-value (SAT):           0.001   (Highly significant - SAT matters!)
Prob (F-statistic):      7.20e-11 (Model is statistically significant)
```

---

## What the Code Doesn't Check (Important!)

⚠️ **Assumptions not verified in this notebook:**
- Linearity (assumed but should verify)
- Normality of errors
- Homoscedasticity (constant variance)
- Multicollinearity (only 1 predictor, so not an issue)
- Autocorrelation

**To do this, you'd add:**
```python
# Plot residuals
plt.scatter(yhat, results.resid)
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.show()
```

---

## Summary

| What | How | Result |
|---|---|---|
| **Predict** | Y from X | GPA from SAT |
| **Method** | OLS | Minimize squared errors |
| **Equation** | ŷ = b₀ + b₁x | GPA = 0.275 + 0.0017*SAT |
| **Strength** | R² | 0.406 (moderate fit) |
| **Significance** | P-value | 0.001 (very significant) |

---

## One-Liner

This notebook builds a regression model to predict college GPA from SAT scores, showing that SAT explains ~40% of GPA variation, with each SAT point increasing GPA by 0.0017.

---

## Next Steps

1. ✅ Check OLS assumptions (add residual plots)
2. ✅ Add more predictors (multiple regression)
3. ✅ Cross-validate on test data
4. ✅ Make predictions on new data

