# Day 3: Linear Algebra Applied to Machine Learning

**Course:** Mathematics for Machine Learning  
**Topic:** Linear Algebra Applications in ML  
**Date:** Sep 21, 2026

**Resource:** DeepLearning.AI

---

## 🎯 What is Day 3?

Welcome to **Advanced Linear Algebra**! Today you'll learn how linear algebra is actually applied in real machine learning problems. This is where math meets practice.

---

## 📚 What You'll Cover

### Core Topics
- **Systems of Linear Equations** - The foundation of ML problems
- **Matrices and Vectors** - Data representation
- **Singular vs Non-Singular Systems** - When solutions exist
- **Linear Regression** - Practical ML application
- **Multiple Inputs & Outputs** - Scaling to real problems
- **Supervised Learning Problems** - Classification and prediction

---

## Part 1: Systems of Linear Equations in ML

### 1.1 What is a System of Linear Equations?

**Real-world problem:** Wind turbine power prediction

```
A wind turbine's power output depends on:
- Wind speed
- Blade angle
- Air temperature

Power = w1×(wind_speed) + w2×(blade_angle) + w3×(temp) + b

This is ONE equation. Real systems have MULTIPLE equations.
```

**Why multiple equations?**
- Each data point is an equation
- More data = more equations
- We solve to find the best weights

---

### 1.2 System Representation

**Real scenario: 3 turbines, 3 features each**

```
Turbine 1: 10×w₁ + 45×w₂ + 20×w₃ + b = 500 kW (actual)
Turbine 2: 8×w₁ + 42×w₂ + 22×w₃ + b = 450 kW (actual)
Turbine 3: 12×w₁ + 48×w₂ + 18×w₃ + b = 550 kW (actual)

Goal: Find w₁, w₂, w₃, b that fit all three equations
```

**Why this matters for ML:**
```
Each sample = one equation
More samples = more constraints
Solution = best weights that satisfy all samples
```

---

### 1.3 Matrix Form of Systems

**Mathematical representation:**

```
[10  45  20]     [w₁]   [500]
[8   42  22]  ×  [w₂] = [450]
[12  48  18]     [w₃]   [550]

X (features) × w (weights) = y (targets)
```

**ML Application:**

```python
# Wind Turbine Dataset
Features (X):           Targets (y):
[wind, angle, temp]     [power]
[10, 45, 20]       →    500
[8, 42, 22]        →    450
[12, 48, 18]       →    550

Problem: Solve for w such that X·w ≈ y
```

---

## Part 2: Understanding Singular & Non-Singular Systems

### 2.1 What Makes a System Solvable?

**Non-Singular System (Good):**
```
All equations are independent and consistent
3 equations, 3 unknowns
→ Has a unique solution

Example:
x + y = 5
x - y = 1

Solution: x = 3, y = 2 (one answer)
```

**Visual:**
```
Two independent lines
    ↑
    |  x+y=5
    | /
    |/
  --|--→ They intersect at ONE point
   /|
  / | x-y=1
    |
```

---

### 2.2 Singular System (Problem)

**Singular System (Bad):**
```
Equations are dependent or inconsistent
→ No unique solution or no solution at all

Example (Dependent):
x + y = 5
2x + 2y = 10  (just 2× the first equation)

Infinite solutions! Any (x,y) where x+y=5 works.
```

**Example (Inconsistent):**
```
x + y = 5
x + y = 3

No solution! (Same x,y can't equal both 5 and 3)
```

**Visual:**
```
Two dependent lines        Two inconsistent lines
    ↑                           ↑
    |  x+y=5                    | x+y=5
    | /                         | /
    |/                          |/
  --|--→ Same line         --|--→ Parallel lines
   /|   Infinite solutions      (never meet)
  / |   2x+2y=10                No solution
```

---

### 2.3 Why This Matters for ML

**Singular = Bad for ML:**
```
• Features are highly correlated (redundant)
• Can't determine unique weights
• Model becomes unstable
• Predictions unreliable

Solution: Remove correlated features
```

**Non-Singular = Good for ML:**
```
• Features are independent
• Unique best weights found
• Model is stable
• Predictions reliable

This is what we want!
```

---

## Part 3: Linear Regression - The Classic ML Problem

### 3.1 The Linear Regression Setup

**Problem:** Predict house prices

```
Dataset:
House Size (sqft)  →  Price ($)
1000               →  250,000
1500               →  350,000
2000               →  450,000
2500               →  550,000
3000               →  650,000
```

**Goal:** Find the line that best fits this data

```
Price = w × Size + b

Where:
w = weight (slope) - price change per sq ft
b = bias (intercept) - base price
```

---

### 3.2 From One Equation to Multiple

**With ONE house:**
```
250,000 = w × 1000 + b
Infinite solutions! (many w,b combinations work)
```

**With FIVE houses:**
```
250,000 = w × 1000 + b  (Equation 1)
350,000 = w × 1500 + b  (Equation 2)
450,000 = w × 2000 + b  (Equation 3)
550,000 = w × 2500 + b  (Equation 4)
650,000 = w × 3000 + b  (Equation 5)

5 equations, 2 unknowns
→ Overdetermined system
→ No perfect solution
→ Find BEST fit (minimize error)
```

---

### 3.3 Matrix Form of Linear Regression

```
[1000  1]     [w]   [250,000]
[1500  1]     [b] = [350,000]
[2000  1]        [450,000]
[2500  1]        [550,000]
[3000  1]        [650,000]

X·θ = y

Where:
X = [size, 1] for each house
θ = [w, b] weights we're solving for
y = actual prices
```

---

## Part 4: Multiple Inputs & Outputs

### 4.1 More Complex Scenario

**Real estate prediction with multiple features:**

```
House Features:          Prediction:
Size (sqft)              Price ($)
Bedrooms
Bathrooms
Age
Location Score
Garage

7 inputs → 1 output
```

**Linear model:**
```
Price = w₁×size + w₂×beds + w₃×baths + w₄×age + w₅×location + w₆×garage + b
```

**Matrix form:**
```
[2000  3  2  10  8  2]     [w₁]   [400,000]
[1500  2  1   5  6  1]  ×  [w₂]   [300,000]
[2500  4  3  15  9  3]     [w₃] = [450,000]
[1800  3  2   8  7  2]  =  [w₄]   [350,000]
       ...              [w₅]   ...
                         [w₆]
                         [b ]

X (features) × w (weights) = y (prices)
```

---

### 4.2 Multiple Outputs Example

**Scenario:** Real estate company predicts multiple properties

```
Input (ONE house):
Size, Bedrooms, Bathrooms, Age, Location

Output (MULTIPLE predictions):
Expected selling price
Rental income potential
Days on market
```

**Matrix form:**
```
ONE house, multiple predictions:

[2000  3  2  10  8]     [w₁₁  w₁₂  w₁₃]   [Price]
                  ×  [w₂₁  w₂₂  w₂₃] = [Rental]
                     [w₃₁  w₃₂  w₃₃]   [Days]
                     [w₄₁  w₄₂  w₄₃]
                     [w₅₁  w₅₂  w₅₃]

Features × Weights = Predictions
```

---

## Part 5: Supervised Learning Problems

### 5.1 Regression Problem

**Goal:** Predict continuous values

```
Examples:
• House prices (continuous numbers)
• Temperature predictions (continuous)
• Stock price forecasts (continuous)
• Salary estimates (continuous)

Approach: Linear regression
Output: Single continuous value
```

---

### 5.2 Classification Problem

**Goal:** Predict categories

```
Examples:
• Email: Spam or Not Spam
• Image: Cat, Dog, or Bird
• Medical: Disease present or absent
• Loan: Approve or Deny

Approach: Logistic regression (uses linear algebra internally)
Output: Probability of each class
```

**Connection to Linear Algebra:**
```
Classification uses linear decision boundaries

Example (2D):
      ↑ Feature 2
      |  /← Decision line (linear algebra)
      | /  Cats above
      |/ ___
    --|----→ Feature 1
      |\ Dogs below
      | \
      
Equation of line: w₁×feature₁ + w₂×feature₂ + b = 0
```

---

### 5.3 Sequence Problem

**Goal:** Predict sequences

```
Examples:
• Next word in sentence
• Next stock price in time series
• Next frame in video

Approach: Recurrent neural networks (built on linear algebra)
Uses matrix operations to process sequence data
```

---

## Part 6: Practical ML Workflow Using Linear Algebra

### 6.1 Complete Example: House Price Prediction

```
STEP 1: Organize Data as Matrices
─────────────────────────────────
Dataset:
Size  Beds  Age  Price
2000   3   10   400k
1500   2    5   300k
2500   4   15   450k

Matrix form:
X = [2000  3  10]     y = [400]  (in thousands)
    [1500  2   5]         [300]
    [2500  4  15]         [450]


STEP 2: Set Up the Problem
─────────────────────────
Want to find w where: X·w ≈ y

w = [w₁]  (weight for size)
    [w₂]  (weight for bedrooms)
    [w₃]  (weight for age)


STEP 3: Solve Using Linear Algebra
──────────────────────────────────
Method: Least Squares Solution
w = (X^T·X)^(-1)·X^T·y

Where:
X^T = transpose of X
(X^T·X)^(-1) = inverse of product
This gives the BEST weights


STEP 4: Make Predictions
────────────────────────
New house: Size=2200, Beds=3, Age=8
New data point: [2200, 3, 8]

Prediction = [2200, 3, 8]·w + b
           = 2200×w₁ + 3×w₂ + 8×w₃ + b
           = Estimated Price
```

---

## Part 7: Why Linear Algebra Matters for Modern ML

### 7.1 It's Everywhere in ML

```
Linear Regression
    ↓ Uses matrix multiplication
    
Deep Neural Networks
    ↓ Uses matrix multiplication at each layer
    
Image Recognition
    ↓ Convolution = matrix operations on pixels
    
Natural Language Processing
    ↓ Word embeddings = vectors, transformations = matrices
    
Recommender Systems
    ↓ Matrix factorization breaks data into components
```

---

### 7.2 Computational Efficiency

```
Why matrices matter:
• Process millions of data points efficiently
• GPU acceleration works on matrices
• Batch processing (process many samples at once)
• Parallel computation

Example:
100 features × 1,000,000 samples = 100M operations
Using matrix math: Fast (seconds on GPU)
Using loops: Very slow (minutes)
```

---

## Part 8: Real-World Applications

### Application 1: Netflix Recommendations

```
Problem: Recommend movies to users

Data:
        Movie1  Movie2  Movie3  Movie4  ...
User1    5      3      -       4
User2    4      -      2       3
User3    -      5      5       -
...

Matrix form:
R = User-Movie rating matrix (sparse)

Solution:
Factor R into: R ≈ U × V^T

Where:
U = User features matrix
V = Movie features matrix

Multiply to predict missing ratings!
```

---

### Application 2: Autonomous Vehicle Control

```
Problem: Steer car based on camera input

Input: 640×480 image = 307,200 pixels (features)
Output: Steering angle (-45° to +45°)

Solution:
[pixel₁, pixel₂, ..., pixel₃₀₇₂₀₀] × [w₁, w₂, ..., w₃₀₇₂₀₀] = steering_angle

Learn weights that map images to steering
Uses matrix operations billions of times per second
```

---

### Application 3: Medical Diagnosis

```
Problem: Classify if patient has disease

Input features:
- Age
- Blood pressure
- Cholesterol
- Weight
- Glucose level
- ...

Output: Disease probability (0 to 1)

Solution:
[age, bp, chol, weight, glucose, ...] × [w₁, w₂, w₃, w₄, w₅, ...] = probability

Medical AI uses this pattern with deep networks
```

---

## Quick Reference

### Key Concepts

| Concept | Definition | ML Use |
|---------|-----------|--------|
| **Linear System** | Ax = b | ML problem: X·w = y |
| **Non-Singular** | Unique solution | Good features (independent) |
| **Singular** | No/infinite solutions | Bad features (redundant) |
| **Linear Regression** | Line fit to data | Predict continuous values |
| **Matrix Multiplication** | X·w | Network computation |
| **Transpose** | Flip rows/cols | Mathematical operations |

---

### Key Formulas

```
Linear Regression Setup:
X·w = y

Least Squares Solution:
w = (X^T·X)^(-1)·X^T·y

Prediction:
y_pred = X_new·w

Cost (Error):
J = mean((y_pred - y)²)
```

---

*Linear algebra is not just math. It's the language of machine learning.* 🚀
