# Exercise 3: Strings

*Oct 25, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Exercise from the **Strings** lecture of the **CodeBasics Python course**.

This exercise put the Lecture 3 tools to work: reading built-in help, f-strings, slicing and `replace()`.

## 1. Exploring `help(str)`

`help(str)` lists every method a string has. I tried `endswith()`:

```python
s = "Python is Easy."
s.endswith(".")     # True

s2 = "I love Pandas"
s2.endswith(".")    # False
```

## 2. f-strings

```python
vegetables = 3
fruits = 2
print(f"I eat {vegetables} vegetables and {fruits} fruits daily")
# I eat 3 vegetables and 2 fruits daily
```

The exercise asks for how many, so I stored numbers here. The original solution stored fruit names as text, which also works with f-strings.

## 3. Slicing

```python
string = "The Himalayas are one of the youngest mountain range on the planet."

print(string[0:13])                          # The Himalayas
print(string[-29:-15])                       # mountain range
print(f"{string[0:13]} {string[-14:]}")      # The Himalayas on the planet.
```

Negative indexes count back from the end, which is handy when the part I want sits near the end of the sentence.

## 4. Fixing a sentence with `replace()`

```python
string = "There are 9 planet in the solar system"
string = string.replace("9 planet", "8 planets")   # one-line fix
print(string)   # There are 8 planets in the solar system
```

Strings can't be edited in place, so `replace()` returns a new string, and I save it back to the same variable.

## What stuck with me

Slicing by position is precise but fragile: if the sentence changes, the numbers break. In audit work, I'd rather find text with `in` or `index()` than rely on fixed positions in messy data.
