# Takeaways: NumPy

*Oct 29, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *NumPy – Takeaways* from the **CodeBasics Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the NumPy module, kept handy for quick revision.

## Introduction and benefits

- NumPy (Numeric Python) is the go-to library for data analysis, machine learning and scientific computing. Anyone doing data analysis in Python uses it almost daily.
- Compared with plain Python lists, NumPy arrays offer:
  - **less memory** use,
  - **faster** operations, and
  - **convenient functions** for a wide range of maths.

## Basic operations

- There's no need to memorise the syntax. In practice, everyone checks the NumPy documentation, ChatGPT or Google.
- `sum()`, `min()`, `max()` and `std()` give quick statistical summaries.
- Four attributes describe an array:

| Attribute | Tells me |
| --- | --- |
| `ndim` | Number of dimensions |
| `itemsize` | Bytes per element |
| `size` | Total number of elements |
| `shape` | Size of each dimension, e.g. `(2, 3)` |

## Slicing, stacking and splitting

- Indexing and slicing work like Python lists, with an extra position for columns: `arr[row, col]`.
- `np.vstack` stacks arrays **on top** of each other, and `np.hstack` places them **side by side**.
- `np.vsplit` splits an array by rows, and `np.hsplit` splits it by columns.

## All together

```python
import numpy as np

# rows: City Hospital, Lakeside Clinic | columns: Jan, Feb, Mar billing ($000s)
q1 = np.array([[420, 435, 410], [180, 175, 390]])
q2 = np.array([[425, 430, 415], [185, 400, 410]])

half_year = np.hstack((q1, q2))         # 2 × 6: six months side by side
print(half_year.shape)                  # (2, 6)
print(half_year.sum(axis=1))            # [2535 1740]: total per provider
print(half_year[1, :].std().round(1))   # 110.2: Lakeside's billing swings widely
```
