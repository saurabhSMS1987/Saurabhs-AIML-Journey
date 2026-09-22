# Python Topic of the Day #1: Conditional Statements

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Level:** Beginner  
**Audience:** New learners wanting to understand Python basics  
**Duration:** 30-45 minutes

---

## Overview

Conditional statements are the foundation of programming logic. They allow your code to make decisions and take different actions based on conditions. Without conditional statements, all programs would run the same way every time!

**Why is this important?**
```
Without conditionals:
Code runs the same way → No decisions possible

With conditionals:
Code can make decisions → Smart programs!

Example:
IF temperature is cold → Wear a jacket
ELSE → Wear a t-shirt
```

---

## Part 1: Understanding Conditions

### 1.1 What is a Condition?

A condition is a statement that is either **True** or **False**.

```python
# Examples of conditions
age = 20
age > 18           # True (age is greater than 18)
age < 18           # False (age is not less than 18)
age == 20          # True (age equals 20)
age != 25          # True (age is not equal to 25)
```

**Real-world examples:**
```
Is it raining? → True or False
Is the door open? → True or False
Do you have enough money? → True or False
Is the password correct? → True or False
```

---

### 1.2 Boolean Values

Python has two special boolean values: **True** and **False**

```python
# Boolean values
is_student = True
is_working = False

print(is_student)   # True
print(is_working)   # False
```

---

## Part 2: Comparison Operators

Comparison operators are used to create conditions.

### 2.1 Basic Comparison Operators

```python
# Equal to: ==
age = 20
age == 20          # True
age == 25          # False

# Not equal to: !=
age != 20          # False
age != 25          # True

# Greater than: >
age > 18           # True
age > 25           # False

# Less than: <
age < 25           # True
age < 18           # False

# Greater than or equal to: >=
age >= 20          # True
age >= 25          # False

# Less than or equal to: <=
age <= 20          # True
age <= 18          # False
```

**Quick Reference Table:**

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | True |
| `!=` | Not equal to | `5 != 3` | True |
| `>` | Greater than | `5 > 3` | True |
| `<` | Less than | `5 < 10` | True |
| `>=` | Greater than or equal | `5 >= 5` | True |
| `<=` | Less than or equal | `5 <= 6` | True |

---

### 2.2 Comparison with Different Data Types

```python
# Comparing numbers
5 > 3              # True
10.5 < 10          # False

# Comparing strings (alphabetical order)
"apple" < "banana" # True
"zebra" > "apple"  # True
"hello" == "hello" # True

# Comparing with variables
name = "John"
name == "John"     # True
name == "Jane"     # False

# Comparing with None
value = None
value == None      # True
value is None      # Also True
```

---

## Part 3: The if Statement

### 3.1 Basic if Syntax

```python
if condition:
    # Code here runs if condition is True
    print("Condition is True!")
```

**Important:** Python uses **indentation** (spaces) to show which code belongs to the if block.

---

### 3.2 Simple if Example

```python
age = 20

if age >= 18:
    print("You are an adult")

# Output: You are an adult
```

**Step by step:**
```
1. age = 20
2. Check if age >= 18? → 20 >= 18 is True
3. Since True, execute print statement
4. Output: "You are an adult"
```

**Another example:**

```python
temperature = 15

if temperature < 20:
    print("It's cold outside")

# Output: It's cold outside
```

---

### 3.3 if with No Action

```python
score = 50

if score > 100:
    print("Perfect score!")

# If condition is False, nothing happens
# No output printed
```

---

## Part 4: The else Statement

### 4.1 if...else Syntax

Use `else` to run code when the condition is False.

```python
if condition:
    # Code here runs if condition is True
    print("Condition is True!")
else:
    # Code here runs if condition is False
    print("Condition is False!")
```

---

### 4.2 if...else Examples

**Example 1: Age check**

```python
age = 15

if age >= 18:
    print("You can vote")
else:
    print("You cannot vote yet")

# Output: You cannot vote yet
```

**Example 2: Pass/Fail**

```python
score = 35

if score >= 40:
    print("You passed!")
else:
    print("You failed. Try again.")

# Output: You failed. Try again.
```

**Example 3: Even or Odd**

```python
number = 7

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")

# Output: Odd number
# (7 divided by 2 has remainder 1, so it's odd)
```

---

## Part 5: The elif Statement

### 5.1 Using elif for Multiple Conditions

Use `elif` (else if) to check multiple conditions.

```python
if condition1:
    # Code if condition1 is True
elif condition2:
    # Code if condition1 is False AND condition2 is True
elif condition3:
    # Code if condition1 and condition2 are False AND condition3 is True
else:
    # Code if all conditions are False
```

---

### 5.2 elif Examples

**Example 1: Grade Assignment**

```python
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")
# Output: Your grade is: C
```

**Step by step:**
```
1. score = 75
2. Is 75 >= 90? → False, skip this block
3. Is 75 >= 80? → False, skip this block
4. Is 75 >= 70? → True! Execute this block
5. grade = "C"
6. Print "Your grade is: C"
```

**Example 2: Traffic Light**

```python
light_color = "red"

if light_color == "red":
    action = "Stop"
elif light_color == "yellow":
    action = "Slow down"
elif light_color == "green":
    action = "Go"
else:
    action = "Unknown color"

print(f"Light is {light_color}, so {action}")
# Output: Light is red, so Stop
```

**Example 3: Temperature Clothing**

```python
temperature = 25

if temperature < 0:
    clothing = "Heavy winter coat"
elif temperature < 10:
    clothing = "Winter jacket"
elif temperature < 20:
    clothing = "Light jacket"
else:
    clothing = "Light clothing"

print(f"Wear: {clothing}")
# Output: Wear: Light clothing
```

---

## Part 6: Logical Operators

### 6.1 Using Multiple Conditions with AND

The `and` operator requires BOTH conditions to be True.

```python
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive")
else:
    print("You cannot drive")

# Output: You can drive
# (Both age >= 18 AND has_license are True)
```

**Visual:**
```
Condition 1: age >= 18 → True
Condition 2: has_license → True
Result: True AND True → True
```

**More examples:**

```python
# Entering a club: Must be 21 AND have ID
age = 25
has_id = True

if age >= 21 and has_id:
    print("You can enter")
else:
    print("You cannot enter")
# Output: You can enter

# All conditions must be True
age = 25
has_id = False

if age >= 21 and has_id:
    print("You can enter")
else:
    print("You cannot enter")
# Output: You cannot enter (has_id is False)
```

---

### 6.2 Using Multiple Conditions with OR

The `or` operator requires AT LEAST ONE condition to be True.

```python
can_drive = False
can_take_taxi = True

if can_drive or can_take_taxi:
    print("You can get to work")
else:
    print("You're stuck")

# Output: You can get to work
# (can_take_taxi is True, so OR is True)
```

**Visual:**
```
Condition 1: can_drive → False
Condition 2: can_take_taxi → True
Result: False OR True → True
```

**More examples:**

```python
# Can go outside if it's not raining OR you have umbrella
is_raining = True
has_umbrella = True

if not is_raining or has_umbrella:
    print("You can go outside")
else:
    print("You should stay inside")
# Output: You can go outside

# Only need ONE to be True
is_raining = True
has_umbrella = False

if not is_raining or has_umbrella:
    print("You can go outside")
else:
    print("You should stay inside")
# Output: You should stay inside (both are False)
```

---

### 6.3 Using NOT

The `not` operator reverses True/False.

```python
is_raining = True

if not is_raining:
    print("It's not raining")
else:
    print("It's raining")

# Output: It's raining
# (not True = False)

# Another example
is_raining = False

if not is_raining:
    print("It's not raining")
else:
    print("It's raining")

# Output: It's not raining
# (not False = True)
```

**Truth Table:**

| Condition | NOT Condition |
|-----------|---------------|
| True | False |
| False | True |

---

### 6.4 Combining Operators

```python
age = 25
has_money = True
wants_to_go = False

# Must be adult AND have money AND want to go
if age >= 18 and has_money and wants_to_go:
    print("Let's go!")
else:
    print("We can't go")

# Output: We can't go
# (wants_to_go is False)

# Can go if has money OR has credit card
has_money = False
has_credit_card = True

if has_money or has_credit_card:
    print("You can buy it")
else:
    print("You can't afford it")

# Output: You can buy it
```

---

## Part 7: Common Mistakes for Beginners

### ❌ Wrong → ✅ Correct

```python
# Mistake 1: Using = instead of ==
age = 20
if age = 18:           # ❌ Error! = is assignment
    print("Adult")
    
if age == 18:          # ✅ Correct! == is comparison
    print("Adult")

# Mistake 2: Forgetting indentation
if age >= 18:
print("Adult")         # ❌ Error! Not indented

if age >= 18:
    print("Adult")     # ✅ Correct! Indented

# Mistake 3: Using quotes wrong in comparisons
name = "John"
if name = "John":      # ❌ Wrong
    print("Hello John")
    
if name == "John":     # ✅ Correct
    print("Hello John")

# Mistake 4: Extra colon
if age > 18            # ❌ Missing :
    print("Adult")
    
if age > 18:           # ✅ Has :
    print("Adult")

# Mistake 5: String comparison case sensitivity
name = "JOHN"
if name == "john":     # ❌ False! "JOHN" ≠ "john"
    print("Hello")
    
if name.lower() == "john":  # ✅ True! Convert to lowercase first
    print("Hello")
```

---

## Part 8: Nested Conditionals

### 8.1 if Inside if

You can put an if statement inside another if statement.

```python
age = 20
has_license = True

if age >= 18:
    print("You're an adult")
    
    if has_license:
        print("You can drive")
    else:
        print("You need a license to drive")
else:
    print("You're not an adult yet")

# Output:
# You're an adult
# You can drive
```

**Real example: Ticket pricing**

```python
age = 12
student = True

if age < 18:
    print("You get student pricing")
    
    if student:
        price = 5
    else:
        price = 8
else:
    print("You get regular pricing")
    price = 15

print(f"Your ticket costs: ${price}")
# Output:
# You get student pricing
# Your ticket costs: $5
```

---

## Part 9: Practical Examples

### 9.1 Example 1: Simple Login

```python
stored_password = "secret123"
entered_password = "secret123"

if entered_password == stored_password:
    print("Login successful!")
else:
    print("Invalid password")

# Output: Login successful!
```

---

### 9.2 Example 2: Restaurant Reservation

```python
time = 19  # 7 PM in 24-hour format
party_size = 4

if time >= 11 and time < 14:
    print("Lunch time!")
elif time >= 17 and time < 21:
    print("Dinner time!")
else:
    print("We're closed")

if party_size > 6:
    print("We need a reservation for that size")
elif party_size > 0 and party_size <= 6:
    print("We have a table for you")
else:
    print("Invalid party size")

# Output:
# Dinner time!
# We have a table for you
```

---

### 9.3 Example 3: BMI Calculator

```python
weight = 70      # kg
height = 1.75    # meters

bmi = weight / (height ** 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal weight"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print(f"Your BMI: {bmi:.1f}")
print(f"Category: {category}")

# Output:
# Your BMI: 22.9
# Category: Normal weight
```

---

### 9.4 Example 4: Game - Guessing Number

```python
secret_number = 7
guess = 7

if guess == secret_number:
    print("You won! 🎉")
elif guess > secret_number:
    print("Too high! Try lower")
elif guess < secret_number:
    print("Too low! Try higher")

# Output: You won! 🎉
```

---

## Part 10: Quick Reference

### if Statement Syntax

```python
# Simple if
if condition:
    code_block

# if...else
if condition:
    code_block_1
else:
    code_block_2

# if...elif...else
if condition1:
    code_block_1
elif condition2:
    code_block_2
else:
    code_block_3
```

### Comparison Operators

```python
==   # Equal to
!=   # Not equal to
>    # Greater than
<    # Less than
>=   # Greater than or equal
<=   # Less than or equal
```

### Logical Operators

```python
and   # Both must be True
or    # At least one must be True
not   # Reverses True/False
```

---

## Part 11: Practice Exercises

### Exercise 1: Basic if/else
```python
# Given: score = 85
# TODO: Print "Pass" if score >= 60, else print "Fail"

score = 85
if score >= 60:
    print("Pass")
else:
    print("Fail")
```

### Exercise 2: Using elif
```python
# Given: age = 16
# TODO: Print "Child" if age < 13, "Teen" if 13-19, "Adult" if 20+

age = 16
if age < 13:
    print("Child")
elif age < 20:
    print("Teen")
else:
    print("Adult")
```

### Exercise 3: Using Logical Operators
```python
# Given: temperature = 25, has_umbrella = False
# TODO: Print "Go outside" if temp > 15 AND (not raining OR has umbrella)

temperature = 25
is_raining = True
has_umbrella = False

if temperature > 15 and (not is_raining or has_umbrella):
    print("Go outside")
else:
    print("Stay inside")
```

---

## Key Concepts Summary

✅ **Conditions** are statements that are True or False  
✅ **Comparison operators** (<, >, ==, !=, <=, >=) create conditions  
✅ **if** runs code when condition is True  
✅ **else** runs code when condition is False  
✅ **elif** checks additional conditions  
✅ **and** requires all conditions to be True  
✅ **or** requires at least one condition to be True  
✅ **not** reverses True and False  
✅ **Indentation** matters! Shows which code belongs to the condition  

---

## Common Patterns

### Pattern 1: Validation
```python
age = int(input("Enter your age: "))
if age >= 0 and age <= 150:
    print("Valid age")
else:
    print("Invalid age")
```

### Pattern 2: Multiple Checks
```python
username = "john"
password = "pass123"
is_logged_in = False

if username == "john" and password == "pass123":
    is_logged_in = True
    print("Welcome!")
else:
    print("Login failed")
```

### Pattern 3: Exclusive Checks
```python
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")
else:
    print("It's a weekday")
```

---

## What's Next?

After mastering conditional statements:
1. Learn **loops** (repeat code multiple times)
2. Learn **functions** (organize reusable code)
3. Learn **lists** (store multiple values)
4. Combine all three for powerful programs!

---

## Tips for Success

✅ **Practice writing conditions** - Start simple, build complexity  
✅ **Test edge cases** - What happens at boundaries? (18 years old, 0, negative)  
✅ **Read code carefully** - Make sure logic matches your intention  
✅ **Use meaningful variable names** - `is_student` is clearer than `x`  
✅ **Comment your conditions** - Explain complex logic  
✅ **Indent consistently** - Use 4 spaces or 1 tab  

---

*Conditional statements are the logic of programming. Master them, and you can make your programs smart!* 🚀
