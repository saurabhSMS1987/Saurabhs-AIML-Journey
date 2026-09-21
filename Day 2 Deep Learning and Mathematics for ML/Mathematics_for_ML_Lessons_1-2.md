# Mathematics for Machine Learning - Lessons 1-2 (Concise)

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Focus:** Essential concepts from Lessons 1-2 only

---

## Lesson 1: Systems of Equations & Matrices

### 1.1 What is a System of Linear Equations?

**Real-world problem:** Predict house price

```
Price depends on multiple factors:
2 × size + 3 × bedrooms + 5 × age = estimated_price

This is ONE equation. Real problems have MANY such relationships.
```

**System of equations:**
```
Example with multiple houses:
House 1: 2(2000) + 3(3) + 5(10) = 4039 (actual: 4000)
House 2: 2(1500) + 3(2) + 5(5) = 3031 (actual: 3000)
House 3: 2(2500) + 3(4) + 5(15) = 5095 (actual: 5100)

Problem: Find the best weights (2, 3, 5) that fit ALL examples
```

---

### 1.2 Vectors and Matrices

**Vector:** List of numbers representing one data point or feature
```
House features = [size, bedrooms, age]
             = [2000, 3, 10]
```

**Matrix:** 2D grid representing multiple data points
```
All houses:
        Size  Bedrooms  Age
House1  2000     3      10
House2  1500     2       5
House3  2500     4      15

Matrix notation:
     [2000  3  10]
X =  [1500  2   5]
     [2500  4  15]
```

---

### 1.3 Matrix Representation of System

**Standard form:**
```
2x + 3y = 8
4x + 1y = 10

Matrix form:
[2  3] [x]   [8]
[4  1] [y] = [10]

    A    ×  θ =   b

Where:
A = coefficient matrix (features)
θ = weights/unknowns
b = targets (prices)
```

**For housing example:**
```
[2000  3  10]     [w1]   [4000]
[1500  2   5]  ×  [w2] = [3000]
[2500  4  15]     [w3]   [5100]

     X     ×   w  =   y

Find w that makes X·w ≈ y
```

---

### 1.4 Matrix Operations

**Matrix-Vector Multiplication:**
```
Result of one prediction:
[2000  3  10] × [0.5]   = 2000(0.5) + 3(0.5) + 10(0.5)
                [0.5]     = 1005.5
                [0.5]

(features) × (weights) = prediction
```

**Why it matters:** Neural network forward pass is just repeated matrix multiplication

```
Input → [Weight Matrix] → Hidden → [Weight Matrix] → Output
         (linear algebra)          (linear algebra)
```

---

## Lesson 2: Introduction to Optimization

### 2.1 The Cost Function

**Goal:** Find weights w that minimize prediction error

**Cost (Loss) Function:**
```
J(w) = Average squared error

J(w) = (1/m) × Σ(predicted - actual)²

Example with 3 houses:
Error1 = (1005.5 - 4000)² = big error
Error2 = (752.5 - 3000)² = big error
Error3 = (1252.5 - 5100)² = big error

J(w) = (Error1 + Error2 + Error3) / 3

Goal: Make J(w) as small as possible
```

---

### 2.2 Derivatives (Rate of Change)

**Simple example:**
```
Cost function J(w) = (w - 5)²

At w = 1: J = (1-5)² = 16 (high cost)
At w = 3: J = (3-5)² = 4  (lower cost)
At w = 5: J = (5-5)² = 0  (minimum!)

Derivative dJ/dw tells us:
- Direction to move (positive/negative)
- How steep the slope is
```

**Interpretation:**
```
dJ/dw > 0: Move w to the LEFT (decrease w)
dJ/dw < 0: Move w to the RIGHT (increase w)
dJ/dw = 0: Found minimum (stop!)
```

---

### 2.3 Gradient Descent Algorithm

**The idea:** Walk downhill to find minimum cost

```
1. Start with random weights w
2. Calculate slope (derivative) at current w
3. Move opposite to slope (downhill direction)
4. Repeat until you reach bottom
```

**Formula:**
```
w_new = w_old - α × (dJ/dw)

Where:
α = learning rate (step size)
dJ/dw = slope/gradient (which direction)

Example:
w_old = 10
dJ/dw = 4 (steep positive slope)
α = 0.1

w_new = 10 - 0.1 × 4 = 9.6  (moved left)
```

**Visual:**
```
Cost
  |      ╱╱╱  
  |    ╱╱●╱   ← Start here
  |   ╱╱  ╱
  |  ╱╱  ╱
  | ╱╱  ╱     ← Minimum
  |╱╱──╱
  └────────→ Weights
  
Each step, we move downhill (gradient descent)
```

---

### 2.4 Partial Derivatives (Multiple Weights)

**Problem:** Housing model has 3 weights (size, bedrooms, age)
```
Price = w1×size + w2×bedrooms + w3×age

Need to know:
- How does cost change if we adjust w1?
- How does cost change if we adjust w2?
- How does cost change if we adjust w3?
```

**Partial Derivatives:**
```
∂J/∂w1 = how cost changes with w1
∂J/∂w2 = how cost changes with w2
∂J/∂w3 = how cost changes with w3
```

**Update all weights:**
```
w1_new = w1_old - α × (∂J/∂w1)
w2_new = w2_old - α × (∂J/∂w2)
w3_new = w3_old - α × (∂J/∂w3)

Do this for ALL 3 weights simultaneously
```

---

## Key Concepts Summary

### Lesson 1: Linear Algebra Foundation

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Vector** | 1D list of numbers | One data point (features) |
| **Matrix** | 2D grid of numbers | All data points together |
| **Ax = b** | Matrix equation form | ML problem representation |
| **Matrix multiplication** | Combining matrices | Neural network computation |

**Simple example:**
```
House data (matrix) × Weights (vector) = Predictions (vector)
       X            ×        w         =        y
```

---

### Lesson 2: Optimization

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Cost function** | Measure of error | What we want to minimize |
| **Derivative** | Rate of change | Shows which direction to move |
| **Gradient descent** | Optimization algorithm | How to find best weights |
| **Learning rate** | Step size | Controls optimization speed |

**Simple example:**
```
Cost goes down as we iterate:
Iteration 1: J = 1000 (bad predictions)
Iteration 2: J = 900
Iteration 3: J = 800
...
Iteration 100: J = 50 (good predictions!)
```

---

## How Lessons 1-2 Connect

### The Process:

```
1. LESSON 1: Represent problem
   ↓
   Data (matrix X) × Weights (w) = Predictions (y)

2. LESSON 2: Find best weights
   ↓
   Define cost: J(w) = error²
   ↓
   Use gradient descent:
   w_new = w_old - α × (∂J/∂w)
   ↓
   Repeat until J(w) is small
```

---

## Real Example: Housing Price

**Given:**
```
3 houses with features and actual prices:

House  Size  Bedrooms  Age  Price
  1    2000     3      10   400k
  2    1500     2       5   300k
  3    2500     4      15   450k
```

**Step 1 (Lesson 1):** Represent as matrices
```
X = [2000  3  10]     y = [400]
    [1500  2   5]         [300]
    [2500  4  15]         [450]

Want to find w = [w1, w2, w3] such that X·w ≈ y
```

**Step 2 (Lesson 2):** Use gradient descent to find w
```
Start: w = [0.1, 0.1, 0.1]

Iteration 1:
- Calculate predictions: X·w
- Calculate cost: J = mean squared error
- Calculate gradients: ∂J/∂w1, ∂J/∂w2, ∂J/∂w3
- Update: w = w - 0.01 × gradients

Iteration 2: (same process, w is getting better)
...

After many iterations:
w ≈ [0.2, 100, -5]  (weights that make good predictions)
```

---

## Why This Matters for Neural Networks

**Linear Regression (Lessons 1-2):**
```
y = w·x + b  (simple line)

Training: Use gradient descent to find optimal w
```

**Neural Networks:**
```
y = Network(x)  (complex function with many layers)
     ↓
   Multiple matrix multiplications (Lesson 1)
     ↓
   Each layer: w·x + b with activation function
     ↓
   Cost function (Lesson 2)
     ↓
   Gradient descent on ALL weights (Lesson 2)
     ↓
   Backpropagation = repeated use of chain rule
```

**Same principles, just more complex!**

---

## Essential Takeaways

✅ **Lesson 1:** Data and predictions are matrix operations
✅ **Lesson 2:** Finding best weights is an optimization problem
✅ **Combined:** Matrix math + calculus = machine learning

**The formula that drives everything:**
```
w_new = w_old - α × ∇J(w)

Where:
- w = weights
- α = learning rate
- ∇J = gradient (partial derivatives)

This one formula is used to train:
- Linear regression
- Neural networks
- Deep learning models
```

---

*Master these two lessons, and you understand the heart of machine learning.* 🚀
