<div align="center">

# 🐍 Python Interview Questions: A Practical Guide

**32 commonly asked Python interview questions with clear answers, runnable code and interview tips**

`Beginner` · `Intermediate` · `Advanced`

*7 Nov 2026 · Compiled by Saurabh S*

</div>

> [!NOTE]
> **Source:** The questions and core answers come from **CodeBasics** (*Python Interview Questions Solution*, [codebasics.io](https://codebasics.io)). I've added extra context, corrections for newer Python versions, interview tips and runnable examples, all marked as additions where they go beyond the original. Every code example was run on Python 3.12.

---

## 📋 How to use this guide

1. **Skim the [quick-reference table](#-quick-reference)** to find the topics you're least comfortable with.
2. **Read each answer out loud** in your own words. Interviewers want understanding, not memorised text.
3. **Run the code.** Changing an example and predicting the output is the fastest way to learn.
4. **Look for the 💡 tips.** They cover the follow-up questions interviewers like to ask next.

## 🧭 Quick reference

| # | Level | Topic | Key idea in one line |
| --- | --- | --- | --- |
| B1 | 🟢 Beginner | [Choosing a data type](#b1-storing-products-and-prices) | Key–value pairs → `dict` |
| B2 | 🟢 Beginner | [Benefits of Python](#b2-main-benefits-of-python) | Readable, versatile, huge ecosystem |
| B3 | 🟢 Beginner | [String slicing](#b3-string-slicing-output) | `s[:i] + s[i:] == s` |
| B4 | 🟢 Beginner | [`enumerate()`](#b4-looping-with-positions-enumerate) | Index and value without a counter |
| B5 | 🟢 Beginner | [Handling bad input](#b5-handling-invalid-user-input) | `try` / `except ValueError` |
| B6 | 🟢 Beginner | [`append()` vs `extend()`](#b6-append-vs-extend) | One item vs many items |
| B7 | 🟢 Beginner | [Modules](#b7-what-is-a-module) | A `.py` file you can import |
| B8 | 🟢 Beginner | [`//` floor division](#b8-the--operator) | Rounds **down**, even for negatives |
| B9 | 🟢 Beginner | [`zip()`](#b9-the-zip-function) | Pairs items from several iterables |
| B10 | 🟢 Beginner | [Creating a class](#b10-creating-a-class) | `class` + `__init__` + object |
| B11 | 🟢 Beginner | [`__init__` and `self`](#b11-__init__-and-self) | Constructor and the current object |
| B12 | 🟢 Beginner | [File handling](#b12-file-handling-and-file-modes) | `open()` modes and `with` |
| I1 | 🟡 Intermediate | [Source code encoding](#i1-source-code-encoding) | UTF-8 by default |
| I2 | 🟡 Intermediate | [PEP 8](#i2-pep-8) | The official style guide |
| I3 | 🟡 Intermediate | [Memory management](#i3-memory-management) | Private heap, reference counting, GC |
| I4 | 🟡 Intermediate | [MySQL from Python](#i4-reading-data-from-mysql) | Connect → cursor → execute → fetch → close |
| I5 | 🟡 Intermediate | [Programming paradigms](#i5-object-oriented-or-functional) | Python is multi-paradigm |
| I6 | 🟡 Intermediate | [Magic (dunder) methods](#i6-magic-dunder-methods) | `__init__`, `__str__`, `__len__`… |
| I7 | 🟡 Intermediate | [Lambda expressions](#i7-lambda-expressions) | Small one-line anonymous functions |
| I8 | 🟡 Intermediate | [Inheritance and overriding](#i8-inheritance-and-method-overriding) | Child classes reuse and redefine |
| I9 | 🟡 Intermediate | [`super()`](#i9-the-super-function) | Call the parent's methods |
| I10 | 🟡 Intermediate | [String immutability](#i10-string-immutability) | Every "change" makes a new string |
| A1 | 🔴 Advanced | [Sorting with a lambda key](#a1-sorting-with-a-lambda-key) | `sorted(..., key=..., reverse=True)` |
| A2 | 🔴 Advanced | [Metaclasses](#a2-metaclasses) | Classes that create classes |
| A3 | 🔴 Advanced | [The GIL](#a3-the-global-interpreter-lock-gil) | One thread runs Python bytecode at a time |
| A4 | 🔴 Advanced | [Debugging techniques](#a4-debugging-techniques) | print, pdb, IDEs, logging, tests |
| A5 | 🔴 Advanced | [Packaging a project](#a5-turning-a-project-into-a-package) | `pyproject.toml` and a build |
| A6 | 🔴 Advanced | [Decorators for logging and retry](#a6-decorators-for-logging-and-retries) | Add behaviour without editing code |
| A7 | 🔴 Advanced | [List comprehension vs loops](#a7-list-comprehensions-vs-loops) | Concise filtering and transforming |
| A8 | 🔴 Advanced | [Generators for big data](#a8-generators-for-large-datasets) | One record in memory at a time |
| A9 | 🔴 Advanced | [Abstract classes](#a9-abstract-classes-for-a-payment-system) | Enforce a common interface |
| A10 | 🔴 Advanced | [SOLID principles](#a10-solid-principles) | Five rules for maintainable OOP |

---

# 🟢 Beginner

### B1. Storing products and prices

> **Q:** If you have data with names of products and their prices, which Python data type will you use to store it and why?

**A dictionary (`dict`).** The product name is the **key** and the price is the **value**.

```python
product_prices = {
    "Laptop": 55000,
    "Headphones": 1500,
    "Monitor": 8000,
}
print(product_prices["Monitor"])        # 8000: direct lookup by name
product_prices["Monitor"] = 7500        # update in place
```

Dictionaries look up a value by its key in roughly **constant time**, however many items there are, so they're ideal for key–value data.

> [!TIP]
> A common follow-up: *"What if two products have the same name?"* Dictionary keys must be unique, so a second entry overwrites the first. If duplicates are possible, use a list of tuples or a pandas DataFrame instead.

### B2. Main benefits of Python

> **Q:** What are the main benefits of Python?

| Benefit | What it means |
| --- | --- |
| **Clean, English-like syntax** | Easy to read and write. Indentation defines code blocks, instead of `{}` braces and `;` semicolons. |
| **Multi-paradigm** | Supports object-oriented, functional, procedural and imperative styles (see [I5](#i5-object-oriented-or-functional)). |
| **"Batteries included"** | A large standard library, plus **hundreds of thousands** of third-party packages on PyPI for web, data, ML, automation and more. |
| **Dynamic and interpreted** | No need to declare variable types, and code runs without a separate compile step, which makes testing and scripting quick. |
| **Leader in data science and AI** | NumPy, pandas, scikit-learn, TensorFlow and PyTorch are all Python-first. |
| **Cross-platform** | The same code runs on Windows, macOS and Linux. |
| **Strong community** | Extensive documentation, tutorials and open-source contributions. |

> [!TIP]
> Be ready to name a **trade-off**, too: Python is usually slower than compiled languages like C++ or Java for CPU-heavy work, which is why performance-critical libraries such as NumPy do their heavy lifting in C.

### B3. String slicing output

> **Q:** What is the output of `name = 'Codebasics'` followed by `print(name[:4] + name[4:])`?

**Output: `Codebasics`**

- `name[:4]` takes characters at positions 0–3 → `'Code'` (the end position is **excluded**).
- `name[4:]` takes everything from position 4 to the end → `'basics'`.
- Joining the two halves rebuilds the original string.

```python
name = "Codebasics"
print(name[:4], "+", name[4:])     # Code + basics
print(name[:4] + name[4:])         # Codebasics
```

> [!TIP]
> This works for **any** split point: `s[:i] + s[i:] == s` is always `True`. Interviewers may also ask about negative indices: `name[-6:]` is `'basics'`.

### B4. Looping with positions: `enumerate()`

> **Q:** How do you print each company with its position (e.g. "0 Meta") without a separate counter variable?

**Use `enumerate()`**, which returns the position and the item together:

```python
companies = ["Meta", "Amazon", "Apple", "Netflix", "Google"]
for i, company in enumerate(companies):
    print(i, company)
# 0 Meta / 1 Amazon / 2 Apple / 3 Netflix / 4 Google
```

> [!TIP]
> Mention the `start` argument: `enumerate(companies, start=1)` numbers from 1, which is handy for human-friendly rankings.

### B5. Handling invalid user input

> **Q:** A user types "twenty" instead of a number. How do you show "Please enter a valid number!" instead of crashing?

**Catch the `ValueError`** that `int()` raises when text can't be converted:

```python
try:
    age = int(input("Enter your age: "))
    print("You are", age, "years old.")
except ValueError:
    print("Please enter a valid number!")
```

> [!TIP]
> A strong answer adds a **retry loop**, so the user can try again:
> ```python
> while True:
>     try:
>         age = int(input("Enter your age: "))
>         break
>     except ValueError:
>         print("Please enter a valid number!")
> ```

### B6. `append()` vs `extend()`

> **Q:** You have existing data and new items. When do you use `append()` and when `extend()`?

- **`append()`** adds its argument as **one single element**, even if that argument is a list.
- **`extend()`** adds **each item** from another iterable individually.

```python
b = [3, 4]

a1 = [1, 2]
a1.append(b)
print(a1)          # [1, 2, [3, 4]]: the whole list becomes one element

a2 = [1, 2]
a2.extend(b)
print(a2)          # [1, 2, 3, 4]
```

> [!TIP]
> `a2 += b` does the same as `extend()`. For combining lists without changing either one, use `a + b`.

### B7. What is a module?

> **Q:** What is a module in Python?

A **module** is a `.py` file containing Python code: functions, classes, variables, or code to run. Modules split programs into manageable, reusable parts, and you use one by **importing** it.

```python
# mymodule.py
def greet():
    return "Hello from the module!"

# main.py
import mymodule
print(mymodule.greet())     # Hello from the module!
```

> [!TIP]
> Related terms interviewers like: a **package** is a folder of modules (usually with an `__init__.py` file), and a **library** is a collection of packages. You can also import selectively: `from mymodule import greet`.

### B8. The `//` operator

> **Q:** What is the use of the `//` operator?

`//` is **floor division**: it divides and returns the **largest whole number less than or equal to** the result. It always rounds **down**.

| Expression | True division | Floor division | Why |
| --- | --- | --- | --- |
| `7 // 3` | 2.33 | **2** | The largest whole number ≤ 2.33 |
| `-7 // 3` | −2.33 | **−3** | The largest whole number ≤ −2.33 (rounding *down* goes more negative) |

```python
print(7 // 3, -7 // 3, 7 % 3)      # 2 -3 1
print(int(-7 / 3))                 # -2: int() truncates towards zero, which is different!
```

> [!IMPORTANT]
> For negative numbers, `//` is **not** the same as dropping the decimal. `-7 // 3` is `-3`, while truncating gives `-2`. This is a favourite trick question.

### B9. The `zip()` function

> **Q:** What is the use of `zip()`? Explain with an example.

`zip()` pairs up items from two or more iterables **by position** and returns an iterator of tuples:

```python
list_1 = ["a", "b", "c"]
list_2 = ["1", "2", "3"]

for a, b in zip(list_1, list_2):
    print(a, b)                       # a 1 / b 2 / c 3

print(list(zip(list_1, list_2)))      # [('a', '1'), ('b', '2'), ('c', '3')]
print(list(zip([1, 2, 3], ["x"])))    # [(1, 'x')]: stops at the shortest iterable
```

> [!TIP]
> Since Python 3.10, `zip(..., strict=True)` raises an error when lengths differ, which prevents silently losing data. `dict(zip(keys, values))` is a quick way to build a dictionary.

### B10. Creating a class

> **Q:** Create a class `Book` and an object for "Harry Potter" by "J.K. Rowling".

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

book1 = Book("Harry Potter", "J.K. Rowling")
print(book1.title, "-", book1.author)       # Harry Potter - J.K. Rowling
```

The **class** is the blueprint, and `book1` is an **object** (an instance) built from it.

### B11. `__init__` and `self`

> **Q:** What is the role of `__init__()`? How does `self` work, and why is it important?

- **`__init__()`** runs **automatically** when a new object is created. It's commonly called the **constructor**, and it sets up the object's starting data.
- **`self`** refers to **the current object**. It's how a method reaches that object's own attributes and other methods.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner          # stored on *this* object
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount      # changes *this* object's balance only
        return self.balance

a, b = Account("Ravi"), Account("Mira", 100)
a.deposit(50)
print(a.balance, b.balance)         # 50 100: each object keeps its own data
```

> [!TIP]
> Precise detail: strictly, `__new__` creates the object and `__init__` **initialises** it. `self` isn't a keyword, just a strong convention for the first parameter, which Python fills in automatically.

### B12. File handling and file modes

> **Q:** How is file handling done in Python? Describe the file modes and how they affect operations.

Files are opened with the built-in `open(filename, mode)`:

| Mode | Meaning | If the file doesn't exist | If it exists |
| --- | --- | --- | --- |
| `'r'` | Read (default) | Error | Read from the start |
| `'w'` | Write | Created | **Contents erased** |
| `'a'` | Append | Created | Writes added at the end |
| `'x'` | Exclusive create | Created | Error |
| `'b'` | Binary, combined with others (`'rb'`, `'wb'`) | n/a | For images, PDFs and so on |
| `'+'` | Read and write, combined with others (`'r+'`) | n/a | n/a |

```python
with open("output.txt", "w") as file:       # create or overwrite
    file.write("This is a test message.")

with open("output.txt", "r") as file:       # read it back
    print(file.read())                      # This is a test message.
```

**Why use `with`?** It closes the file automatically when the block ends, **even if an error occurs**, which prevents resource leaks and keeps code clean.

> [!TIP]
> Add `encoding="utf-8"` when reading or writing text, so files behave the same on every operating system.

---

# 🟡 Intermediate

### I1. Source code encoding

> **Q:** How do you specify source code encoding in a Python file?

Python 3 source files are **UTF-8 by default**. To use a different encoding, add a special comment on the **first or second line** of the file (after any `#!` line):

```python
# -*- coding: <encoding-name> -*-
```

> [!NOTE]
> *Added context:* this is defined in **PEP 263**. In modern Python 3 it's rarely needed. Simply saving files as UTF-8 is the standard practice.

### I2. PEP 8

> **Q:** What is the use of PEP 8?

**PEP 8** is the official **style guide** for Python code. It covers indentation (4 spaces), line length, naming, imports, whitespace and more. Its goal is **consistency and readability**, so that code written by different people looks familiar and is easier to maintain.

| Element | PEP 8 convention | Example |
| --- | --- | --- |
| Variables and functions | `lowercase_with_underscores` | `total_amount`, `calculate_tax()` |
| Classes | `CapWords` | `JournalEntry` |
| Constants | `ALL_CAPS` | `MAX_RETRIES` |
| Indentation | 4 spaces | |

> [!TIP]
> Mention the tools that enforce it automatically: linters like **flake8** or **ruff**, and formatters like **black**.

### I3. Memory management

> **Q:** How does memory management work in Python?

- Python stores all objects in a **private heap**, managed internally by the **Python memory manager**. You never allocate or free memory by hand.
- In **CPython** (the standard Python), the memory manager handles allocating, caching and reusing memory blocks. A specialised allocator (`pymalloc`) is used for small objects.
- Memory is reclaimed automatically, mainly by **reference counting**: when nothing refers to an object any more, its memory is freed.
- A separate **cyclic garbage collector** (the `gc` module) cleans up groups of objects that refer to each other, which reference counting alone can't free.

```python
import sys
data = []
alias = data
print(sys.getrefcount(data) - 1)    # 2: `data` and `alias` both point to the list
```

> [!NOTE]
> *Added context:* the original answer mentions only reference counting. The cyclic garbage collector is worth naming in an interview, as it's a common follow-up.

### I4. Reading data from MySQL

> **Q:** How can you retrieve data from a MySQL database using Python? Explain the steps.

Using the `mysql.connector` module (`pip install mysql-connector-python`):

```python
import os
import mysql.connector

conn = mysql.connector.connect(                 # 1. connect
    host="localhost",
    user=os.environ["DB_USER"],                 #    keep credentials out of code
    password=os.environ["DB_PASSWORD"],
    database="your_database",
)
cursor = conn.cursor()                          # 2. create a cursor
cursor.execute("SELECT * FROM your_table WHERE id = %s", (42,))   # 3. run a parameterised query
results = cursor.fetchall()                     # 4. fetch: fetchone() for a single row
for row in results:
    print(row)
cursor.close()                                  # 5. always close
conn.close()
```

| Function | Purpose |
| --- | --- |
| `connect()` | Opens the connection |
| `cursor()` | Creates an object that sends SQL and holds results |
| `execute()` | Runs a query |
| `fetchall()` / `fetchone()` / `fetchmany(n)` | Retrieves all rows, one row, or *n* rows |
| `commit()` | Saves changes after `INSERT`, `UPDATE` or `DELETE` |
| `close()` | Releases the cursor and connection |

> [!IMPORTANT]
> *Added context:* always pass values as **parameters** (`%s` plus a tuple), never by building the SQL text with f-strings. That's what prevents **SQL injection**, and interviewers often check for it.

### I5. Object-oriented or functional?

> **Q:** Is Python an object-oriented or functional programming language?

**Both, and more.** Python is **multi-paradigm**:

```python
# Object-oriented: classes and objects
class Dog:
    def bark(self):
        return "Woof!"

# Functional: functions as values, map/filter/lambda, avoiding state changes
squared = list(map(lambda x: x ** 2, [1, 2, 3]))      # [1, 4, 9]

# Procedural: step-by-step instructions grouped into functions
def greet(name):
    return f"Hello {name}"

# Imperative: explicit commands that change program state
total = 0
for i in range(5):
    total += i                                         # total is now 10
```

> [!TIP]
> A nuance worth adding: **everything in Python is an object**, even integers and functions, which is why Python is often described as object-oriented at its core.

### I6. Magic (dunder) methods

> **Q:** What are magic functions in Python?

**Magic methods** (or **dunder methods**, from "**d**ouble **under**score") start and end with `__`, like `__init__`, `__str__` and `__len__`. Python calls them **automatically** to support built-in operations.

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"This is {self.name}"

my_dog = Dog("Buddy")
print(my_dog)            # This is Buddy
```

| Method | Called when you… |
| --- | --- |
| `__init__` | Create an object |
| `__str__` | `print()` the object, or call `str()` |
| `__repr__` | Inspect the object in the console |
| `__len__` | Call `len()` |
| `__eq__`, `__lt__` | Compare with `==` or `<` |
| `__add__` | Use `+` |

### I7. Lambda expressions

> **Q:** What is a lambda expression?

A **lambda** is a small, **anonymous** (unnamed) function written in one line: `lambda arguments: expression`. It's useful when a function is needed only briefly, especially inside `map()`, `filter()` or `sorted()`.

```python
square = lambda x: x * x
print(square(5))                                   # 25

nums = [1, 2, 3, 4]
print(list(map(lambda x: x ** 2, nums)))          # [1, 4, 9, 16]
print(list(filter(lambda x: x % 2 == 0, nums)))   # [2, 4]
```

> [!TIP]
> A lambda can contain only **one expression**: no statements and no multiple lines. PEP 8 also advises against assigning a lambda to a name (as in `square = ...`); use `def` for named functions.

### I8. Inheritance and method overriding

> **Q:** What is inheritance and why is it useful? How does method overriding work? Create `Shape` and a `Rectangle` that overrides `area()`.

- **Inheritance** lets a **child** class reuse the attributes and methods of a **parent** class.
- **Overriding** means the child **redefines** a parent method to give it new behaviour.

```python
class Shape:
    def area(self):
        return "Area is undefined"

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):                      # overrides Shape.area
        return self.length * self.width

print(Rectangle(5, 3).area())           # 15
print(Shape().area())                   # Area is undefined
```

### I9. The `super()` function

> **Q:** What is the purpose of `super()`?

`super()` gives access to the **parent class's methods**. It's most often used to call the parent's constructor, so the setup code isn't repeated:

```python
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):
    def __init__(self, name, emp_id):
        super().__init__(name)          # let the parent set `name`
        self.emp_id = emp_id

e = Employee("Ravi", 101)
print(e.name, e.emp_id)                 # Ravi 101
```

> [!TIP]
> With **multiple inheritance**, `super()` follows the **method resolution order (MRO)**, which you can inspect with `Employee.__mro__`.

### I10. String immutability

> **Q:** How does string immutability affect string operations? What are its advantages and disadvantages?

Strings are **immutable**: once created, they can't be changed. Any operation that seems to modify a string actually **returns a new one**.

```python
s = "hello"
# s[0] = "H"                     # TypeError: 'str' object does not support item assignment
t = s.replace("h", "H")
print(s, t)                      # hello Hello: the original is unchanged
```

| Operation | Example | Result |
| --- | --- | --- |
| Concatenation | `"a" + "b"` | A new string `"ab"` |
| Slicing | `"hello"[0:2]` | A new string `"he"` |
| Replacement | `"hi there".replace("hi", "hello")` | A new string `"hello there"` |

| ✅ Advantages | ⚠️ Disadvantages |
| --- | --- |
| **Safe as dictionary keys and set members**, because they're hashable | **Repeated `+=` in a loop** creates many temporary strings |
| **Predictable:** no function can change a string you passed it | **Extra memory** when making many modified copies |

> [!TIP]
> The fix for slow concatenation in loops is `"".join(parts)`, which builds the final string in one step.

---

# 🔴 Advanced

### A1. Sorting with a lambda key

> **Q:** Sort `students = [("Alice", 88), ("Bob", 75), ("Charlie", 95), ("David", 82)]` by score, highest first, using a lambda.

```python
students = [("Alice", 88), ("Bob", 75), ("Charlie", 95), ("David", 82)]
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)
print(sorted_students)     # [('Charlie', 95), ('Alice', 88), ('David', 82), ('Bob', 75)]
```

| Part | Meaning |
| --- | --- |
| `sorted(students, ...)` | Returns a **new** sorted list. The original isn't changed. |
| `key=lambda x: x[1]` | Sort by the second item of each tuple: the score |
| `reverse=True` | Descending order, highest first |

> [!TIP]
> `students.sort(...)` sorts **in place** instead. To break ties by name, use a tuple key: `key=lambda x: (-x[1], x[0])`.

### A2. Metaclasses

> **Q:** What is a metaclass?

A **metaclass** is a **class of a class**. Classes create objects, and metaclasses create classes. Python's default metaclass is `type`:

```python
class Dog:
    pass

print(type(Dog()))     # <class '__main__.Dog'>: an object's type is its class
print(type(Dog))       # <class 'type'>: a class's type is its metaclass
```

> [!NOTE]
> *Added context:* custom metaclasses (`class Meta(type): ...`) let frameworks change how classes are built, for example to register or validate them automatically. They're rarely needed in everyday code. Class decorators or `__init_subclass__` are usually simpler.

### A3. The Global Interpreter Lock (GIL)

> **Q:** What is the GIL, and how does it affect multithreading?

The **GIL** is a lock in **CPython** that lets only **one thread execute Python bytecode at a time**, even on a multi-core machine. It exists mainly to keep memory management (reference counting) safe and simple.

| Task type | Examples | Effect of the GIL | Better choice |
| --- | --- | --- | --- |
| **CPU-bound** | Heavy calculations, image processing | Threads can't run truly in parallel | `multiprocessing` |
| **I/O-bound** | File reading, API calls, database queries | Little impact, because threads release the GIL while waiting | `threading` or `asyncio` |

> [!NOTE]
> *Added context:* Python 3.13 introduced an **optional, experimental "free-threaded" build** that can run without the GIL. The standard build still uses it, so the answer above remains the norm.

### A4. Debugging techniques

> **Q:** What are the different debugging techniques in Python?

| Technique | Best for | Example |
| --- | --- | --- |
| **`print()` statements** | Quick checks in small scripts | `print(f"Dividing {a} by {b}")` |
| **`pdb`**, the built-in debugger | Stepping through code line by line | `breakpoint()`, the modern shortcut for `pdb.set_trace()` |
| **IDE debuggers** (VS Code, PyCharm) | Breakpoints, watched variables, call stacks, stepping visually | Click in the margin to set a breakpoint |
| **Logging** | Production code, with levels and output to files | `logging.debug("Debug message")` |
| **Unit tests** (`unittest`, `pytest`) | Isolating and preventing bugs | `assert square(4) == 16` |
| **Exceptions and tracebacks** | Understanding and handling errors | `except ZeroDivisionError as e: ...` |
| **`assert` statements** | Checking assumptions during development | `assert x > 0, "x must be positive"` |
| **Third-party tools** | Richer debugging and profiling | `ipdb`, `pudb`, `py-spy` |

```python
import unittest

def square(x):
    return x * x

class TestSquare(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(square(4), 16)

# run with: python -m unittest   (or pytest, which also runs unittest-style tests)
```

> [!TIP]
> `assert` statements are **skipped** when Python runs with the `-O` (optimise) flag, so never use them for checks that must always run, such as validating user input.

### A5. Turning a project into a package

> **Q:** A large project has `auth/`, `billing/` and `utils/` folders (each with `__init__.py`), plus `main.py` and `requirements.txt`. How would you make it a distributable package?

**Steps from the original answer:**

- Add the packaging files: `setup.py`, `pyproject.toml`, and `MANIFEST.in` (for non-Python files).
- Add a `README.md` and a `LICENSE`.
- Keep an `__init__.py` in each sub-package (already present).

> [!NOTE]
> *Added context:* in modern Python packaging, **`pyproject.toml` on its own is enough**, and `setup.py` is optional. A minimal version:
>
> ```toml
> [build-system]
> requires = ["setuptools>=61"]
> build-backend = "setuptools.build_meta"
>
> [project]
> name = "my-project"
> version = "0.1.0"
> dependencies = ["requests"]          # move runtime needs from requirements.txt here
> ```
>
> Then build with `python -m build` and publish with `twine upload dist/*`. Placing the code inside a top-level package folder (or a `src/` layout) keeps imports clean, as in `from my_project.billing import invoice`.

### A6. Decorators for logging and retries

> **Q:** How can decorators add access logging and retry logic to functions, without modifying them? What are the advantages, and how does stacking work?

A **decorator** wraps a function with extra behaviour, keeping the business logic clean. This is called **separation of concerns**.

```python
import functools
import time

def log_access(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[log] calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def retry(times=3, delay=0.1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    print(f"[retry] attempt {attempt} failed")
                    if attempt == times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

calls = {"n": 0}

@retry(times=3)
@log_access
def process_payment():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("network blip")
    return "payment processed"

print(process_payment())
# [log] calling process_payment / [retry] attempt 1 failed / ... / payment processed
```

| Technique | Limitation | Decorator advantage |
| --- | --- | --- |
| Manual wrappers | Repetitive and error-prone | Write the logic once, reuse it anywhere |
| Inheritance | Works only with classes, not plain functions | Works on any callable |
| Inline logic | Mixes logging and retries into business code | Keeps code modular and clean |

**Stacking:** decorators are **applied bottom-up**. `@log_access` wraps the function first, and `@retry` wraps the result. When called, they **run top-down**: `retry` runs first and calls the logged function on each attempt, so every retry is logged.

> [!NOTE]
> *Added context:* the original answer says stacked decorators "execute inside-out: first `log_access`, then `retry`". That describes the order they're **applied**. At **call time**, the outermost decorator (`retry`) runs first, as the output above shows.

### A7. List comprehensions vs loops

> **Q:** From a list of `(name, department, salary)` tuples, get the uppercase names of "Tech" employees earning over 75,000, in one list comprehension. What are the trade-offs against loops?

```python
employees = [("Alice", "Tech", 80000), ("Bob", "HR", 50000), ("Charlie", "Tech", 72000),
             ("Diana", "Tech", 88000), ("Eve", "Sales", 60000)]

tech_high_earners = [name.upper() for name, dept, sal in employees if dept == "Tech" and sal > 75000]
print(tech_high_earners)       # ['ALICE', 'DIANA']
```

| Use a **list comprehension** when… | Use a **`for` loop** when… |
| --- | --- |
| The logic is a simple filter plus transform | The logic has several steps or nested conditions |
| You want concise, readable code | You need side effects (printing, logging, writing files) |
| Speed matters: comprehensions are usually a little faster | Readability would suffer from one long line |

> [!TIP]
> For very large data, swap the square brackets for parentheses to get a **generator expression** (see [A8](#a8-generators-for-large-datasets)), which doesn't build the whole list in memory.

### A8. Generators for large datasets

> **Q:** How can generators process a dataset too large to load into memory? Show an example and explain the benefits.

A **generator** produces items **one at a time** with `yield`, pausing between them, so only one record needs to be in memory:

```python
def fetch_records(records):
    for record in records:
        yield record                    # hand back one record, then pause here

def process(r):
    return r * 2

total = 0
for r in fetch_records(range(1_000_000)):
    total += process(r)
print(total)                            # 999999000000
```

**Benefits:**

- **Memory-efficient:** only the current record is held in memory.
- **Faster start-up:** processing begins right away, with no wait for the whole dataset to load.
- **Scalable:** works the same for thousands or millions of records.

> [!TIP]
> In real pipelines, the generator usually reads from a source in chunks, such as `cursor.fetchmany(1000)` from a database or one line of a file at a time. A one-line alternative is a generator expression: `(r for r in records)`.

### A9. Abstract classes for a payment system

> **Q:** How would you use abstract classes to enforce a consistent interface across payment methods? What are the benefits?

Create an **abstract base class** with Python's `abc` module. Each payment type must implement every abstract method:

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def authorize(self, amount): ...
    @abstractmethod
    def pay(self, amount): ...
    @abstractmethod
    def refund(self, amount): ...

class UPIPayment(PaymentMethod):
    def authorize(self, amount): return True
    def pay(self, amount): return f"Paid ₹{amount} via UPI"
    def refund(self, amount): return f"Refunded ₹{amount} via UPI"

class IncompletePayment(PaymentMethod):
    def pay(self, amount): return "?"           # forgot authorize() and refund()

print(UPIPayment().pay(500))                    # Paid ₹500 via UPI
try:
    IncompletePayment()
except TypeError as e:
    print("TypeError:", e)                      # can't instantiate: abstract methods not implemented
```

| Benefit | What it means |
| --- | --- |
| **Consistency** | Every payment method has the same interface |
| **Enforced contracts** | A missing method raises a `TypeError` as soon as anyone tries to create the object |
| **Scalability** | A new payment method is just a new subclass, with no changes to existing code |
| **Polymorphism** | Client code can call `pay()` on any payment method without knowing which one it is |

### A10. SOLID principles

> **Q:** What are the SOLID principles?

Five design principles for clean, scalable and maintainable object-oriented code:

| | Principle | Meaning | In practice |
| --- | --- | --- | --- |
| **S** | Single Responsibility | A class should have only one reason to change | Separate `InvoiceCalculator` and `InvoicePrinter` classes |
| **O** | Open/Closed | Open for extension, closed for modification | Add `UPIPayment` as a new subclass instead of editing a big `if` / `elif` |
| **L** | Liskov Substitution | Subclasses must work wherever their base class is expected | Any `PaymentMethod` subclass can be passed to `checkout()` |
| **I** | Interface Segregation | Don't force classes to depend on methods they don't use | Split a huge interface into small, focused ones |
| **D** | Dependency Inversion | High-level modules depend on abstractions, not on low-level details | `checkout()` relies on `PaymentMethod`, not on a specific bank's code |

> [!TIP]
> Connect your answer to [A9](#a9-abstract-classes-for-a-payment-system): the payment-system design there already follows **O**, **L** and **D**. Interviewers love seeing principles tied to concrete code.

---

<div align="center">

### 🎯 Final interview tips

**Explain your thinking out loud** · **Mention trade-offs, not just answers** · **Write small, runnable examples** · **Ask clarifying questions**

*Good luck with your interview! ⭐ Star this repository if it helped you.*

</div>

---

**Credits:** Questions and core answers from **CodeBasics** ([codebasics.io](https://codebasics.io)). Additional context, notes and examples by Saurabh S. Code verified on Python 3.12.
