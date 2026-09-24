# Python Topic of the Day #2: Joins in Python

**Author:** Saurabh Shirgaokar  
**Date:** Sep 22, 2026  

---

## Overview

Joins in Python are techniques for **combining or merging data** from different sources. While joins are commonly associated with databases (SQL), Python has several powerful ways to join data structures like strings, lists, and DataFrames.

**Why Learn This?**
```
✓ Essential for data manipulation
✓ Combines data from multiple sources
✓ Used constantly in data analysis
✓ Foundation for more complex operations
✓ Applies to strings, lists, and DataFrames
```

---

## Part 1: Understanding Joins

### 1.1 What is a Join?

A join combines two or more pieces of data into one unified result.

**Real-world examples:**
```
String Join: Combine words into a sentence
"hello" + "world" = "hello world"

List Join: Combine lists into one
[1, 2, 3] + [4, 5, 6] = [1, 2, 3, 4, 5, 6]

DataFrame Join: Combine data tables
Employee table + Salary table = Combined employee info
```

---

### 1.2 Types of Joins in Python

```
String Joins
├─ Concatenation: "hello" + "world"
└─ Using join(): " ".join(["hello", "world"])

List/Array Joins
├─ Concatenation: list1 + list2
├─ Extend: list1.extend(list2)
└─ Unpacking: [*list1, *list2]

DataFrame Joins
├─ Inner Join: Only matching rows
├─ Outer Join: All rows from both
├─ Left Join: All from left, matching from right
└─ Right Join: All from right, matching from left

Dictionary Joins
├─ Merge: Combine two dictionaries
└─ Update: Add one to another
```

---

## Part 2: String Joins

### 2.1 Combining Strings with +

The simplest join - combining text strings.

```python
# Combine two strings
first_name = "John"
last_name = "Doe"

full_name = first_name + " " + last_name
print(full_name)
# Output: John Doe
```

**More examples:**

```python
# Greeting message
greeting = "Hello" + ", " + "Welcome to Python!"
print(greeting)
# Output: Hello, Welcome to Python!

# Building a sentence
subject = "Python"
verb = "is"
adjective = "awesome"

sentence = subject + " " + verb + " " + adjective
print(sentence)
# Output: Python is awesome
```

---

### 2.2 Joining Lists of Strings

The `.join()` method combines a list of strings into one string.

```python
# Using join() with a list
words = ["Hello", "World", "Python"]
result = " ".join(words)
print(result)
# Output: Hello World Python

# Using different separators
numbers = ["1", "2", "3", "4", "5"]
dash_separated = "-".join(numbers)
print(dash_separated)
# Output: 1-2-3-4-5

# With empty separator (no space between)
letters = ["P", "y", "t", "h", "o", "n"]
word = "".join(letters)
print(word)
# Output: Python
```

**Why use join() instead of +?**

```python
# Using + (NOT recommended for many strings)
result = ""
for word in ["Python", "is", "powerful"]:
    result = result + " " + word
# Slow and creates many temporary strings

# Using join() (RECOMMENDED)
words = ["Python", "is", "powerful"]
result = " ".join(words)
# Much faster and cleaner!
```

---

### 2.3 Common String Join Patterns

**Create CSV data:**
```python
names = ["Alice", "Bob", "Charlie"]
csv_line = ",".join(names)
print(csv_line)
# Output: Alice,Bob,Charlie
```

**Create file paths:**
```python
parts = ["home", "user", "documents", "file.txt"]
path = "/".join(parts)
print(path)
# Output: home/user/documents/file.txt
```

**Create URLs:**
```python
domain = "example.com"
path_parts = ["api", "users", "profile"]
url = domain + "/" + "/".join(path_parts)
print(url)
# Output: example.com/api/users/profile
```

---

## Part 3: List Joins

### 3.1 Combining Lists with +

Combine two lists into a new list.

```python
# Combine lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]

combined = list1 + list2
print(combined)
# Output: [1, 2, 3, 4, 5, 6]

# Original lists stay unchanged
print(list1)  # [1, 2, 3]
print(list2)  # [4, 5, 6]
```

**Real example:**

```python
morning_tasks = ["Brush teeth", "Shower", "Breakfast"]
afternoon_tasks = ["Work", "Lunch", "Meeting"]
evening_tasks = ["Dinner", "Exercise", "Read"]

daily_schedule = morning_tasks + afternoon_tasks + evening_tasks

print(daily_schedule)
# Output: ['Brush teeth', 'Shower', 'Breakfast', 'Work', 'Lunch', 'Meeting', 'Dinner', 'Exercise', 'Read']
```

---

### 3.2 Extending Lists with .extend()

Modify original list by adding items from another.

```python
# Using extend() - modifies original list
list1 = [1, 2, 3]
list2 = [4, 5, 6]

list1.extend(list2)
print(list1)
# Output: [1, 2, 3, 4, 5, 6]

# list2 stays the same
print(list2)
# Output: [4, 5, 6]
```

**Difference between + and extend():**

```python
# Using + creates new list (doesn't change original)
list1 = [1, 2, 3]
list2 = [4, 5, 6]
result = list1 + list2
print(list1)  # Still [1, 2, 3] - unchanged!

# Using extend() changes original list
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list1.extend(list2)
print(list1)  # Now [1, 2, 3, 4, 5, 6] - changed!
```

---

### 3.3 Advanced List Joining

**Using unpacking (Python 3.5+):**

```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

# Unpack all lists into a new list
combined = [*list1, *list2, *list3]
print(combined)
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

**Adding items in the middle:**

```python
list1 = [1, 2, 5]
list2 = [3, 4]

# Insert list2 items in the middle of list1
combined = list1[:2] + list2 + list1[2:]
print(combined)
# Output: [1, 2, 3, 4, 5]
```

---

## Part 4: DataFrame Joins (Pandas)

### 4.1 Understanding DataFrame Joins

When working with data tables, joins combine information from two tables based on a common column.

```python
import pandas as pd

# Employee table
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana']
})

# Salary table
salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'salary': [50000, 60000, 70000, 80000]
})

print(employees)
#   emp_id     name
# 0      1    Alice
# 1      2      Bob
# 2      3  Charlie
# 3      4    Diana

print(salaries)
#   emp_id  salary
# 0      1   50000
# 1      2   60000
# 2      3   70000
# 3      4   80000
```

---

### 4.2 Inner Join

Keep only rows that match in BOTH tables.

```python
# Inner join on emp_id
result = employees.merge(salaries, on='emp_id', how='inner')

print(result)
#   emp_id     name  salary
# 0      1    Alice   50000
# 1      2      Bob   60000
# 2      3  Charlie   70000
# 3      4    Diana   80000

# All rows matched, so we get all 4
```

**When to use:**
```
You only want data for employees that have salary info
You need complete information from both tables
```

---

### 4.3 Left Join

Keep ALL rows from LEFT table, add matching rows from RIGHT table.

```python
# Employees table (left)
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
})

# Salaries table (right)
salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],  # Missing emp_id 5
    'salary': [50000, 60000, 70000, 80000]
})

# Left join keeps ALL employees
result = employees.merge(salaries, on='emp_id', how='left')

print(result)
#   emp_id     name   salary
# 0      1    Alice  50000.0
# 1      2      Bob  60000.0
# 2      3  Charlie  70000.0
# 3      4    Diana  80000.0
# 4      5      Eve      NaN  ← No salary info, so NaN
```

**When to use:**
```
You want to keep all records from the primary table (left)
But add additional info when available from the secondary table (right)
Example: All customers with their last purchase (if they made one)
```

---

### 4.4 Right Join

Keep ALL rows from RIGHT table, add matching rows from LEFT table.

```python
# Same tables
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana']
})

salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],  # Extra emp_id 5
    'salary': [50000, 60000, 70000, 80000, 90000]
})

# Right join keeps ALL salaries
result = employees.merge(salaries, on='emp_id', how='right')

print(result)
#   emp_id     name   salary
# 0      1    Alice  50000.0
# 1      2      Bob  60000.0
# 2      3  Charlie  70000.0
# 3      4    Diana  80000.0
# 4      5      NaN  90000.0  ← No employee name, so NaN
```

---

### 4.5 Outer Join

Keep ALL rows from BOTH tables.

```python
# Using outer join
result = employees.merge(salaries, on='emp_id', how='outer')

print(result)
#   emp_id     name   salary
# 0      1    Alice  50000.0
# 1      2      Bob  60000.0
# 2      3  Charlie  70000.0
# 3      4    Diana  80000.0
# 4      5      NaN  90000.0  ← From right table only
# 5      6      Eve      NaN  ← From left table only (if existed)
```

**When to use:**
```
You want a complete dataset with all records from both tables
You're okay with NaN (missing) values
Example: Complete view of all employees and all salary records
```

---

### 4.6 Join Types Visual Comparison

```
LEFT TABLE          RIGHT TABLE         RESULT BY JOIN TYPE
   A                   B
   1    ─────────────  ●                 INNER: 1 (only matching)
   2    ─────────────  ●                 LEFT:  1, 2, 3 (all from left)
   3                   ●                 RIGHT: 1, 2, ● (all from right)
        ─────────────  ●                 OUTER: 1, 2, 3, ● (all from both)
```

---

## Part 5: Dictionary Joins

### 5.1 Merging Dictionaries

Combine two dictionaries into one.

```python
# Method 1: Using unpacking (Python 3.5+)
dict1 = {"name": "Alice", "age": 25}
dict2 = {"city": "NYC", "job": "Engineer"}

merged = {**dict1, **dict2}
print(merged)
# Output: {'name': 'Alice', 'age': 25, 'city': 'NYC', 'job': 'Engineer'}
```

**Method 2: Using update()**

```python
# Update adds items from one dict to another
dict1 = {"name": "Alice", "age": 25}
dict2 = {"city": "NYC", "job": "Engineer"}

dict1.update(dict2)
print(dict1)
# Output: {'name': 'Alice', 'age': 25, 'city': 'NYC', 'job': 'Engineer'}

# Note: This modifies dict1, not dict2
print(dict2)
# Output: {'city': 'NYC', 'job': 'Engineer'} - unchanged
```

---

### 5.2 Handling Duplicate Keys

What happens when both dictionaries have the same key?

```python
# The right dictionary's value overwrites the left
dict1 = {"name": "Alice", "age": 25}
dict2 = {"age": 26, "city": "NYC"}

merged = {**dict1, **dict2}
print(merged)
# Output: {'name': 'Alice', 'age': 26, 'city': 'NYC'}
# Note: age is 26 (from dict2), not 25 (from dict1)
```

---

## Part 6: Combining Different Data Types

### 6.1 Lists of Dictionaries (Common in Data Science)

```python
# List of student records (each is a dictionary)
students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# List of scores
scores = [
    {"id": 1, "score": 85},
    {"id": 2, "score": 92}
]

# Convert to DataFrame for easy joining
import pandas as pd
df_students = pd.DataFrame(students)
df_scores = pd.DataFrame(scores)

# Join them
result = df_students.merge(df_scores, on='id')
print(result)
#   id name  score
# 0  1 Alice     85
# 1  2   Bob     92
```

---

### 6.2 Combining List of Lists

```python
# Two lists of data
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

# Create combined data
students = []
for name, age in zip(names, ages):
    students.append({"name": name, "age": age})

print(students)
# Output: [{'name': 'Alice', 'age': 25}, 
#          {'name': 'Bob', 'age': 30}, 
#          {'name': 'Charlie', 'age': 35}]
```

---

## Part 7: Real-World Examples

### Example 1: Combining Customer Data

```python
import pandas as pd

# Customer info
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana']
})

# Purchase history
purchases = pd.DataFrame({
    'customer_id': [1, 1, 2, 2, 3],
    'purchase_id': [101, 102, 201, 202, 301],
    'amount': [100, 150, 200, 50, 300]
})

# Join to get customer names with their purchases
result = customers.merge(purchases, on='customer_id', how='left')

print(result)
#   customer_id     name  purchase_id  amount
# 0            1    Alice          101     100
# 1            1    Alice          102     150
# 2            2      Bob          201     200
# 3            2      Bob          202      50
# 4            3  Charlie          301     300
# 5            4    Diana          NaN     NaN  ← No purchases
```

---

### Example 2: Building a URL from Components

```python
# URL components
components = {
    "protocol": "https",
    "domain": "example.com",
    "path": "/api/users",
    "query": "id=123"
}

# Build URL
url = components["protocol"] + "://" + \
      components["domain"] + \
      components["path"] + "?" + \
      components["query"]

print(url)
# Output: https://example.com/api/users?id=123

# Or cleaner with join
parts = [
    f"{components['protocol']}://{components['domain']}",
    components['path'],
    components['query']
]
url = "?".join(parts[:2]) + "?" + parts[2]
print(url)
# Output: https://example.com/api/users?id=123
```

---

### Example 3: Combining Sales Data from Multiple Stores

```python
# Store A sales
store_a = pd.DataFrame({
    'product': ['Apple', 'Banana', 'Orange'],
    'quantity': [100, 150, 80],
    'store': ['A', 'A', 'A']
})

# Store B sales
store_b = pd.DataFrame({
    'product': ['Apple', 'Banana', 'Grape'],
    'quantity': [120, 90, 200],
    'store': ['B', 'B', 'B']
})

# Combine all stores
all_sales = pd.concat([store_a, store_b], ignore_index=True)

print(all_sales)
#   product  quantity store
# 0   Apple       100     A
# 1  Banana       150     A
# 2  Orange        80     A
# 3   Apple       120     B
# 4  Banana        90     B
# 5   Grape       200     B
```

---

## Part 8: Common Mistakes to Avoid

### ❌ Mistake 1: Not Specifying Join Type

```python
# Without specifying how='inner'
result = df1.merge(df2, on='id')  # Defaults to inner join

# Better: Be explicit
result = df1.merge(df2, on='id', how='inner')
```

---

### ❌ Mistake 2: Forgetting the Key Column

```python
# Wrong - no column specified to join on
employees.merge(salaries)  # ❌ Unclear what to join on

# Correct - specify the join column
employees.merge(salaries, on='emp_id')  # ✅ Clear join key
```

---

### ❌ Mistake 3: Using + Instead of extend() When You Need to Modify

```python
# Using + doesn't change original
list1 = [1, 2, 3]
list1 = list1 + [4, 5, 6]  # ❌ Creates new list, need to reassign

# Better: Use extend() if you want to modify original
list1 = [1, 2, 3]
list1.extend([4, 5, 6])  # ✅ Modifies original, cleaner
```

---

### ❌ Mistake 4: Ignoring NaN Values After Join

```python
# After a left join, you might have NaN values
result = left_df.merge(right_df, how='left')

# Need to handle missing values
result.fillna(0)  # ✅ Replace NaN with 0
result.dropna()   # ✅ Or remove rows with NaN
```

---

### ❌ Mistake 5: Joining on Wrong Column Names

```python
# If column names don't match
employees = pd.DataFrame({'emp_id': [1,2,3]})
salaries = pd.DataFrame({'employee_id': [1,2,3]})

# This won't work - column names don't match
result = employees.merge(salaries, on='emp_id')  # ❌ Error!

# Use left_on and right_on
result = employees.merge(
    salaries, 
    left_on='emp_id', 
    right_on='employee_id'
)  # ✅ Works!
```

---

## Part 9: Quick Reference

### String Joins

```python
# Concatenation
"hello" + " " + "world"
# Output: "hello world"

# Join list of strings
" ".join(["hello", "world"])
# Output: "hello world"
```

### List Joins

```python
# Concatenate
[1, 2] + [3, 4]
# Output: [1, 2, 3, 4]

# Extend (modifies original)
list1.extend([3, 4])

# Unpacking
[*list1, *list2]
```

### DataFrame Joins

```python
# Inner join (only matches)
df1.merge(df2, on='key', how='inner')

# Left join (all from left)
df1.merge(df2, on='key', how='left')

# Right join (all from right)
df1.merge(df2, on='key', how='right')

# Outer join (all from both)
df1.merge(df2, on='key', how='outer')

# Concatenate rows
pd.concat([df1, df2])
```

---

## Part 10: Practice Exercises

### Exercise 1: String Joins
```python
# Given:
words = ["Python", "is", "powerful"]

# TODO:
# 1. Join with spaces
# 2. Join with dashes
# 3. Join with empty string (no separator)
```

### Exercise 2: List Joins
```python
# Given:
morning = ["Wake up", "Breakfast", "Commute"]
afternoon = ["Work", "Lunch", "Meeting"]
evening = ["Dinner", "Exercise", "Sleep"]

# TODO:
# 1. Combine all into daily_schedule
# 2. Add "Relax" between afternoon and evening
```

### Exercise 3: DataFrame Join
```python
import pandas as pd

# Employee table
employees = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})

# Department table
departments = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'dept': ['Engineering', 'Sales', 'HR']
})

# TODO:
# 1. Inner join (should have all rows)
# 2. Left join (should have all employees)
# 3. Compare the results
```

---

## Key Takeaways

✅ **Joins combine data** from different sources  
✅ **String joins** use + or .join()  
✅ **List joins** use + or .extend()  
✅ **DataFrame joins** have different types (inner, left, right, outer)  
✅ **Choose the right join type** for your data  
✅ **Handle missing values** after joins with NaN  
✅ **Be explicit** with join specifications  

---

## What's Next?

After mastering joins:
1. Learn **groupby** (group data by categories)
2. Learn **filtering** (select specific rows)
3. Learn **aggregation** (calculate summaries)
4. Combine all for powerful data analysis!

---

## Tips for Success

✅ **Practice with real data** - Use CSV files or APIs  
✅ **Visualize joins** - Draw diagrams to understand data flow  
✅ **Test different join types** - See which gives desired results  
✅ **Always check your results** - Verify row counts after joins  
✅ **Handle NaN values** - Don't ignore missing data  
✅ **Document your joins** - Comment why you chose that join type  

---

*Joins are fundamental to data manipulation. Master them, and you can combine any data sources!* 🚀
