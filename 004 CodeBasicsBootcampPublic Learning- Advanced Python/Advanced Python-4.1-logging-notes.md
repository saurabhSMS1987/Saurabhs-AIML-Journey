# Logging in Python: My Advanced Python Notes

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Logging** lecture from the **CodeBasics Advanced Python course**. The two-handler setup in the audit examples follows the [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html).

## Where I started

So far, whenever I wanted to know what my code was doing, I used `print()`. That works while I'm watching the screen, but the messages disappear once the program finishes, and there's no time, no severity and no record. **Logging** fixes all three. Each message gets a timestamp and a level, and it can be saved to a file. For an auditor, that's an audit trail for the code itself.

## The code in brief

The lecture used three short scripts:

- **`logging_1.py`:** the five log levels, printed to the screen.
- **`logging_2.py`:** a small "web app" with login, data processing and logout that writes to `web_app.log`, including the full error details when bad data arrives.
- **`logging_3.py`:** a named, custom logger that writes every level to `my_app.log`.

## What I learnt

**Five levels, from least to most serious:**

| Level | Use it for |
| --- | --- |
| `DEBUG` | Detailed information while developing |
| `INFO` | Normal progress: "user logged in", "file loaded" |
| `WARNING` | Something unexpected, but the program carries on |
| `ERROR` | Something failed |
| `CRITICAL` | A serious failure that may stop the program |

**The level acts as a filter.** With `level=logging.INFO`, the debug message from `logging_1.py` didn't appear. Only INFO and above were shown:

```text
INFO:root:This is an info message
WARNING:root:This is a warning message
ERROR:root:This is an error message
CRITICAL:root:This is a critical message
```

**Logging to a file, with a timestamp** (`logging_2.py`):

```python
logging.basicConfig(
    filename="web_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```

When `process_data("bad_data")` raised a `ValueError`, `logging.error(..., exc_info=True)` saved the **full traceback** to the file, including the line where it failed. The program still went on to log the logout. The file looked like this (your timestamps will differ):

```text
2026-11-02 10:15:42,118 - INFO - User Dhaval Patel logged in
2026-11-02 10:15:42,118 - ERROR - Error processing data: Invalid data
Traceback (most recent call last):
  File "logging_2.py", line 18, in process_data
    raise ValueError("Invalid data")
ValueError: Invalid data
2026-11-02 10:15:42,119 - INFO - User Dhaval Patel logged out
```

**A custom logger** (`logging_3.py`) gives finer control, built from three pieces:

| Piece | Job | In the lecture |
| --- | --- | --- |
| **Logger** | Receives messages, with its own name and level | `logging.getLogger("my_logger")`, set to `DEBUG` |
| **Handler** | Decides where messages go | `FileHandler("my_app.log")` |
| **Formatter** | Decides how each message looks | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` |

Because this logger was set to `DEBUG`, all five messages, including debug, reached `my_app.log`, each labelled with the logger's name.

**`basicConfig` vs a custom logger:** `basicConfig` is quick for a single script, but only its first call takes effect. Named loggers are better for larger programs, where each part of the code can have its own name, level and destination.

## How this shows up in financial statement audit work

Logging gives an automated audit test its own documentation: what ran, when, on which data, what it found and what went wrong. These snippets use small sample data built in the code.

**1. An audit-trail logger with two destinations.** Everything goes to a file for the workpaper, while only warnings and above appear on screen:

```python
import logging

def audit_logger(name, logfile):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()                                   # avoid duplicate handlers on re-run

    file_handler = logging.FileHandler(logfile, mode="w")
    file_handler.setLevel(logging.DEBUG)                      # the file keeps the complete record
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)                         # the screen shows only what needs attention

    fmt = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    for handler in (file_handler, console):
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger

log = audit_logger("je_testing", "je_testing.log")
```

**2. Logging completeness checks and exceptions during a journal entry test.** Record counts and control totals become evidence that the full population was tested:

```python
ledger = [
    {"je": "JE01", "amount": 4_200,   "approver": "K. Wong"},
    {"je": "JE02", "amount": 98_000,  "approver": None},
    {"je": "JE03", "amount": "12,5O0", "approver": "D. Smith"},     # a corrupted amount: letter O, not zero
    {"je": "JE04", "amount": 125_000, "approver": "D. Smith"},
]
CONTROL_COUNT = 4

log.info("Loaded %d entries (control total: %d)", len(ledger), CONTROL_COUNT)
if len(ledger) != CONTROL_COUNT:
    log.critical("Population incomplete: stopping the test")

flagged = []
for entry in ledger:
    try:
        amount = float(str(entry["amount"]).replace(",", ""))
    except ValueError:
        log.error("%s: amount '%s' could not be read; excluded and raised with the client",
                  entry["je"], entry["amount"], exc_info=True)
        continue
    log.debug("%s: amount %.2f read", entry["je"], amount)
    if amount > 50_000:
        flagged.append(entry["je"])
        log.warning("%s: %.2f exceeds the 50,000 threshold", entry["je"], amount)
    if not entry["approver"]:
        log.warning("%s: no approver recorded", entry["je"])

log.info("Test complete: %d of %d entries flagged: %s", len(flagged), len(ledger), flagged)
```

On screen, only the warnings and the error appear. The log file keeps the complete record, every DEBUG and INFO line included:

```python
with open("je_testing.log") as f:
    lines = f.readlines()
print(len(lines), sum("WARNING" in l for l in lines), sum("ERROR" in l for l in lines))
# 12 3 1: 12 lines (3 of them the error's traceback), 3 warnings and 1 error

for logger_handler in log.handlers:
    logger_handler.close()                                     # release the file
```

**3. Separate loggers for separate procedures.** Named loggers keep each test's messages identifiable, even when they share one file:

```python
recon_log = logging.getLogger("tb_recon")
recon_log.setLevel(logging.INFO)
recon_log.handlers.clear()
handler = logging.FileHandler("je_testing.log")              # append to the same audit file
handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))
recon_log.addHandler(handler)

difference = 1_928_655.41 - 1_903_655.41
if difference:
    recon_log.warning("Revenue: TB differs from GL by %.2f", difference)
handler.close()

with open("je_testing.log") as f:
    print([line.split(" | ")[1] for line in f if " | " in line][-1])   # tb_recon
```

## My reflection

Logging is the coding version of something auditors already do: document the work as it happens, not afterwards from memory. A timestamped log of what was loaded, how many records there were, what failed and what was flagged is exactly the evidence a reviewer looks for. And it's created automatically, every time the test runs.

The `exc_info=True` example stayed with me most. The program didn't crash on bad data. It recorded *exactly* what went wrong and where, then carried on. That's how I want my tests to behave with messy client data: never stop silently and never skip silently, but keep a precise record.
