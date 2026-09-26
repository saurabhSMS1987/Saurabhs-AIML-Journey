# Python Topic of the Day #4: Reading and Writing Files with Pandas

**Author:** Saurabh Shirgaokar  
**Date:** Sep 25, 2026  
---

## Overview

Pandas is the **go-to library for data analysis in Python**. It makes reading, writing, and manipulating data incredibly easy.

**Why Learn Pandas for File Operations?**
```
✓ Works with multiple file formats (CSV, Excel, JSON, SQL)
✓ Automatically converts to DataFrames (organized tables)
✓ Built-in data cleaning and transformation
✓ Fast and efficient (handles large files)
✓ Industry standard for data science
```

---

## Part 1: Understanding Pandas DataFrames

### 1.1 What is a DataFrame?

A DataFrame is a **table with rows and columns** - like Excel but in Python.

```python
import pandas as pd

# Create a simple DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['NYC', 'LA', 'Chicago']
})

print(df)
# Output:
#      Name  Age     City
# 0   Alice   25      NYC
# 1     Bob   30       LA
# 2 Charlie   35  Chicago
```

**DataFrame Structure:**
```
     Column 1  Column 2  Column 3
Row1    data      data      data
Row2    data      data      data
Row3    data      data      data
```

---

## Part 2: Reading Files with Pandas

### 2.1 Reading CSV Files (Most Common)

```python
import pandas as pd

# Basic read
df = pd.read_csv('students.csv')

print(df)
# Automatically displays as formatted table

print(df.head())      # First 5 rows
print(df.tail())      # Last 5 rows
print(df.info())      # Column types and info
print(df.shape)       # (rows, columns)
```

**With Options:**

```python
# Skip rows
df = pd.read_csv('data.csv', skiprows=1)

# Use specific columns only
df = pd.read_csv('data.csv', usecols=['Name', 'Age'])

# Set column names
df = pd.read_csv('data.csv', names=['Name', 'Age', 'City'])

# Handle missing values
df = pd.read_csv('data.csv', na_values=['NA', 'N/A', ''])

# Set first column as index
df = pd.read_csv('data.csv', index_col=0)

# Read only first 100 rows
df = pd.read_csv('data.csv', nrows=100)
```

---

### 2.2 Reading Excel Files

```python
# Simple read
df = pd.read_excel('data.xlsx')

# Specify sheet name
df = pd.read_excel('data.xlsx', sheet_name='Sales')  # By name
df = pd.read_excel('data.xlsx', sheet_name=0)         # By index

# Read multiple sheets
df1 = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df2 = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# Get all sheet names
sheets = pd.ExcelFile('data.xlsx').sheet_names
print(sheets)  # ['Sheet1', 'Sheet2', 'Sheet3']
```

---

### 2.3 Reading JSON Files

```python
# Simple read
df = pd.read_json('data.json')

# Specify orientation
df = pd.read_json('data.json', orient='records')  # List of objects
df = pd.read_json('data.json', orient='split')    # {index, columns, data}

# Example JSON structure:
# [
#   {"Name": "Alice", "Age": 25},
#   {"Name": "Bob", "Age": 30}
# ]
```

---

### 2.4 Reading from URLs and Databases

```python
# Read from URL
url = 'https://raw.githubusercontent.com/data.csv'
df = pd.read_csv(url)

# Read from SQL database
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM users', conn)
```

---

## Part 3: Writing Files with Pandas

### 3.1 Writing to CSV

```python
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['NYC', 'LA', 'Chicago']
})

# Write to CSV
df.to_csv('output.csv')

# Without index
df.to_csv('output.csv', index=False)

# Specify delimiter (semicolon instead of comma)
df.to_csv('output.csv', sep=';')

# Specify columns order
df.to_csv('output.csv', columns=['Name', 'Age'], index=False)

# Append to existing file
df.to_csv('output.csv', mode='a', header=False)
```

---

### 3.2 Writing to Excel

```python
# Simple write
df.to_excel('output.xlsx', index=False)

# Specify sheet name
df.to_excel('output.xlsx', sheet_name='People', index=False)

# Write multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sales', index=False)
    df2.to_excel(writer, sheet_name='Expenses', index=False)
    df3.to_excel(writer, sheet_name='Summary', index=False)

# With formatting
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
```

---

### 3.3 Writing to JSON

```python
# Simple write
df.to_json('output.json')

# As list of objects (readable)
df.to_json('output.json', orient='records', indent=4)

# Pretty print (human readable)
df.to_json('output.json', indent=4)

# As array format
df.to_json('output.json', orient='split')
```

---

## Part 4: Common Data Operations

### 4.1 Filtering Data

```python
df = pd.read_csv('students.csv')

# Filter rows where Age > 25
young = df[df['Age'] > 25]

# Filter by string
nyc_students = df[df['City'] == 'NYC']

# Multiple conditions
result = df[(df['Age'] > 25) & (df['City'] == 'NYC')]

# Get specific columns
names = df[['Name', 'City']]
```

---

### 4.2 Adding and Modifying Columns

```python
df = pd.read_csv('students.csv')

# Add new column
df['Year'] = 2026

# Calculate new column
df['Age_Next_Year'] = df['Age'] + 1

# Apply function to column
df['Name_Upper'] = df['Name'].str.upper()

# Replace values
df['City'] = df['City'].replace('NYC', 'New York City')
```

---

### 4.3 Handling Missing Values

```python
df = pd.read_csv('data.csv')

# Check for missing values
print(df.isnull())          # Shows True/False
print(df.isnull().sum())    # Count per column

# Drop rows with missing values
df_clean = df.dropna()

# Drop specific column with missing values
df_clean = df.drop(columns=['Age'])

# Fill missing values
df['Age'].fillna(0)                    # Fill with 0
df['Age'].fillna(df['Age'].mean())     # Fill with average
df['Age'].fillna(method='ffill')       # Forward fill
```

---

### 4.4 Sorting and Grouping

```python
df = pd.read_csv('students.csv')

# Sort by column
df_sorted = df.sort_values('Age')           # Ascending
df_sorted = df.sort_values('Age', ascending=False)  # Descending

# Group and aggregate
age_counts = df.groupby('City').size()      # Count by city
avg_age = df.groupby('City')['Age'].mean()  # Average age by city

# Multiple operations
summary = df.groupby('City').agg({
    'Age': ['mean', 'min', 'max'],          # Multiple stats
    'Name': 'count'                          # Count names
})
```

---

## Part 5: Practical Implementation Examples

### Example 1: Read, Process, and Save Student Grades

```python
import pandas as pd

# 1. Read CSV file
df = pd.read_csv('student_grades.csv')

print("Original data:")
print(df.head())

# 2. Process data
# Calculate average grade
df['Average'] = (df['Math'] + df['English'] + df['Science']) / 3

# Add grade letter
def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

df['Grade'] = df['Average'].apply(get_grade)

# Add status
df['Status'] = df['Average'].apply(lambda x: 'Pass' if x >= 60 else 'Fail')

# 3. Save results
df.to_csv('student_grades_processed.csv', index=False)

print("\nProcessed data:")
print(df)

print("\nSummary:")
print(f"Total students: {len(df)}")
print(f"Passed: {(df['Status'] == 'Pass').sum()}")
print(f"Failed: {(df['Status'] == 'Fail').sum()}")
print(f"Average class grade: {df['Average'].mean():.2f}")

# 4. Save to Excel with multiple sheets
with pd.ExcelWriter('student_report.xlsx') as writer:
    df.to_excel(writer, sheet_name='All Students', index=False)
    
    # Top performers
    top = df.nlargest(5, 'Average')
    top.to_excel(writer, sheet_name='Top Performers', index=False)
    
    # Students needing help
    struggling = df[df['Status'] == 'Fail'].sort_values('Average')
    struggling.to_excel(writer, sheet_name='Needs Help', index=False)
```

---

### Example 2: Combine Multiple CSV Files

```python
import pandas as pd
import os

# Get all CSV files from directory
csv_files = [f for f in os.listdir('data/') if f.endswith('.csv')]

# Read and combine
all_data = []

for file in csv_files:
    df = pd.read_csv(f'data/{file}')
    df['Source_File'] = file  # Track source
    all_data.append(df)

# Combine all
combined = pd.concat(all_data, ignore_index=True)

print(f"Combined {len(csv_files)} files")
print(f"Total rows: {len(combined)}")
print(f"Total columns: {len(combined.columns)}")

# Save combined data
combined.to_csv('combined_data.csv', index=False)

# Save to Excel too
combined.to_excel('combined_data.xlsx', index=False)
```

---

### Example 3: Sales Data Analysis

```python
import pandas as pd

# 1. Read sales data
df = pd.read_csv('sales.csv')

# 2. Data cleaning
df['Date'] = pd.to_datetime(df['Date'])  # Convert to datetime
df['Amount'] = df['Amount'].astype(float)  # Ensure numeric
df = df.dropna()  # Remove missing values

# 3. Analysis
print("=== SALES ANALYSIS ===\n")

# Total sales
total_sales = df['Amount'].sum()
print(f"Total Sales: ${total_sales:,.2f}\n")

# By product
sales_by_product = df.groupby('Product')['Amount'].sum().sort_values(ascending=False)
print("Sales by Product:")
print(sales_by_product)
print()

# By region
sales_by_region = df.groupby('Region')['Amount'].sum().sort_values(ascending=False)
print("Sales by Region:")
print(sales_by_region)
print()

# By month
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Amount'].sum()
print("Monthly Sales:")
print(monthly_sales)
print()

# Top customers
top_customers = df.groupby('Customer')['Amount'].sum().nlargest(5)
print("Top 5 Customers:")
print(top_customers)

# 4. Save results
with pd.ExcelWriter('sales_report.xlsx') as writer:
    # Summary stats
    summary = pd.DataFrame({
        'Metric': ['Total Sales', 'Avg Transaction', 'Max Transaction', 'Min Transaction'],
        'Value': [
            total_sales,
            df['Amount'].mean(),
            df['Amount'].max(),
            df['Amount'].min()
        ]
    })
    summary.to_excel(writer, sheet_name='Summary', index=False)
    
    # By product
    sales_by_product.to_excel(writer, sheet_name='By Product')
    
    # By region
    sales_by_region.to_excel(writer, sheet_name='By Region')
    
    # Full data
    df.to_excel(writer, sheet_name='Raw Data', index=False)
```

---

### Example 4: Data Transformation Pipeline

```python
import pandas as pd

# 1. Read data from multiple sources
customers = pd.read_csv('customers.csv')
orders = pd.read_csv('orders.csv')

print("Customers shape:", customers.shape)
print("Orders shape:", orders.shape)

# 2. Join data
combined = orders.merge(customers, on='CustomerID', how='left')

# 3. Transform
combined['OrderDate'] = pd.to_datetime(combined['OrderDate'])
combined['Month'] = combined['OrderDate'].dt.to_period('M')
combined['TotalWithTax'] = combined['Amount'] * 1.08  # Add 8% tax

# 4. Aggregate
monthly_summary = combined.groupby('Month').agg({
    'OrderID': 'count',
    'Amount': 'sum',
    'TotalWithTax': 'sum'
}).rename(columns={
    'OrderID': 'NumOrders',
    'Amount': 'Revenue',
    'TotalWithTax': 'RevenueWithTax'
})

print("\nMonthly Summary:")
print(monthly_summary)

# 5. Save results
combined.to_csv('combined_data.csv', index=False)
monthly_summary.to_csv('monthly_summary.csv')
combined.to_excel('combined_report.xlsx', index=False)

print("\nFiles saved!")
```

---

### Example 5: Filtering and Export by Category

```python
import pandas as pd

# 1. Read all products
df = pd.read_csv('products.csv')

print(f"Total products: {len(df)}\n")

# 2. Create separate files by category
categories = df['Category'].unique()

with pd.ExcelWriter('products_by_category.xlsx') as writer:
    # All products in first sheet
    df.to_excel(writer, sheet_name='All Products', index=False)
    
    # Separate sheet per category
    for category in categories:
        category_data = df[df['Category'] == category].sort_values('Price', ascending=False)
        
        # Sheet name (truncate if too long)
        sheet_name = category[:31]  # Excel sheet name limit
        
        category_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"{category}: {len(category_data)} products")

print("\nFile saved: products_by_category.xlsx")
```

---

## Part 6: Best Practices

### ✅ Good Practices

```python
# 1. Always specify index=False when writing (unless needed)
df.to_csv('output.csv', index=False)

# 2. Handle missing values explicitly
df = df.dropna()  # or fillna()

# 3. Use meaningful column names
df.columns = ['Customer_Name', 'Purchase_Date', 'Amount']

# 4. Check data types
print(df.dtypes)

# 5. Validate after operations
print(df.shape)
print(df.head())

# 6. Use encoding for non-ASCII characters
df.to_csv('output.csv', encoding='utf-8')
```

---

### ❌ Common Mistakes

```python
# ❌ Not checking for missing values
df = pd.read_csv('data.csv')
result = df['Age'].mean()  # May give wrong result if NaN present

# ✅ Check first
df.dropna(subset=['Age'])
result = df['Age'].mean()

# ❌ Forgetting column selection creates full copy
new_df = df  # This is reference, not copy!
new_df['Age'] = 0  # Modifies original df!

# ✅ Use copy()
new_df = df.copy()
new_df['Age'] = 0  # Only modifies new_df

# ❌ Not converting data types
df['Date'] = df['Date']  # Still string, not datetime

# ✅ Convert explicitly
df['Date'] = pd.to_datetime(df['Date'])
```

---

## Part 7: Quick Reference Cheatsheet

### Reading Files

```python
# CSV
df = pd.read_csv('file.csv')

# Excel
df = pd.read_excel('file.xlsx')

# JSON
df = pd.read_json('file.json')

# SQL
df = pd.read_sql('SELECT * FROM table', connection)
```

### Writing Files

```python
# CSV
df.to_csv('output.csv', index=False)

# Excel
df.to_excel('output.xlsx', index=False)

# JSON
df.to_json('output.json', orient='records', indent=4)

# SQL
df.to_sql('table_name', connection)
```

### Common Operations

```python
# Basic info
df.head()           # First 5 rows
df.info()           # Column types
df.describe()       # Statistics
df.shape            # (rows, columns)

# Filtering
df[df['Age'] > 25]  # Filter rows
df[['Name', 'Age']] # Select columns
df.loc[0]           # By index
df.iloc[0]          # By position

# Modifications
df['New'] = value        # Add column
df = df.drop(columns=['Age'])  # Remove column
df = df.sort_values('Age')     # Sort
df.groupby('City').sum()       # Group and aggregate
```

---

## Part 8: Practice Exercises

### Exercise 1: Read and Summarize

```python
# Given: 'employees.csv' with columns: Name, Department, Salary
# TODO:
# 1. Read the CSV
# 2. Group by Department
# 3. Calculate average salary per department
# 4. Save to 'department_summary.csv'
```

---

### Exercise 2: Filter and Export

```python
# Given: 'products.csv' with columns: ProductName, Category, Price
# TODO:
# 1. Read CSV
# 2. Filter products over $100
# 3. Sort by price (descending)
# 4. Save to 'expensive_products.xlsx'
```

---

### Exercise 3: Combine and Process

```python
# Given: Multiple CSV files in 'data/' folder
# TODO:
# 1. Read all CSV files
# 2. Combine them
# 3. Remove duplicates
# 4. Save to 'combined_unique.csv'
```

---

*Pandas is the superpower of data work. Master it, and you can tackle any data challenge!* 🚀
