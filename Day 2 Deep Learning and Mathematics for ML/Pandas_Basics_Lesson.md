# Pandas Basics - Quick Lesson with Examples

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Source:** DataCamp Python Cheatsheet  
**Level:** Beginner

---

## What is Pandas?

Pandas is a powerful Python library for data manipulation and analysis. It provides:
- **DataFrame:** 2D table structure (rows and columns) - think of it like Excel spreadsheet
- **Series:** 1D array structure - single column of data

**Import statement:**
```python
import pandas as pd
```

---

## Part 1: Creating DataFrames

### 1.1 Create from Dictionary

```python
# Create DataFrame from dictionary
# Keys become column names
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

# Result:
#      name  age     city
# 0   Alice   25      NYC
# 1     Bob   30       LA
# 2  Charlie   35  Chicago
```

**Key concept:** Each key-value pair becomes a column

---

### 1.2 Create from List of Dictionaries

```python
# Each dictionary becomes a row
df = pd.DataFrame([
    {'name': 'Alice', 'age': 25, 'city': 'NYC'},
    {'name': 'Bob', 'age': 30, 'city': 'LA'},
    {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
])

# Result is the same as above
#      name  age     city
# 0   Alice   25      NYC
# 1     Bob   30       LA
# 2  Charlie   35  Chicago
```

**Visual comparison:**
```
Method 1: Dictionary of lists
{column: [values]}

Method 2: List of dictionaries
[{column: value, ...}, ...]

Both produce the same DataFrame!
```

---

### 1.3 Understanding DataFrame Structure

```
     Index  Column1   Column2  Column3
        0    value1   value2   value3
        1    value4   value5   value6
        2    value7   value8   value9
        
Rows are numbered 0, 1, 2, ... (index)
Columns have names: Column1, Column2, Column3
```

**Real example:**
```python
# House data
df = pd.DataFrame({
    'size': [2000, 1500, 2500],
    'bedrooms': [3, 2, 4],
    'price': [400000, 300000, 450000]
})

#    size  bedrooms   price
# 0  2000         3  400000
# 1  1500         2  300000
# 2  2500         4  450000
```

---

## Part 2: Selecting DataFrame Elements

### 2.1 Select a Single Column

```python
# Select by column name - returns a Series (1D)
df['name']

# Result:
# 0      Alice
# 1        Bob
# 2    Charlie
# Name: name, dtype: object
```

**Visual:**
```
Original DataFrame:
     name  age   city
0   Alice   25    NYC
1     Bob   30     LA
2  Charlie   35 Chicago

df['name'] selects this column:
   name
0  Alice
1    Bob
2  Charlie
```

---

### 2.2 Select Multiple Columns

```python
# Select multiple columns - returns a DataFrame (2D)
df[['name', 'city']]

# Result:
#      name     city
# 0   Alice      NYC
# 1     Bob       LA
# 2  Charlie  Chicago

# Note: Use double brackets [[]] for multiple columns
```

**Common mistake:**
```python
df['name', 'city']  # ❌ Wrong - gives error
df[['name', 'city']]  # ✅ Correct - use [[]]
```

---

### 2.3 Select Rows by Position

```python
# Select a single row by position (index)
df.iloc[0]  # First row (position 0)

# Result:
# name         Alice
# age             25
# city           NYC
# Name: 0, dtype: object

# Select multiple rows by position
df.iloc[0:2]  # Rows 0 and 1 (position 0 to 2, excluding 2)

# Result:
#      name  age   city
# 0   Alice   25    NYC
# 1     Bob   30     LA
```

**Visual:**
```
DataFrame positions (remember: 0-indexed):
     Index  name     age   city
        0    Alice    25    NYC  ← df.iloc[0]
        1    Bob      30    LA   ← df.iloc[1]
        2    Charlie  35    Chicago ← df.iloc[2]

df.iloc[0:2] selects rows at positions 0 and 1
(position 2 is excluded in range)
```

---

### 2.4 Select a Specific Element

```python
# Select element at row position 2, column position 3
df.iloc[2, 3]  # Returns single value

# Select element by row position and column name
df.loc[1, 'age']  # Returns 30

# Difference:
df.iloc[1, 2]  # Position-based: row at position 1, column at position 2
df.loc[1, 'age']  # Label-based: row at index 1, column named 'age'
```

**When to use:**
```python
df.iloc[]  # Use when you know position numbers
df.loc[]   # Use when you know column names
df[]       # Use to select column(s)
```

---

## Part 3: Manipulating DataFrames

### 3.1 Filter Rows (Using Conditions)

```python
# Get rows where age > 25
df.query('age > 25')

# Result:
#      name  age     city
# 1     Bob   30       LA
# 2  Charlie   35  Chicago

# Alternative syntax:
df[df['age'] > 25]  # Same result
```

**Visual:**
```
Original:
     name  age   city
0   Alice   25   NYC   ← Excluded (age = 25)
1     Bob   30   LA    ← Included (age > 25)
2  Charlie   35 Chicago ← Included (age > 25)

After filtering:
     name  age   city
1     Bob   30   LA
2  Charlie   35 Chicago
```

---

### 3.2 Add a New Column

```python
# Add a column for salary
df.assign(salary=[50000, 60000, 70000])

# Result:
#      name  age     city  salary
# 0   Alice   25      NYC   50000
# 1     Bob   30       LA   60000
# 2  Charlie   35  Chicago  70000

# Calculate new column from existing columns
df.assign(age_in_10_years=df['age'] + 10)

# Result:
#      name  age     city  age_in_10_years
# 0   Alice   25      NYC               35
# 1     Bob   30       LA               40
# 2  Charlie   35  Chicago              45
```

---

### 3.3 Drop Columns

```python
# Drop column(s) by name
df.drop(columns=['city'])

# Result:
#      name  age
# 0   Alice   25
# 1     Bob   30
# 2  Charlie   35

# Drop multiple columns
df.drop(columns=['age', 'city'])

# Result:
#      name
# 0   Alice
# 1     Bob
# 2  Charlie
```

---

### 3.4 Rename Columns

```python
# Rename one or multiple columns
df.rename(columns={'age': 'years', 'city': 'location'})

# Result:
#      name  years location
# 0   Alice     25      NYC
# 1     Bob     30       LA
# 2  Charlie    35  Chicago
```

---

### 3.5 Concatenate DataFrames

```python
# Create two DataFrames
df1 = pd.DataFrame({'name': ['Alice'], 'age': [25]})
df2 = pd.DataFrame({'name': ['Bob'], 'age': [30]})

# Combine vertically (stack on top of each other)
pd.concat([df1, df2])

# Result:
#     name  age
# 0  Alice   25
# 0    Bob   30

# Combine horizontally (side by side)
pd.concat([df1, df2], axis=1)

# Result:
#     name  age name  age
# 0  Alice   25  Bob   30
```

**Visual:**
```
Vertical (axis=0, default):
df1:          df2:
name age      name age
Alice 25      Bob  30

Result:
name  age
Alice 25
Bob   30

Horizontal (axis=1):
df1:     df2:
name age name age
Alice 25 Bob 30

Result:
name age name age
Alice 25 Bob  30
```

---

### 3.6 Remove Duplicate Rows

```python
# Create DataFrame with duplicates
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Alice'],
    'age': [25, 30, 25]
})

# Result:
#     name  age
# 0  Alice   25
# 1    Bob   30
# 2  Alice   25

# Remove duplicates
df.drop_duplicates()

# Result:
#     name  age
# 0  Alice   25
# 1    Bob   30
```

---

## Part 4: Data Analysis & Statistics

### 4.1 Basic Statistics

```python
# Calculate mean (average) of numeric columns
df.mean()

# Result:
# age    30.0
# salary 60000.0
# dtype: float64

# Get summary statistics
df.agg('mean')  # Or use specific function
```

---

### 4.2 Sort DataFrame

```python
# Sort by a column in ascending order (smallest to largest)
df.sort_values(by='age')

# Result:
#      name  age
# 0   Alice   25
# 1     Bob   30
# 2  Charlie   35

# Sort in descending order (largest to smallest)
df.sort_values(by='age', ascending=False)

# Result:
#      name  age
# 2  Charlie   35
# 1     Bob   30
# 0   Alice   25
```

---

### 4.3 Get Largest/Smallest Values

```python
# Get 2 rows with largest age values
df.nlargest(2, 'age')

# Result:
#      name  age
# 2  Charlie   35
# 1     Bob   30

# Get 2 rows with smallest age values
df.nsmallest(2, 'age')

# Result:
#     name  age
# 0  Alice   25
# 1    Bob   30
```

---

## Part 5: Real-World Example

### Complete Workflow

```python
# 1. Create DataFrame
houses = pd.DataFrame({
    'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St'],
    'size_sqft': [2000, 1500, 2500, 1800],
    'bedrooms': [3, 2, 4, 3],
    'price': [400000, 300000, 450000, 350000]
})

# 2. View the data
print(houses)
#        address  size_sqft  bedrooms   price
# 0  123 Main St       2000         3  400000
# 1  456 Oak Ave       1500         2  300000
# 2  789 Pine Rd       2500         4  450000
# 3  321 Elm St        1800         3  350000

# 3. Filter: Get houses with 3+ bedrooms
large_houses = houses.query('bedrooms >= 3')

# 4. Add column: Price per square foot
large_houses = large_houses.assign(price_per_sqft=large_houses['price'] / large_houses['size_sqft'])

# 5. Sort by price
large_houses = large_houses.sort_values(by='price')

# 6. Get top 2 most expensive
most_expensive = large_houses.nlargest(2, 'price')

# 7. Final result
print(most_expensive)
#        address  size_sqft  bedrooms   price  price_per_sqft
# 2  789 Pine Rd       2500         4  450000         180.00
# 0  123 Main St       2000         3  400000         200.00
```

**Step-by-step visualization:**
```
Step 1: Create DataFrame (4 houses)
Step 2: View all data
Step 3: Filter bedrooms >= 3 (removes 1 house)
        Now have 3 houses
Step 4: Add price_per_sqft column
        Now have 5 columns
Step 5: Sort by price (ascending)
Step 6: Get 2 most expensive
        Final result: 2 houses
```

---

## Quick Reference Table

| Task | Code | Returns |
|------|------|---------|
| Create from dict | `pd.DataFrame({...})` | DataFrame |
| Select column | `df['col']` | Series |
| Select columns | `df[['col1','col2']]` | DataFrame |
| Select row (pos) | `df.iloc[0]` | Series |
| Select rows (pos) | `df.iloc[0:3]` | DataFrame |
| Filter rows | `df.query('col > 5')` | DataFrame |
| Add column | `df.assign(new_col=[...])` | DataFrame |
| Drop column | `df.drop(columns=['col'])` | DataFrame |
| Rename column | `df.rename(columns={...})` | DataFrame |
| Concatenate | `pd.concat([df1,df2])` | DataFrame |
| Sort | `df.sort_values(by='col')` | DataFrame |
| Statistics | `df.mean()` | Series |
| Largest n rows | `df.nlargest(n,'col')` | DataFrame |

---

## Common Mistakes to Avoid

### ❌ Wrong → ✅ Correct

```python
# Mistake 1: Single brackets for multiple columns
df['name', 'age']          # ❌ Error
df[['name', 'age']]        # ✅ Correct

# Mistake 2: Forgetting to save result
df.assign(new_col=[1,2,3])  # ❌ Doesn't change df
df = df.assign(new_col=[1,2,3])  # ✅ Saves result

# Mistake 3: Wrong concatenation axis
pd.concat([df1, df2])      # ✅ Vertical (default)
pd.concat([df1, df2], axis=1)  # ✅ Horizontal

# Mistake 4: Zero-indexing confusion
df.iloc[3]                 # ✅ 4th row (0-indexed)
df.loc[3]                  # ✅ Row with index label 3
```

---

## Key Concepts Summary

✅ **DataFrame** - 2D table with rows and columns (like Excel)  
✅ **Series** - 1D array, single column of data  
✅ **Index** - Row labels (0, 1, 2, ...) for position  
✅ **Columns** - Column names for selection  
✅ **iloc** - Position-based selection (integer location)  
✅ **loc** - Label-based selection (using names/index)  
✅ **Zero-indexed** - First element is at position 0  

---

## Practice Exercises

**Exercise 1: Basic Selection**
```python
# Given:
df = pd.DataFrame({
    'product': ['Apple', 'Banana', 'Cherry'],
    'price': [1.5, 0.5, 2.0],
    'quantity': [10, 20, 15]
})

# Questions:
# 1. Select just the price column
# 2. Select rows 0 and 1
# 3. Get the price of item at position 2
```

**Exercise 2: Data Manipulation**
```python
# Add a column for total value (price × quantity)
# Filter products with quantity > 12
# Sort by total value
```

**Exercise 3: Real Data Analysis**
```python
# Create a DataFrame of students with name, grade, and score
# Filter students with score > 80
# Add a column for grade level
# Find student with highest score
```

---

## Next Steps

After mastering these basics:
1. **Learn groupby** - Group data by category and aggregate
2. **Learn merge** - Combine DataFrames by matching columns
3. **Learn data cleaning** - Handle missing values, duplicates
4. **Learn visualization** - Plot data using matplotlib/seaborn
5. **Apply to real projects** - Use with CSV files and datasets

---

## Useful Resources

```python
# Get help
df.head()       # Show first 5 rows
df.tail()       # Show last 5 rows
df.info()       # Show column types and missing values
df.describe()   # Show statistical summary
df.shape        # Show (rows, columns)
len(df)         # Show number of rows
```

---

*Pandas is essential for data science. Master these basics, and you're on your way!* 🚀
