# Takeaways: Classes, Inheritance and Exception Handling

*Oct 28, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Basics: Classes, Exception Handling – Takeaways* from the **CodeBasics Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the fourth module, kept handy for quick revision.

## Classes and objects

- Object-oriented programming (OOP) makes larger projects easier to manage, and classes and objects are at its core.
- A **class** is a blueprint, and an **object** is one specific instance. `Human` is a class, and Mira Sharma is an object of it.
- Classes have **properties** (data) and **methods** (behaviours).
- `__init__` sets an object's properties when it is created.

## Operator overloading

- Special methods define how operators such as `<`, `>`, `==`, `+`, `-` and `*` work on my own objects.
- This makes custom classes more intuitive, readable and easier to maintain.

## Inheritance

- A child class takes on its parent's attributes and methods, so code is reused, not repeated.
- New subclasses extend or customise existing code.
- Inheritance gives code a clear, maintainable structure.

## Exception handling

- Lets a program recover from errors instead of crashing.
- `try` / `except` separates normal code from error-handling code.
- Catching **specific** exceptions allows a targeted response to each type of error.
- `finally` always runs, so clean-up is guaranteed.

## The `__main__` entry point

- `if __name__ == "__main__":` marks where a script starts running, like `main()` in C++ or Java.
- When a file is imported, its `__name__` is the module's name (for example, `np.__name__` is `'numpy'`). The block under the check therefore runs only when the file is run directly, not when it is imported.

## All together

```python
class Claim:
    def __init__(self, claim_id, amount):
        self.claim_id = claim_id
        self.amount = amount

    def __lt__(self, other):                       # operator overloading
        return self.amount < other.amount


class MotorClaim(Claim):                           # inheritance
    pass


if __name__ == "__main__":                         # entry point
    claims = [MotorClaim("MC-01", 48000), Claim("CL-02", 95000)]
    try:
        largest = max(claims)                      # max() uses __lt__
        print(largest.claim_id)                    # CL-02
    except ValueError:
        print("No claims to review")
```
