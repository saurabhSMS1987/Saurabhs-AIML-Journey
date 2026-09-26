# Regression Analysis: Concept Guide

**Author:** Based on 365DataScience Course Notes  
**Level:** Beginner  

---

## What is Linear Regression?

**Simple Definition:**
```
Linear Regression = Find a line that best predicts Y from X
```

**Why Use It?**
- Make predictions from data
- Understand relationships between variables
- Determine what affects an outcome

---

## The Regression Equation

### Population Model (Greek letters):
```
Y = β₀ + β₁X + ε

Where:
  Y  = Dependent variable (what we predict)
  β₀ = Intercept (constant)
  β₁ = Slope (how much Y changes with X)
  X  = Independent variable (predictor)
  ε  = Error term
```

### Sample Equation (lowercase):
```
ŷ = b₀ + b₁*x

Where:
  ŷ = Predicted value
  b₀ = Estimated intercept
  b₁ = Estimated slope
  x  = Sample data
```

---

## Visual: The Regression Line

```
        y (Dependent Variable)
        ▲
        │         ●
        │    ●  /  ε (Error)
        │   /● /
        │  / ●/
        │ /  ●
        │/●  /
    b₀ ●────────────► x (Independent Variable)
        
        b₁ = Slope (steepness)
        b₀ = Y-intercept (where line crosses y-axis)
```

**Key Concept:**
- Red dots = Observed data
- Blue line = Regression line
- Distance = Error (what we minimize)

---

## Correlation vs Regression

```
╔════════════════════════╦════════════════════════╗
║     CORRELATION        ║      REGRESSION        ║
╠════════════════════════╬════════════════════════╣
║ Relationship between   ║ Cause and effect       ║
║ 2 variables            ║ between 2+ variables   ║
║                        ║                        ║
║ Symmetric              ║ Directional            ║
║ ρ(x,y) = ρ(y,x)       ║ Y depends on X         ║
║                        ║                        ║
║ Result: Single number  ║ Result: Equation/Line  ║
║ Example: -1 to +1      ║ Example: ŷ = 2 + 3x   ║
╚════════════════════════╩════════════════════════╝
```

---

## The 3-Step Process

```
Step 1              Step 2              Step 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Get Sample Data  →  Design Model  →  Make Predictions
                     (Find line)      (On population)
                     
Example:
Students'          Equation:          Predict GPA
test scores    ŷ = 2.5 + 0.8*x      for new students
```

---

## Key Metrics Explained

### 1. **R-squared (R²)** - Goodness of Fit
```
Range: 0 to 1

R² = 0.40  →  Model explains 40% of variation
R² = 0.80  →  Model explains 80% of variation
R² = 0.95  →  Excellent model
```

### 2. **Adjusted R²** - Accounts for Number of Variables
```
Range: Could be negative (interpreted as 0)

Use this when:
- Multiple independent variables
- Comparing models with different numbers of predictors
```

### 3. **P-value** - Statistical Significance
```
If P-value < 0.05  →  Variable is SIGNIFICANT ✓
If P-value > 0.05  →  Variable is NOT significant ✗

Example:
- P-value = 0.001  →  99.9% confident it matters
- P-value = 0.87   →  87% chance it's just noise
```

### 4. **Coefficients (b₀, b₁)** - Model Parameters
```
ŷ = 2.5 + 0.8*x

b₀ = 2.5   (Baseline prediction when x=0)
b₁ = 0.8   (For every unit increase in x, y increases 0.8)
```

---

## OLS Assumptions (Must Check!)

**OLS = Ordinary Least Squares (most common method)**

For reliable results, 5 assumptions must hold:

```
┌─────────────────────────────────────────────────┐
│ 1. LINEARITY                                    │
│    The relationship must be linear              │
│    ✓ Check: Scatter plot shows linear pattern   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 2. NO ENDOGENEITY                               │
│    X should not be correlated with error term   │
│    ✓ Check: Residuals plot shows no pattern     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 3. NORMALITY & HOMOSCEDASTICITY                 │
│    Errors should be normally distributed        │
│    with constant variance                       │
│    ✓ Check: Q-Q plot is linear                  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 4. NO AUTOCORRELATION                           │
│    Errors should be independent                 │
│    ✓ Check: Durbin-Watson ≈ 2                   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 5. NO MULTICOLLINEARITY                         │
│    Predictors should not be highly correlated   │
│    with each other                              │
│    ✓ Check: Correlation matrix < 0.8            │
└─────────────────────────────────────────────────┘
```

---

## Alternative Regression Methods

When OLS assumptions don't hold:

```
Method              When to Use
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generalized LS      Heteroscedasticity issues
(GLS)

Maximum Likelihood  Asymptotic efficiency needed
(MLE)

Kernel              Non-linear relationships
Regression

Bayesian            Prior knowledge available
Regression

Gaussian Process    Uncertainty quantification
Regression
```

---

## Simple Worked Example

**Problem:** Predict house price from square footage

```
Data:
SqFt    Price ($1000s)
1000    150
1500    200
2000    250
2500    300

Step 1: Plot the data
    Price ▲
    300   │          ●
    250   │      ●
    200   │  ●
    150   │●
        └─────────────► SqFt

Step 2: Fit regression line
    ŷ = 50 + 0.1*SqFt
    
    (Intercept = 50k, Slope = 0.1k per sq ft)

Step 3: Make predictions
    New house with 2200 sq ft:
    ŷ = 50 + 0.1*(2200) = $270k
```
---

## Key Formulas Summary

```
Basic Equation:              ŷ = b₀ + b₁*x

Slope (b₁):                 Cov(X,Y) / Var(X)

Intercept (b₀):             ȳ - b₁*x̄

R-squared:                  (Explained Variation) / (Total Variation)

Residual:                   e = y - ŷ

F-statistic p-value:        Overall model significance
T-statistic p-value:        Individual variable significance
```

---

## Common Interpretation Examples

```
Example 1: Sales Regression
ŷ = 5000 + 12*AdSpend

Meaning:
- Base sales (no ads) = $5,000
- Each $1 spent on ads → +$12 in sales
- Doubling ad spend → Sales increase by $12*Budget

Example 2: GPA Prediction  
ŷ = 0.5 + 0.05*StudyHours

Meaning:
- Base GPA (0 hours studying) = 0.5
- Each extra hour of study → +0.05 GPA points
- 20 hours more study → 1 point higher GPA
```

---

## When Regression Works Best

✅ **Good Use Cases:**
- Linear relationships exist
- Continuous dependent variable
- Decent sample size (30+)
- Predictable, stable relationships
- Making inferences about effects

❌ **Bad Use Cases:**
- Non-linear relationships
- Categorical outcomes (use logistic regression)
- Tiny samples
- Highly complex, chaotic systems
- Extreme outliers dominating

---

## Bottom Line

```
LINEAR REGRESSION:
├─ Find best-fit line through data
├─ Make predictions for new cases
├─ Understand how variables affect outcome
└─ Check 5 OLS assumptions to ensure reliability

KEY METRIC: R² tells how well model fits
KEY TEST: P-value tells if variables matter
KEY USE: ŷ = b₀ + b₁*x predicts new values
```

---

*Regression analysis is the foundation of predictive modeling. Master it!* 📊
