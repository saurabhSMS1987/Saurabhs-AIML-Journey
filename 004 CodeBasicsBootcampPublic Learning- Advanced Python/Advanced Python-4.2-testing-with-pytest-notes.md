# Testing Python Code with pytest: My Notes

*Nov 3, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Unit Testing with pytest** lecture from **CodeBasics**. Fixtures, `parametrize` and `approx` in the audit examples come from the [pytest documentation](https://docs.pytest.org/en/stable/how-to/index.html).

## Where I started

So far, I've checked my code by running it and looking at the output. That works once, but not every time I change something. **pytest** lets me write small, automatic checks that prove a function does what it should, and re-run all of them in seconds. It's the coding version of something auditors know well: re-performing a control to confirm it still works.

## The code in brief

The lecture used two test files:

- **`test_1.py`:** an `add` function and a test with three checks.
- **`test_2.py`:** `multiply` and `divide` functions, where `divide` refuses to divide by zero, with a test for each.

Running `pytest` found and passed all three tests:

```text
test_1.py::test_add PASSED
test_2.py::test_multiply PASSED
test_2.py::test_divide PASSED
============ 3 passed in 0.01s ============
```

## What I learnt

**A test is a function starting with `test_` that uses `assert`:**

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5        # if any assert is False, the test fails
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

**pytest finds tests automatically.** Run `pytest` in a folder and it collects every file named `test_*.py` (or `*_test.py`) and every function inside that starts with `test_`. Add `-v` to list each test by name.

**Testing that errors happen when they should:**

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ValueError):   # passes only if a ValueError is raised
        divide(10, 0)
```

**Good tests cover three kinds of input,** as the lecture's examples did:

| Kind | Example from the lecture |
| --- | --- |
| Normal values | `add(2, 3) == 5`, `multiply(3, 4) == 12` |
| Edge cases | `add(0, 0)`, `multiply(0, 5)`, negative numbers |
| Invalid input | `divide(10, 0)` must raise an error |

When a test fails, pytest shows exactly which `assert` broke and what the values were, which makes finding the bug much faster.

## How this shows up in financial statement audit work

Every automated audit test is itself code that can be wrong. pytest gives a way to **prove** the logic before relying on its results, and to re-prove it every year when the code is reused. These snippets show two files: the audit functions and the tests for them.

**`audit_checks.py`: the functions being tested**

```python
def check_balanced(lines):
    """Raise an error if a journal entry's debits (+) and credits (-) don't net to zero."""
    difference = round(sum(lines), 2)
    if difference != 0:
        raise ValueError(f"Entry out of balance by {difference:,.2f}")
    return True

def aging_bucket(days_overdue):
    """Classify a receivable by days past due."""
    if days_overdue < 0:
        raise ValueError("Days overdue cannot be negative")
    if days_overdue <= 30:
        return "0-30"
    if days_overdue <= 60:
        return "31-60"
    if days_overdue <= 90:
        return "61-90"
    return "91+"

def to_reporting_currency(amount, rate):
    """Translate a foreign-currency amount at the given rate."""
    return amount * rate

def large_manual_entries(entries, threshold):
    """Return the IDs of manual entries above the threshold."""
    return [e["je"] for e in entries if e["source"] == "Manual" and e["amount"] > threshold]
```

**`test_audit_checks.py`: the tests**

```python
import pytest
from audit_checks import aging_bucket, check_balanced, large_manual_entries, to_reporting_currency

# 1. normal case and error case, as in the lecture's divide() test
def test_balanced_entry_passes():
    assert check_balanced([5_000, -3_000, -2_000])

def test_unbalanced_entry_is_rejected():
    with pytest.raises(ValueError, match="out of balance by 500.00"):
        check_balanced([5_000, -3_000, -1_500])

# 2. boundary testing with parametrize: one test, many cases (like cut-off testing)
@pytest.mark.parametrize("days, expected", [
    (0, "0-30"), (30, "0-30"), (31, "31-60"), (60, "31-60"),
    (61, "61-90"), (90, "61-90"), (91, "91+"), (400, "91+"),
])
def test_aging_bucket_boundaries(days, expected):
    assert aging_bucket(days) == expected

def test_negative_days_are_rejected():
    with pytest.raises(ValueError):
        aging_bucket(-5)

# 3. pytest.approx for currency maths, where floats aren't exact
def test_fx_translation():
    assert to_reporting_currency(0.10 + 0.20, 1.0) == pytest.approx(0.30)

# 4. a fixture: shared sample data that every test can request by name
@pytest.fixture
def sample_entries():
    return [
        {"je": "JE01", "source": "Manual",    "amount": 98_000},
        {"je": "JE02", "source": "Automated", "amount": 250_000},
        {"je": "JE03", "source": "Manual",    "amount": 4_200},
        {"je": "JE04", "source": "Manual",    "amount": 50_000},
    ]

def test_large_manual_entries(sample_entries):
    assert large_manual_entries(sample_entries, 50_000) == ["JE01"]   # 50,000 itself isn't "above"

def test_no_entries_above_a_high_threshold(sample_entries):
    assert large_manual_entries(sample_entries, 1_000_000) == []
```

**Running it:**

```text
$ pytest -v
test_audit_checks.py::test_balanced_entry_passes PASSED
test_audit_checks.py::test_unbalanced_entry_is_rejected PASSED
test_audit_checks.py::test_aging_bucket_boundaries[0-0-30] PASSED
...
test_audit_checks.py::test_aging_bucket_boundaries[400-91+] PASSED
test_audit_checks.py::test_negative_days_are_rejected PASSED
test_audit_checks.py::test_fx_translation PASSED
test_audit_checks.py::test_large_manual_entries PASSED
test_audit_checks.py::test_no_entries_above_a_high_threshold PASSED
============ 14 passed ============
```

**What each new tool adds:**

| Tool | What it does | Audit parallel |
| --- | --- | --- |
| `pytest.raises(..., match=...)` | Checks that the right error, with the right message, is raised | Confirming a control rejects bad input |
| `@pytest.mark.parametrize` | Runs one test over many inputs | Boundary and cut-off testing |
| `pytest.approx` | Compares decimals with a tiny tolerance | Rounding differences in reconciliations |
| `@pytest.fixture` | Supplies shared test data | A standard sample used across procedures |

The boundary test is the one I'd never skip. Is 30 days "0-30" or "31-60"? Is an entry of exactly 50,000 "above" a 50,000 threshold? Those edges are exactly where calculation errors hide.

## My reflection

pytest reframes something I already believe as an auditor: don't rely on a control until you've tested it. My audit scripts are controls too, and a bug in an aging calculation or a threshold test could mean a wrong conclusion. A test file is the evidence that the logic works, and it can be re-run in seconds every time the code changes or the engagement rolls forward.

The `divide` by zero example also made me think about tests differently. A good test doesn't just confirm the happy path. It confirms the code **refuses** bad input, loudly and predictably.
