# Assignment 5: NumPy Exercise – Employee Happiness Survey

*Oct 29, 2026 · Saurabh S*

> [!NOTE]
> **Source:** NumPy exercise from the **CodeBasics Python course**, covering the NumPy lectures.

As Peter Pandey, I helped AtliQ's HR team analyse an employee happiness survey. I combined employee details (ID, department, years at AtliQ) with survey scores (1–10) and summarised the results.

## Tasks at a glance

| Task | What I did | Result |
| --- | --- | --- |
| 1 | Merged details and scores with `np.hstack` | One 9 × 5 table |
| 2 | Pulled out the score column with `merged[:, 4]` | `8, 10, 9, 6, 7, 8, 9, 5, 7` |
| 3 | Sorted the scores after converting them to numbers | `5, 6, 7, 7, 8, 8, 9, 9, 10` |
| 4 | Looped through rows to print ID and department | e.g. `ID: 101, Department: Sales` |
| 5 | Looped through rows to print ID and score | e.g. `ID: 101, Happiness Score: 8` |
| 6 | Converted scores with `.astype(float)` | Numeric scores, ready for maths |
| 7 | Averaged all scores with `np.mean` | **7.67** |
| 8 | Listed departments with `np.unique` | `HR, IT, Sales` |
| 9 | Filtered HR rows and averaged their scores | **8.33** |

## Key code

```python
import numpy as np

employee_details = np.array([
    [101, 'Sales', 3], [102, 'HR', 5], [103, 'IT', 2],
    [104, 'Sales', 8], [105, 'IT', 6], [106, 'HR', 4],
    [107, 'IT', 7], [108, 'Sales', 1], [109, 'HR', 3]])
survey_results = np.array([
    [101, 8], [102, 10], [103, 9], [104, 6], [105, 7],
    [106, 8], [107, 9], [108, 5], [109, 7]])

# my extra check: hstack doesn't match by ID, so confirm the rows line up first
# employee IDs are stored as text ('101') and survey IDs as numbers (101), so convert before comparing
print(np.all(employee_details[:, 0] == survey_results[:, 0].astype(str)))   # True

merged = np.hstack((employee_details, survey_results))
scores = merged[:, 4].astype(float)

print(np.sort(scores))                  # [ 5.  6.  7.  7.  8.  8.  9.  9. 10.]
print(round(np.mean(scores), 2))        # 7.67: company-wide average
print(np.unique(merged[:, 1]))          # ['HR' 'IT' 'Sales']

hr_scores = merged[merged[:, 1] == 'HR'][:, 4].astype(float)
print(round(np.mean(hr_scores), 2))     # 8.33: HR's own average
```

## Two things worth noting

- **Convert before sorting.** After `hstack`, every value is text, and text sorts character by character, so `'10'` would come *before* `'5'`. The solution correctly converts with `.astype(int)` before sorting.
- **Check IDs before `hstack`.** The exercise works because both arrays happen to be in the same employee order. I added a one-line check to confirm that, since a mismatch would attach scores to the wrong people without any error. My first attempt at the check returned `False` even though the IDs match. The employee IDs had become text (`'101'`) because they share an array with department names, while the survey IDs were still numbers (`101`). Converting with `.astype(str)` fixed the comparison. That's the same type trap, showing up in a new place.

## What stuck with me

The final task combined everything from the module: filter rows with a condition, slice one column, convert its type and summarise it. That's the same chain I'd use to work out, say, the average claim value for one provider in an audit population.
