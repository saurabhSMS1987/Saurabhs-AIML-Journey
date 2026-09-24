# Python Topic of the Day #3: Reading and Writing Files

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Level:** Beginner  
**Audience:** New learners wanting to understand Python basics

---

## Overview

Working with files is one of the most practical skills in Python. Whether you're reading data, saving results, or processing documents, **file operations** are essential.

**Why Learn This?**
```
✓ Read data from files (CSV, TXT, JSON)
✓ Write results to files
✓ Process large datasets
✓ Save program output
✓ Work with real-world data
✓ Essential for data science and automation
```

---

## Part 1: Understanding File Operations

### 1.1 What is a File?

A file is stored data on your computer.

```
Examples:
- documents.txt (text file)
- data.csv (comma-separated values)
- config.json (structured data)
- image.png (binary file)
- script.py (Python code)
```

### 1.2 File Operations

Three main operations:

```
READ   → Load data from file into Python
WRITE  → Save data from Python to file
APPEND → Add data to end of file
```

---

## Part 2: Basic File Reading

### 2.1 Simple Read - Read Entire File

```python
# Open and read entire file
file = open('document.txt', 'r')  # 'r' = read mode
content = file.read()             # Read all content
file.close()                       # Close file

print(content)
# Output: All text from file
```

**Important:** Always close files when done!

---

### 2.2 Reading Line by Line

```python
# Read file line by line
file = open('document.txt', 'r')

for line in file:
    print(line)  # Each line is printed

file.close()

# Better: Read into a list
file = open('document.txt', 'r')
lines = file.readlines()  # Returns list of lines
file.close()

print(lines)
# Output: ['Line 1\n', 'Line 2\n', 'Line 3\n']
```

---

### 2.3 Reading Specific Number of Lines

```python
# Read specific number of characters
file = open('document.txt', 'r')

first_100_chars = file.read(100)  # Read first 100 characters
file.close()

print(first_100_chars)
```

---

## Part 3: Basic File Writing

### 3.1 Write to File (Replace Contents)

```python
# Open file in write mode
file = open('output.txt', 'w')  # 'w' = write mode (overwrites!)

file.write("Hello, World!")
file.write("\nSecond line")

file.close()

# File now contains:
# Hello, World!
# Second line
```

**Warning:** 'w' mode **overwrites** entire file!

---

### 3.2 Append to File (Add to End)

```python
# Open file in append mode
file = open('output.txt', 'a')  # 'a' = append mode

file.write("\nNew line added at end")

file.close()

# Original content + new line
```

**Difference:**
```
'w' mode: Replace entire file
'a' mode: Add to end of file
```

---

### 3.3 Writing Multiple Lines

```python
# Write multiple lines
file = open('data.txt', 'w')

lines = [
    "Alice 25\n",
    "Bob 30\n",
    "Charlie 35\n"
]

file.writelines(lines)  # Write multiple lines at once
file.close()

# File now contains:
# Alice 25
# Bob 30
# Charlie 35
```

---

## Part 4: The "with" Statement - Best Practice

### 4.1 Why Use "with"?

```python
# Problem: Must remember to close file
file = open('data.txt', 'r')
content = file.read()
file.close()  # Easy to forget!

# Solution: Use "with" - automatically closes
with open('data.txt', 'r') as file:
    content = file.read()
# File automatically closed!
```

**Benefits:**
```
✓ Automatically closes file
✓ Handles errors gracefully
✓ Cleaner code
✓ No risk of file leaks
```

---

### 4.2 Reading with "with"

```python
# Read entire file
with open('document.txt', 'r') as file:
    content = file.read()
    print(content)

# Read line by line
with open('document.txt', 'r') as file:
    for line in file:
        print(line.strip())  # strip() removes newline

# Read into list
with open('document.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line)
```

---

### 4.3 Writing with "with"

```python
# Write to file (safe)
with open('output.txt', 'w') as file:
    file.write("Line 1\n")
    file.write("Line 2\n")
    file.write("Line 3\n")

# Append to file (safe)
with open('output.txt', 'a') as file:
    file.write("Line 4 appended\n")
```

---

## Part 5: File Modes Reference

### 5.1 All File Modes

| Mode | Name | What it does | Use When |
|------|------|--------------|----------|
| `'r'` | Read | Open for reading | Want to read existing file |
| `'w'` | Write | Create/overwrite file | Want to create new file |
| `'a'` | Append | Add to end of file | Want to add to existing file |
| `'x'` | Exclusive | Create only if doesn't exist | Want to create, fail if exists |
| `'r+'` | Read+Write | Read and modify | Need both operations |

---

### 5.2 Text vs. Binary

```python
# Text mode (default)
with open('file.txt', 'r') as file:   # Text file
    content = file.read()

# Binary mode (for images, videos, etc.)
with open('image.jpg', 'rb') as file:  # 'b' for binary
    data = file.read()
```

---

## Part 6: Working with CSV Files

### 6.1 Reading CSV Files

```python
# Simple CSV reading (manual)
with open('students.csv', 'r') as file:
    lines = file.readlines()
    
for line in lines:
    parts = line.strip().split(',')  # Split by comma
    name, age, grade = parts
    print(f"{name} is {age} years old")

# Output:
# Alice is 25 years old
# Bob is 30 years old
```

---

### 6.2 Reading CSV with CSV Module

```python
import csv

# Better way: Use csv module
with open('students.csv', 'r') as file:
    reader = csv.reader(file)
    
    for row in reader:
        name, age, grade = row
        print(f"{name}: {age} years old, Grade {grade}")
```

---

### 6.3 Writing CSV Files

```python
import csv

# Write CSV file
data = [
    ['Name', 'Age', 'Grade'],
    ['Alice', '25', 'A'],
    ['Bob', '30', 'B'],
    ['Charlie', '35', 'A']
]

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)  # Write all rows

# Result: properly formatted CSV file
```

---

### 6.4 Working with Dictionaries (DictReader/DictWriter)

```python
import csv

# Read CSV as dictionaries (column-based)
with open('students.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        print(f"{row['Name']} - Grade: {row['Grade']}")

# Write using dictionaries
with open('output.csv', 'w', newline='') as file:
    fieldnames = ['Name', 'Age', 'Grade']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()  # Write column names
    writer.writerow({'Name': 'Alice', 'Age': '25', 'Grade': 'A'})
    writer.writerow({'Name': 'Bob', 'Age': '30', 'Grade': 'B'})
```

---

## Part 7: Working with JSON Files

### 7.1 Reading JSON Files

```python
import json

# Read JSON file
with open('config.json', 'r') as file:
    data = json.load(file)  # Load as Python dictionary

print(data)
# Output: {'name': 'Alice', 'age': 25, 'city': 'NYC'}

print(data['name'])  # Access like dictionary
# Output: Alice
```

---

### 7.2 Writing JSON Files

```python
import json

# Python dictionary to save
config = {
    'name': 'Alice',
    'age': 25,
    'city': 'NYC',
    'skills': ['Python', 'Data Analysis', 'SQL']
}

# Write to JSON file
with open('config.json', 'w') as file:
    json.dump(config, file, indent=4)  # indent for readability

# File now contains properly formatted JSON
```

---

### 7.3 JSON Reading/Writing Example

```python
import json

# Read
with open('students.json', 'r') as file:
    students = json.load(file)

# Modify
students.append({'name': 'Diana', 'age': 28})

# Write back
with open('students.json', 'w') as file:
    json.dump(students, file, indent=4)
```

---

## Part 8: Error Handling

### 8.1 Handling File Not Found

```python
# Without error handling - will crash
file = open('nonexistent.txt', 'r')  # FileNotFoundError!

# With error handling
try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found! Check the path.")

# Program continues without crashing
```

---

### 8.2 Handling Permission Errors

```python
try:
    with open('protected.txt', 'r') as file:
        content = file.read()
except PermissionError:
    print("You don't have permission to read this file.")
except FileNotFoundError:
    print("File not found.")
```

---

### 8.3 Comprehensive Error Handling

```python
def read_file_safely(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    
    except PermissionError:
        print(f"Error: No permission to read {filename}.")
        return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

content = read_file_safely('data.txt')
if content:
    print("File read successfully!")
```

---

## Part 9: Practical Implementation Examples

### Example 1: Read CSV, Process Data, Save Results

```python
import csv

# Read student grades from CSV
students_data = []

with open('grades.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row['Name']
        math = int(row['Math'])
        english = int(row['English'])
        average = (math + english) / 2
        
        students_data.append({
            'Name': name,
            'Math': math,
            'English': english,
            'Average': round(average, 2),
            'Status': 'Pass' if average >= 60 else 'Fail'
        })

# Write results to new file
with open('grades_results.csv', 'w', newline='') as file:
    fieldnames = ['Name', 'Math', 'English', 'Average', 'Status']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(students_data)

print("Results saved to grades_results.csv")
```

---

### Example 2: Read Text File, Convert to JSON

```python
import json

# Read names from text file (one name per line)
names = []

with open('names.txt', 'r') as file:
    for line in file:
        name = line.strip()  # Remove whitespace
        if name:  # Only if not empty
            names.append(name)

# Convert to JSON and save
data = {
    'names': names,
    'count': len(names),
    'imported_from': 'names.txt'
}

with open('names.json', 'w') as file:
    json.dump(data, file, indent=4)

print(f"Imported {len(names)} names to JSON")
```

---

### Example 3: Combine Multiple Files

```python
# Read data from multiple files and combine

all_data = []

files = ['data_2023.csv', 'data_2024.csv', 'data_2025.csv']

for filename in files:
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            all_data.extend(lines)  # Add to combined list
            print(f"Read {len(lines)} lines from {filename}")
    
    except FileNotFoundError:
        print(f"Skipping {filename} - not found")

# Write combined data to new file
with open('all_data_combined.txt', 'w') as file:
    file.writelines(all_data)

print(f"Combined {len(all_data)} total lines")
```

---

### Example 4: File Log System

```python
import json
from datetime import datetime

# Simple logging to file
def log_action(action, status, details=""):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'status': status,
        'details': details
    }
    
    # Append to log file
    with open('app_log.json', 'a') as file:
        json.dump(log_entry, file)
        file.write('\n')  # New line for readability

# Usage
log_action('user_login', 'success', 'User: alice@example.com')
log_action('file_upload', 'success', 'File: report.pdf')
log_action('error', 'failed', 'Database connection timeout')

# View logs
with open('app_log.json', 'r') as file:
    for line in file:
        if line.strip():
            log = json.loads(line)
            print(f"[{log['timestamp']}] {log['action']}: {log['status']}")
```

---

### Example 5: Data Processing Pipeline

```python
import csv
import json

# 1. Read data from CSV
print("Step 1: Reading CSV...")
raw_data = []

with open('raw_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        raw_data.append(row)

# 2. Process data
print("Step 2: Processing data...")
processed_data = []

for row in raw_data:
    # Clean and transform
    processed_row = {
        'id': int(row['ID']),
        'name': row['Name'].upper(),
        'value': float(row['Value']),
        'valid': row['Status'] == 'Active'
    }
    processed_data.append(processed_row)

# 3. Filter data
print("Step 3: Filtering data...")
valid_data = [x for x in processed_data if x['valid']]

# 4. Save results
print("Step 4: Saving results...")
with open('processed_results.json', 'w') as file:
    json.dump(valid_data, file, indent=4)

print(f"Complete! Processed {len(raw_data)} rows, kept {len(valid_data)}")
```

---

## Part 10: Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting to Close Files

```python
# Wrong - file not closed
file = open('data.txt', 'r')
content = file.read()
# Forgot to close!

# Right - use with statement
with open('data.txt', 'r') as file:
    content = file.read()
# Auto-closed!
```

---

### ❌ Mistake 2: Using 'w' Instead of 'a'

```python
# Wrong - overwrites entire file!
with open('data.txt', 'w') as file:
    file.write("New data")
# Old data lost!

# Right - append to keep old data
with open('data.txt', 'a') as file:
    file.write("New data")
# Old data preserved!
```

---

### ❌ Mistake 3: Not Handling Errors

```python
# Wrong - crashes if file not found
with open('maybe_exists.txt', 'r') as file:
    content = file.read()

# Right - handle the error
try:
    with open('maybe_exists.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found")
```

---

### ❌ Mistake 4: Not Stripping Whitespace

```python
# Wrong - newlines included
with open('names.txt', 'r') as file:
    for line in file:
        print(line)  # Has \n at end

# Right - remove whitespace
with open('names.txt', 'r') as file:
    for line in file:
        print(line.strip())  # Clean line
```

---

## Part 11: Quick Reference

### Read Patterns

```python
# Read entire file
with open('file.txt', 'r') as file:
    content = file.read()

# Read line by line
with open('file.txt', 'r') as file:
    for line in file:
        process(line)

# Read into list
with open('file.txt', 'r') as file:
    lines = file.readlines()

# Read CSV
import csv
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        process(row)

# Read JSON
import json
with open('data.json', 'r') as file:
    data = json.load(file)
```

### Write Patterns

```python
# Write to file
with open('file.txt', 'w') as file:
    file.write("content")

# Append to file
with open('file.txt', 'a') as file:
    file.write("more content")

# Write CSV
import csv
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Col1', 'Col2'])
    writer.writerow(['Val1', 'Val2'])

# Write JSON
import json
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
```

---

## Part 12: Practice Exercises

### Exercise 1: Read and Count Lines
```python
# Given: file 'text.txt'
# TODO: 
# 1. Read the file
# 2. Count total lines
# 3. Print count

# Solution:
with open('text.txt', 'r') as file:
    lines = file.readlines()
    print(f"Total lines: {len(lines)}")
```

---

### Exercise 2: Filter and Save
```python
# Given: CSV file with numbers
# TODO:
# 1. Read CSV
# 2. Keep only numbers > 50
# 3. Save to new file

# Hint: Use csv module and filtering
```

---

### Exercise 3: JSON Processing
```python
# Given: JSON file with students
# TODO:
# 1. Read JSON
# 2. Add new field 'graduated': True/False
# 3. Save modified JSON
```

---

*File operations are fundamental to real-world Python work. Master them, and you can work with any data!* 🚀
