# Data Validation with Pydantic: My Advanced Python Notes

*Nov 4, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **pydantic Tutorial** lecture from **[Codebasics.io](https://codebasics.io)**. `Field` constraints and `field_validator` in the audit examples come from the [Pydantic documentation](https://docs.pydantic.dev/latest/).

## Where I started

I first met Pydantic briefly in the FastAPI lecture, as the `BaseModel` that checked incoming JSON. This lecture looked at it on its own. **Pydantic** lets you describe what valid data looks like, field by field and type by type, and then checks every record against that description automatically. For someone who spends a lot of time asking "is this data complete and accurate?", that's a very appealing idea.

## The code in brief

- **`pydantic_tutorial.ipynb`:** a `User` model with `id`, `name`, `age` and `email`, tested with good data, missing fields, a wrong type, a convertible type and an optional field.
- **`myserver.py`:** a FastAPI app with one `POST /add_user/` endpoint that receives a `User` and confirms it was created.

## What I learnt

**Defining a model:** a class that inherits from `BaseModel`, with a type for each field:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

User(id=3, name="Dhaval Patel", age=30, email="dhaval@xyz.com")
# User(id=3, name='Dhaval Patel', age=30, email='dhaval@xyz.com')
```

**What Pydantic does with each kind of input:**

| Input | Result |
| --- | --- |
| All fields, right types | A valid `User` object |
| Missing `age` and `email` | `ValidationError`: 2 errors, both **Field required** |
| `age="30 years"` | `ValidationError`: **Input should be a valid integer** |
| `age="30"` | Accepted: the text `"30"` is **converted** to the number `30` |

The `ValidationError` lists **every** problem at once, each with the field name, which is far more useful than stopping at the first.

The notebook's saved error messages use the older Pydantic v1 wording (such as `field required`). Current Pydantic v2 says `Field required` and `Input should be a valid integer`. The behaviour is the same.

**Optional fields:** `Optional[str] = None` means the field can be left out, and then it's `None`:

```python
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    age: int
    email: str
    address: Optional[str] = None

print(User(id=3, name="Dhaval Patel", age=30, email="dhaval@xyz.com"))
# id=3 name='Dhaval Patel' age=30 email='dhaval@xyz.com' address=None
```

**With FastAPI** (`myserver.py`), the model validates the JSON body of every request automatically:

```python
@app.post("/add_user/")
def create_user(user: User):
    return f"User created successfully: User {user}"
```

When I tested it, `{"id": 1, "name": "Mira", "age": "32"}` was accepted, with `"32"` converted to `32`. A request with no `age` was rejected with a `422` and `Field required` for `['body', 'age']`, before the function even ran.

## How this shows up in financial statement audit work

A Pydantic model is essentially a **data specification for an extract**: which fields must exist, what type each one is, and what values are allowed. Checking every row against it is a completeness and accuracy test on the data itself. These snippets use sample journal entry records built in the code.

**1. A journal entry model with audit rules built in:**

```python
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

FY_START, FY_END = date(2026, 1, 1), date(2026, 12, 31)

class JournalEntry(BaseModel):
    je_id: str = Field(pattern=r"^JE\d{5}$")           # must look like JE00001
    posting_date: date                                 # "2026-03-15" text becomes a real date
    account: str = Field(min_length=4, max_length=4)   # 4-character account code, kept as text
    amount: Decimal                                    # exact decimals, no float rounding
    source: str
    approver: Optional[str] = None

    @field_validator("posting_date")
    @classmethod
    def within_financial_year(cls, d):
        if not FY_START <= d <= FY_END:
            raise ValueError(f"{d} is outside FY2026")
        return d

    @field_validator("amount")
    @classmethod
    def not_zero(cls, v):
        if v == 0:
            raise ValueError("zero-value entry")
        return v
```

**2. Validating a whole extract, and keeping every rejection as evidence:**

```python
raw_rows = [
    {"je_id": "JE00001", "posting_date": "2026-03-15", "account": "4000", "amount": "12500.00", "source": "Automated", "approver": "SYSTEM"},
    {"je_id": "JE00002", "posting_date": "2027-01-04", "account": "4000", "amount": "98000",    "source": "Manual"},
    {"je_id": "JE3",     "posting_date": "2026-06-30", "account": "6300", "amount": "0",        "source": "Manual",    "approver": "K. Wong"},
    {"je_id": "JE00004", "posting_date": "2026-09-01", "account": "61",   "amount": "4,200",    "source": "Manual",    "approver": "D. Smith"},
    {"je_id": "JE00005", "posting_date": "2026-12-31", "account": "1200", "amount": "250000",   "source": "Manual"},
]

valid, rejected = [], []
for i, row in enumerate(raw_rows, start=1):
    try:
        valid.append(JournalEntry(**row))
    except ValidationError as e:
        for err in e.errors():
            rejected.append({"row": i, "field": err["loc"][0], "problem": err["msg"]})

print(len(valid), "valid,", len({r["row"] for r in rejected}), "rejected")   # 2 valid, 3 rejected
for r in rejected:
    print(r)
```

Each rejected row lists **every** problem it has, which gives a ready-made data quality findings list for the client:

```text
{'row': 2, 'field': 'posting_date', 'problem': 'Value error, 2027-01-04 is outside FY2026'}
{'row': 3, 'field': 'je_id', 'problem': "String should match pattern '^JE\\d{5}$'"}
{'row': 3, 'field': 'amount', 'problem': 'Value error, zero-value entry'}
{'row': 4, 'field': 'account', 'problem': 'String should have at least 4 characters'}
{'row': 4, 'field': 'amount', 'problem': 'Input should be a valid decimal'}
```

**3. Typed, clean data for the tests that follow.** Once validated, amounts are exact `Decimal`s and dates are real dates, so the actual audit tests are simple and safe:

```python
manual_unapproved = [je.je_id for je in valid if je.source == "Manual" and je.approver is None]
year_end = [je.je_id for je in valid if je.posting_date == FY_END]
print(manual_unapproved, year_end, sum(je.amount for je in valid))   # ['JE00005'] ['JE00005'] 262500.00
```

## My reflection

Pydantic turned a habit I already have, checking an extract before trusting it, into code. Instead of scattered `if` statements, the rules live in one readable model: what fields are required, what types they are, and what counts as valid. Every row is checked against the same rules every time. The way it collects *all* the errors in a row, not just the first, is exactly what I'd want for a data quality finding.

The automatic conversion is useful but worth watching: `"30"` became `30` without complaint, which is helpful for messy exports. But in audit, I'd want to know when a value needed converting, so strict rules (like the account code's length and the date window) belong in the model wherever the data matters.
