# Advanced Python Assignment: Pydantic and pytest

*Nov 4, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **[Codebasics.io](https://codebasics.io) Advanced Python course**, covering Pydantic and pytest.

As Peter Pandey, I worked on two client use cases while my manager was busy: **data validation for a restaurant chain's booking system** using Pydantic, and **automated tests for a retail client's inventory system** using pytest. No data files are needed. Everything is defined in code.

---

# Part 1: Restaurant reservations with Pydantic

## Task 1: The `Reservation` model

**The ask:** define a model that validates the customer name (text), the reservation date (a valid date), the number of guests (a whole number) and optional special requests.

```python
from datetime import datetime
from pydantic import BaseModel, ValidationError
from typing import Optional

class Reservation(BaseModel):
    customer_name: str
    reservation_date: datetime
    number_of_guests: int
    special_requests: Optional[str] = None
```

**Key takeaway:** each line is a rule. `datetime` captures the date *and* time of the booking, and `Optional[str] = None` makes special requests truly optional, so a booking without them is still valid.

## Task 2: `create_reservation()` with error handling

**The ask:** a function that takes a dictionary, tries to build a `Reservation` from it, and prints `"Failed to create reservation"` plus the details if validation fails.

```python
def create_reservation(data):
    try:
        reservation = Reservation(**data)
        print(f"Reservation created successfully for {reservation.customer_name} on {reservation.reservation_date}.")
        if reservation.special_requests:
            print(f"Special Requests: {reservation.special_requests}")
    except ValidationError as e:
        print("Failed to create reservation:", e)
```

**Key takeaway:** `Reservation(**data)` unpacks the dictionary into the model's fields. Wrapping it in `try` / `except ValidationError` means bad data produces a clear message instead of crashing the booking system.

## Task 3: A valid reservation

**The ask:** book Vishnu Parmar for 4 guests on 31 Dec 2025 at 19:00, with a window-table request.

```python
correct_data = {
    "customer_name": "Vishnu Parmar",
    "reservation_date": datetime(2025, 12, 31, 19, 0),
    "number_of_guests": 4,
    "special_requests": "Table near the window"
}
create_reservation(correct_data)
```

**Result:**

```text
Reservation created successfully for Vishnu Parmar on 2025-12-31 19:00:00.
Special Requests: Table near the window
```

**Key takeaway:** when every field matches its rule, the model is created, and its fields can be used directly (`reservation.customer_name`), already in the right types.

## Task 4: An invalid reservation

**The ask:** try to book Chen Chu for 3 guests **without** a reservation date, and confirm the error is caught.

```python
incorrect_data = {
    "customer_name": "Chen Chu",
    "number_of_guests": 3
}
create_reservation(incorrect_data)
```

**Result:**

```text
Failed to create reservation: 1 validation error for Reservation
reservation_date
  Field required [type=missing, ...]
```

**Key takeaway:** Pydantic names the exact field that's missing (`reservation_date`) and why (`Field required`), so whoever fixes the booking knows precisely what to supply.

---

# Part 2: Inventory management with pytest

## The `Inventory` class

**The ask:** save the provided `Inventory` class in `inventory_management.py`, then write `test_inventory_management.py` with five specific test functions.

```python
class Inventory:
    def __init__(self):
        self.stock = {}

    def add_stock(self, item, quantity):
        if item in self.stock:
            self.stock[item] += quantity
        else:
            self.stock[item] = quantity

    def remove_stock(self, item, quantity):
        if item not in self.stock or self.stock[item] < quantity:
            raise ValueError("Insufficient stock")
        self.stock[item] -= quantity

    def check_availability(self, item, quantity):
        return self.stock.get(item, 0) >= quantity
```

The class keeps stock in a dictionary of `{item: quantity}`. `remove_stock` refuses to go below zero, and `check_availability` treats an unknown item as zero stock.

## The tests: `test_inventory_management.py`

The solution's `.py` files weren't included in the downloaded materials, so these are the five tests as I wrote them, following the function names the assignment specifies:

```python
import pytest
from inventory_management import Inventory


def test_add_stock():
    inventory = Inventory()
    inventory.add_stock("laptop", 10)
    assert inventory.stock["laptop"] == 10
    inventory.add_stock("laptop", 5)                  # adding again increases the existing count
    assert inventory.stock["laptop"] == 15


def test_remove_stock():
    inventory = Inventory()
    inventory.add_stock("phone", 20)
    inventory.remove_stock("phone", 8)
    assert inventory.stock["phone"] == 12
    with pytest.raises(ValueError, match="Insufficient stock"):
        inventory.remove_stock("tablet", 1)           # an item that was never added


def test_check_availability():
    inventory = Inventory()
    inventory.add_stock("monitor", 5)
    assert inventory.check_availability("monitor", 5) is True     # exactly enough
    assert inventory.check_availability("monitor", 6) is False    # one too many
    assert inventory.check_availability("keyboard", 1) is False   # not stocked at all


def test_remove_stock_with_insufficient_inventory():
    inventory = Inventory()
    inventory.add_stock("printer", 3)
    with pytest.raises(ValueError, match="Insufficient stock"):
        inventory.remove_stock("printer", 4)
    assert inventory.stock["printer"] == 3            # a failed removal leaves stock unchanged


def test_full_inventory_cycle():
    inventory = Inventory()
    inventory.add_stock("headphones", 50)
    inventory.remove_stock("headphones", 20)
    assert inventory.check_availability("headphones", 30) is True
    assert inventory.check_availability("headphones", 31) is False
```

**Result:**

```text
$ pytest -v
test_inventory_management.py::test_add_stock PASSED
test_inventory_management.py::test_remove_stock PASSED
test_inventory_management.py::test_check_availability PASSED
test_inventory_management.py::test_remove_stock_with_insufficient_inventory PASSED
test_inventory_management.py::test_full_inventory_cycle PASSED
============ 5 passed ============
```

**Key takeaways:**

- **Each test starts with a fresh `Inventory()`,** so tests never affect each other.
- **`pytest.raises(ValueError, match=...)`** confirms both that removing too much stock fails, and that it fails with the right message.
- **Edge cases matter:** exactly enough stock (`5` of `5`), one too many (`6`), and an item never stocked at all.
- **A failed removal must leave stock unchanged.** Checking the state *after* an error is as important as checking the error itself.
- **The full-cycle test** checks that the methods work together (add, then remove, then check), not just one at a time.

---

## Overall

| | Pydantic (reservations) | pytest (inventory) |
| --- | --- | --- |
| Protects against | Bad data entering the system | Bad logic in the code |
| How | A model with typed fields | Test functions with `assert` |
| On failure | `ValidationError` naming each bad field | A failed test showing which `assert` broke |
| Error handling shown | `try` / `except ValidationError` | `pytest.raises(ValueError)` |

The two tools complement each other. **Pydantic** checks that the **data** coming in is valid, and **pytest** checks that the **code** handling it behaves correctly, including how it fails. Together, they're how a booking or inventory system earns trust: invalid inputs are stopped at the door, and the business rules are proven to work before anyone relies on them.
