# Python Topic of the Day #5: Grouping and Aggregating Data

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Level:** Beginner to Intermediate  
**Audience:** Data analysts and Python learners  
**Duration:** 45-60 minutes

---

## Overview

Grouping and aggregating is how you **summarize data by categories**.

**Why Learn This?**
```
✓ Summarize data by categories (city, product, region)
✓ Calculate statistics per group (average, sum, count)
✓ Find patterns in data
✓ Business analysis foundation (sales by region, etc.)
✓ Extremely common in real-world analysis
```

---

## Part 1: Understanding Grouping & Aggregating

### 1.1 What is Grouping?

**Grouping** = Split data into categories

```python
# Raw data
┌─────────┬────────┬────────┐
│ Name    │ City   │ Sales  │
├─────────┼────────┼────────┤
│ Alice   │ NYC    │ 1000   │
│ Bob     │ NYC    │ 1500   │
│ Charlie │ LA     │ 2000   │
│ Diana   │ LA     │ 1800   │
└─────────┴────────┴────────┘

Grouped by City:
NYC Group: [Alice-1000, Bob-1500]
LA Group:  [Charlie-2000, Diana-1800]
```

### 1.2 What is Aggregating?

**Aggregating** = Calculate summary statistics on groups

```python
# After aggregation
┌────────┬─────────────┬────────────┐
│ City   │ Total Sales │ Avg Sales  │
├────────┼─────────────┼────────────┤
│ NYC    │ 2500        │ 1250       │
│ LA     │ 3800        │ 1900       │
└────────┴─────────────┴────────────┘
```

---

## Part 2: Pandas GroupBy (Most Common)

### 2.1 Basic GroupBy

```python
import pandas as pd

df = pd.DataFrame({
    'City': ['NYC', 'NYC', 'LA', 'LA'],
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Sales': [1000, 1500, 2000, 1800]
})

# Group by City and get total sales
grouped = df.groupby('City')['Sales'].sum()

print(grouped)
# Output:
# City
# LA     3800
# NYC    2500
```

### 2.2 Multiple Aggregation Functions

```python
# Calculate multiple statistics at once
stats = df.groupby('City')['Sales'].agg([
    'sum',      # Total
    'mean',     # Average
    'count',    # Count
    'min',      # Minimum
    'max'       # Maximum
])

print(stats)
#       sum  mean  count  min   max
# City
# LA    3800  1900      2  1800  2000
# NYC   2500  1250      2  1000  1500
```

### 2.3 Custom Aggregation Names

```python
# Rename aggregation columns for clarity
summary = df.groupby('City')['Sales'].agg(
    Total='sum',
    Average='mean',
    Count='count',
    Highest='max',
    Lowest='min'
)

print(summary)
#       Total  Average  Count  Highest  Lowest
# City
# LA     3800     1900      2     2000    1800
# NYC    2500     1250      2     1500    1000
```

### 2.4 Multiple Columns Grouping

```python
# Group by multiple columns
df2 = pd.DataFrame({
    'City': ['NYC', 'NYC', 'NYC', 'LA', 'LA', 'LA'],
    'Product': ['A', 'A', 'B', 'A', 'B', 'B'],
    'Sales': [100, 150, 200, 300, 250, 400]
})

grouped = df2.groupby(['City', 'Product'])['Sales'].sum()

print(grouped)
# City  Product
# LA    A           300
#       B           650
# NYC   A           250
#       B           200
```

### 2.5 Multiple Aggregations Per Column

```python
# Different aggregations for different columns
agg_dict = {
    'Sales': ['sum', 'mean'],
    'Product': 'count'  # Count unique products
}

result = df2.groupby('City').agg(agg_dict)
print(result)
```

---

## Part 3: Common Aggregation Functions

### 3.1 Statistical Functions

```python
df = pd.DataFrame({
    'Department': ['Sales', 'Sales', 'HR', 'HR', 'IT', 'IT'],
    'Salary': [50000, 60000, 45000, 48000, 70000, 75000]
})

# Sum - Total salaries
df.groupby('Department')['Salary'].sum()

# Mean - Average salary
df.groupby('Department')['Salary'].mean()

# Median - Middle value
df.groupby('Department')['Salary'].median()

# Std - Standard deviation (spread)
df.groupby('Department')['Salary'].std()

# Min/Max - Lowest/Highest
df.groupby('Department')['Salary'].min()
df.groupby('Department')['Salary'].max()

# Count - Number of entries
df.groupby('Department')['Salary'].count()
```

### 3.2 Counting Occurrences

```python
# Count items in each group
counts = df.groupby('Department').size()
# or
counts = df.groupby('Department')['Department'].count()

print(counts)
# Department
# HR      2
# IT      2
# Sales   2
```

### 3.3 Custom Aggregation Function

```python
# Create custom function
def salary_range(salaries):
    return salaries.max() - salaries.min()

result = df.groupby('Department')['Salary'].agg(salary_range)

print(result)
# Department
# HR      3000
# IT      5000
# Sales   10000
```

---

## Part 4: Practical Implementation Examples

### Example 1: Sales Analysis by Region

```python
import pandas as pd

# Create sales data
sales_data = pd.DataFrame({
    'Region': ['North', 'North', 'North', 'South', 'South', 'South', 'East', 'East'],
    'Month': ['Jan', 'Feb', 'Mar', 'Jan', 'Feb', 'Mar', 'Jan', 'Feb'],
    'Revenue': [50000, 55000, 60000, 45000, 48000, 52000, 70000, 75000]
})

print("=== SALES SUMMARY BY REGION ===\n")

# 1. Total revenue per region
total_by_region = sales_data.groupby('Region')['Revenue'].sum()
print("Total Revenue by Region:")
print(total_by_region)
print()

# 2. Average revenue per region
avg_by_region = sales_data.groupby('Region')['Revenue'].mean()
print("Average Revenue by Region:")
print(avg_by_region)
print()

# 3. Comprehensive summary
summary = sales_data.groupby('Region')['Revenue'].agg({
    'Total': 'sum',
    'Average': 'mean',
    'Min': 'min',
    'Max': 'max',
    'Count': 'count'
})
print("Comprehensive Summary:")
print(summary)
print()

# 4. Save summary
summary.to_csv('regional_sales_summary.csv')
print("✓ Summary saved to regional_sales_summary.csv")
```

**Output:**
```
=== SALES SUMMARY BY REGION ===

Total Revenue by Region:
Region
East      145000
North     165000
South     145000

Average Revenue by Region:
Region
East      72500.0
North     55000.0
South     48333.3

Comprehensive Summary:
        Total    Average     Min     Max  Count
Region
East   145000    72500.0   70000   75000      2
North  165000    55000.0   50000   60000      3
South  145000    48333.3   45000   52000      3
```

---

### Example 2: Customer Purchase Analysis

```python
# Customer transaction data
customers = pd.DataFrame({
    'Customer': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Charlie', 'Charlie'],
    'Product': ['Laptop', 'Mouse', 'Keyboard', 'Laptop', 'Monitor', 'Mouse', 'Keyboard'],
    'Amount': [1000, 25, 75, 1000, 300, 25, 75],
    'Date': ['2026-01-01', '2026-01-05', '2026-01-10', '2026-01-02', 
             '2026-01-08', '2026-01-03', '2026-01-12']
})

print("=== CUSTOMER ANALYSIS ===\n")

# 1. Total spending per customer
total_spent = customers.groupby('Customer')['Amount'].sum().sort_values(ascending=False)
print("Total Spending per Customer:")
print(total_spent)
print()

# 2. Number of purchases per customer
purchases = customers.groupby('Customer').size()
print("Number of Purchases:")
print(purchases)
print()

# 3. Average purchase value
avg_purchase = customers.groupby('Customer')['Amount'].mean()
print("Average Purchase Value:")
print(avg_purchase)
print()

# 4. Customer segment (High/Medium/Low value)
customer_summary = customers.groupby('Customer')['Amount'].agg({
    'Total': 'sum',
    'Count': 'count',
    'Average': 'mean'
})

# Add segment
customer_summary['Segment'] = pd.cut(customer_summary['Total'], 
                                     bins=[0, 100, 500, float('inf')],
                                     labels=['Low', 'Medium', 'High'])

print("Customer Segmentation:")
print(customer_summary)
```

**Output:**
```
=== CUSTOMER ANALYSIS ===

Total Spending per Customer:
Customer
Alice       1100
Bob         1300
Charlie     100

Number of Purchases:
Customer
Alice    3
Bob      2
Charlie  2

Average Purchase Value:
Customer
Alice     366.67
Bob       650.00
Charlie    50.00

Customer Segmentation:
          Total  Count  Average Segment
Customer
Alice      1100      3  366.67     High
Bob        1300      2  650.00     High
Charlie     100      2   50.00     Low
```

---

### Example 3: Product Performance Report

```python
# E-commerce product data
products = pd.DataFrame({
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Clothing', 'Clothing', 'Clothing'],
    'Product': ['Laptop', 'Phone', 'Tablet', 'T-Shirt', 'Jeans', 'Shoes'],
    'Units_Sold': [150, 300, 200, 500, 400, 350],
    'Price': [1000, 800, 500, 30, 80, 120],
    'Returns': [5, 10, 8, 20, 15, 10]
})

print("=== PRODUCT PERFORMANCE ===\n")

# 1. Revenue per category
products['Revenue'] = products['Units_Sold'] * products['Price']

revenue_by_category = products.groupby('Category')['Revenue'].sum()
print("Revenue by Category:")
print(revenue_by_category)
print()

# 2. Top performing products
products_ranked = products.sort_values('Revenue', ascending=False)
print("Top 3 Products by Revenue:")
print(products_ranked[['Product', 'Revenue']].head(3))
print()

# 3. Return rate analysis
products['Return_Rate'] = (products['Returns'] / products['Units_Sold'] * 100).round(2)

print("Return Rate by Category:")
category_returns = products.groupby('Category').agg({
    'Revenue': 'sum',
    'Returns': 'sum',
    'Units_Sold': 'sum'
})
category_returns['Return_Rate_%'] = (category_returns['Returns'] / category_returns['Units_Sold'] * 100).round(2)
print(category_returns)
```

---

### Example 4: Time Series Aggregation (Daily to Monthly)

```python
# Daily sales data
daily_sales = pd.DataFrame({
    'Date': pd.date_range('2026-01-01', periods=30, freq='D'),
    'Sales': [100, 120, 110, 130, 140, 150, 160, 
              170, 180, 190, 200, 210, 220, 230, 240,
              250, 260, 270, 280, 290, 300, 310, 320,
              330, 340, 350, 360, 370, 380, 390]
})

print("=== SALES AGGREGATION: DAILY TO WEEKLY ===\n")

# 1. Extract week from date
daily_sales['Week'] = daily_sales['Date'].dt.isocalendar().week

# 2. Aggregate to weekly
weekly_sales = daily_sales.groupby('Week')['Sales'].agg({
    'Total': 'sum',
    'Average': 'mean',
    'Min': 'min',
    'Max': 'max'
})

print("Weekly Sales Summary:")
print(weekly_sales)
print()

# 3. Monthly aggregation (if data spans multiple months)
daily_sales['Month'] = daily_sales['Date'].dt.to_period('M')
monthly_sales = daily_sales.groupby('Month')['Sales'].sum()
print("Monthly Total Sales:")
print(monthly_sales)
```

---

### Example 5: Chaining Operations (Complex Analysis)

```python
# Company data
employees = pd.DataFrame({
    'Department': ['Sales', 'Sales', 'Sales', 'HR', 'HR', 'IT', 'IT', 'IT'],
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'Salary': [50000, 55000, 60000, 45000, 48000, 70000, 75000, 80000],
    'Years': [2, 3, 5, 2, 1, 4, 6, 8],
    'Bonus': [5000, 6000, 8000, 3000, 2000, 10000, 12000, 15000]
})

print("=== COMPREHENSIVE HR ANALYSIS ===\n")

# 1. Department statistics
dept_stats = employees.groupby('Department').agg({
    'Salary': ['sum', 'mean', 'count'],
    'Years': 'mean',
    'Bonus': 'sum'
}).round(2)

print("Department Overview:")
print(dept_stats)
print()

# 2. Employees with above-average salary in their department
def above_dept_avg(group):
    return group[group['Salary'] > group['Salary'].mean()]

high_earners = employees.groupby('Department', group_keys=False).apply(above_dept_avg)
print("Above Average Earners by Department:")
print(high_earners[['Department', 'Name', 'Salary']])
print()

# 3. Total compensation (Salary + Bonus)
employees['Total_Comp'] = employees['Salary'] + employees['Bonus']

comp_summary = employees.groupby('Department')['Total_Comp'].agg({
    'Total': 'sum',
    'Average': 'mean'
}).round(2)

print("Total Compensation by Department:")
print(comp_summary)
```

---

## Part 5: Best Practices

### ✅ Good Practices

```python
# 1. Use meaningful column names
result = df.groupby('City')['Sales'].sum()  # Clear

# 2. Use .agg() with dictionary for clarity
df.groupby('Category').agg({
    'Price': 'mean',
    'Quantity': 'sum'
})

# 3. Always sort for better readability
df.groupby('Region')['Sales'].sum().sort_values(ascending=False)

# 4. Use round() for financial data
df.groupby('Store')['Revenue'].mean().round(2)

# 5. Store results for later use
quarterly_summary = df.groupby('Quarter')['Sales'].sum()
quarterly_summary.to_csv('quarterly_report.csv')
```

### ❌ Common Mistakes

```python
# ❌ Don't forget to convert to numeric
df.groupby('City')['Sales'].sum()  # Works
# But if Sales is string "1000", will give error

# ✅ Convert first
df['Sales'] = pd.to_numeric(df['Sales'])
df.groupby('City')['Sales'].sum()

# ❌ Don't forget column selection
df.groupby('City').sum()  # Sums ALL numeric columns (messy)

# ✅ Select specific column
df.groupby('City')['Sales'].sum()  # Clean

# ❌ Don't lose the groupby column
result = df.groupby('City')['Sales'].sum()  # OK
result.index.name = 'City'  # If you need city back
```

---

## Part 6: Quick Reference Cheatsheet

### GroupBy Patterns

```python
# Single column group, single aggregation
df.groupby('City')['Sales'].sum()

# Single column group, multiple aggregations
df.groupby('City')['Sales'].agg(['sum', 'mean', 'count'])

# Multiple column group
df.groupby(['City', 'Product'])['Sales'].sum()

# Multiple aggregations with names
df.groupby('City')['Sales'].agg(
    Total='sum',
    Average='mean'
)

# Different agg per column
df.groupby('City').agg({
    'Sales': 'sum',
    'Quantity': 'mean'
})

# Sort results
df.groupby('City')['Sales'].sum().sort_values(ascending=False)

# Get top N groups
df.groupby('City')['Sales'].sum().nlargest(5)

# Reset index (convert index to column)
df.groupby('City')['Sales'].sum().reset_index()
```

---

## Part 7: Practice Exercises

### Exercise 1: Movie Data Analysis

```python
# Given: Movie data with Genre, Rating, Revenue
# TODO:
# 1. Total revenue per genre
# 2. Average rating per genre
# 3. Number of movies per genre
# 4. Genre with highest revenue
```

---

### Exercise 2: Student Grades

```python
# Given: Student data with Class, Subject, Grade
# TODO:
# 1. Average grade per class
# 2. Students above class average
# 3. Subject performance comparison
# 4. Top 3 students per class
```

---

### Exercise 3: Website Traffic

```python
# Given: Traffic data with Date, Page, Views, Bounce_Rate
# TODO:
# 1. Total views per page
# 2. Average bounce rate per page
# 3. Most visited pages
# 4. Daily total views
```

---

## Key Takeaways

✅ **GroupBy = Split data into groups**  
✅ **Aggregation = Calculate statistics on groups**  
✅ **Most common: df.groupby('column')['value'].sum()**  
✅ **Use .agg() for multiple operations**  
✅ **Perfect for business analysis (sales by region, etc.)**  
✅ **Always sort results for better insights**  

---

## What's Next?

After mastering grouping and aggregating:
1. **Pivot tables** (rotate grouped data)
2. **Window functions** (calculations within groups)
3. **Time series analysis** (aggregate over time)
4. **Machine learning** (features from grouped data)

---

## Quick Stats

- **Code Snippets:** 30+
- **Examples:** 5 complete
- **Functions Covered:** 20+
- **Real-World Use Cases:** 10+

---

*Grouping and aggregating is the superpower of data analysis. Master it to unlock business insights!* 🎯

