# Iterators and Generators: Notes

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Iterators and Generators** lecture from the **CodeBasics Advanced Python course**.

## Where I started

I've written `for` loops since my first Python lecture without asking *how* they work. This lecture opened the lid: every `for` loop quietly asks an object for "the next item" until it runs out. Once I understood that, **generators** made sense. They're functions that hand back one item at a time, instead of building a whole list in memory. For ledgers with millions of rows, that matters.

## The data in brief

- **`pricing.txt`:** 1,000 pipe-delimited rows (`ticker|country|price|date`) for 10 tech stocks across 10 countries, with prices from 100.04 to 499.76, dated 2023.
- **`stock_1.txt` to `stock_3.txt`:** one JSON record each, for **AAPL, RIL and NVDA**, with about 17 metrics: price, P/E, market cap, revenue, margins and so on. RIL's file has no `operating_margin`, so the files don't all share the same fields.

## What I learnt

**Iterator basics.** A file object is an iterator. `iter()` gets it ready, and each `next()` returns one more line:

```python
f = open("pricing.txt", "r")
iterator = iter(f)
next(iterator)      # 'MSFT|BRA|381.26|2023-10-27\n'
next(iterator)      # 'CSCO|USA|187.64|2023-02-12\n'
```

A `for` loop does exactly this behind the scenes, and stops when the iterator raises `StopIteration`.

**A custom iterator class** needs two special methods:

```python
class RemoteControl:
    def __init__(self):
        self.channels = ["NDTV", "CNN", "ESPN"]
        self.index = -1

    def __iter__(self):            # returns the iterator itself
        return self

    def __next__(self):            # returns the next item, or signals the end
        self.index += 1
        if self.index == len(self.channels):
            raise StopIteration
        return self.channels[self.index]
```

`for channel in RemoteControl()` printed NDTV, CNN and ESPN. Calling `next()` a fourth time raised `StopIteration`.

**Generators do the same job with far less code.** Any function containing `yield` returns a generator. It pauses at each `yield` and resumes from that point on the next `next()`:

```python
def remote_control():
    yield "NDTV"
    yield "CNN"
    yield "ESPN"

itr = remote_control()     # type: generator
next(itr)                  # 'NDTV'
```

**Why it matters: memory.** The lecture's first `get_company_data()` read all three stock files into a list before returning anything. The generator version `yield`s one file's contents at a time, so only one file is in memory at once.

**Infinite sequences.** A generator can run forever, because it only computes a value when asked:

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
# the first 10 values: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

| | List | Generator |
| --- | --- | --- |
| Builds | Everything at once | One item at a time |
| Memory | Grows with the data | Stays small |
| Can reuse | Yes, any number of times | No: once exhausted, it's empty |
| Can index (`x[5]`) | Yes | No |

## How this shows up in financial statement audit work

Full-year general ledgers can run to millions of lines: too big to load comfortably, but easy to **stream** with a generator. These snippets create a small sample file first, so they run as written.

```python
import itertools
import random

random.seed(3)
with open("gl_extract.txt", "w") as f:
    f.write("je_id|account|amount|source|preparer\n")
    for i in range(1, 2001):
        source = "Manual" if i % 10 == 0 else "Automated"
        f.write(f"JE{i:05d}|{random.choice(['4000', '5000', '6300'])}|{random.uniform(50, 60000):.2f}|{source}|{random.choice(['A. Rao', 'M. Gomez'])}\n")
```

**1. Streaming a ledger one line at a time.** The generator reads, parses and yields each journal entry, so memory use stays flat however big the file is:

```python
def read_gl(path):
    with open(path) as f:
        next(f)                                   # skip the header row
        for line in f:
            je_id, account, amount, source, preparer = line.rstrip("\n").split("|")
            yield {"je_id": je_id, "account": account, "amount": float(amount),
                   "source": source, "preparer": preparer}

for entry in itertools.islice(read_gl("gl_extract.txt"), 2):   # preview the first 2 without reading the rest
    print(entry["je_id"], entry["amount"])
# JE00001 35578.82
# JE00002 54960.89
```

**2. A generator pipeline for exception testing.** Each step is a generator feeding the next, like stages of an audit procedure, and nothing is held in memory between them:

```python
def manual_only(entries):
    return (e for e in entries if e["source"] == "Manual")        # a generator expression

def above(entries, threshold):
    for e in entries:
        if e["amount"] > threshold:
            yield e

flagged = above(manual_only(read_gl("gl_extract.txt")), 50_000)
selected = [e["je_id"] for e in flagged]
print(len(selected), selected[:3])   # 38 ['JE00040', 'JE00110', 'JE00120']
```

**3. Reading many monthly files as one stream.** This follows the lecture's `get_company_data()`, with each record tagged with its source file for the audit trail:

```python
for month in ("2026_10", "2026_11"):
    with open(f"je_{month}.txt", "w") as f:
        f.write("je_id|account|amount|source|preparer\n")
        f.write(f"JE{month[-2:]}001|4000|1200.00|Automated|SYSTEM\n")

def read_months(months):
    for month in months:
        for entry in read_gl(f"je_{month}.txt"):
            entry["source_file"] = f"je_{month}.txt"
            yield entry

for e in read_months(["2026_10", "2026_11"]):
    print(e["je_id"], e["source_file"])     # JE10001 je_2026_10.txt | JE11001 je_2026_11.txt
```

**4. A custom iterator for systematic sampling.** This uses the lecture's class pattern: `__next__` returns every *n*th item from a random start, and stops with `StopIteration`:

```python
class SystematicSample:
    """Yield every interval-th item, starting from a random point in the first interval."""
    def __init__(self, population, interval, seed=None):
        self.population = population
        self.interval = interval
        self.position = random.Random(seed).randrange(interval)

    def __iter__(self):
        return self

    def __next__(self):
        if self.position >= len(self.population):
            raise StopIteration
        item = self.population[self.position]
        self.position += self.interval
        return item

invoice_ids = [f"INV{n:04d}" for n in range(1, 101)]
sample = list(SystematicSample(invoice_ids, interval=25, seed=42))
print(sample)   # ['INV0021', 'INV0046', 'INV0071', 'INV0096']: the fixed seed lets a reviewer re-perform it
```

## My reflection

The `for` loop is no longer a black box. It's just `next()` called again and again until `StopIteration`. And generators answer a practical worry I've had since the big data lectures: how to handle a ledger too large for memory. Reading it line by line with `yield`, and chaining small generator steps together, feels a lot like running audit procedures in sequence.

The one habit to build: **a generator can only be used once.** If I need the results twice, such as to count them and also list them, I'll collect them into a list first, as snippet 2 does.
