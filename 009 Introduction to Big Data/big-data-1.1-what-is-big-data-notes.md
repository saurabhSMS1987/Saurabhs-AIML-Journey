# What Is Big Data? My Big Data: Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **"What is Big Data?"** video lecture from my Big Data course, summarised from the lecture transcript. The Oyo and Goldman Sachs examples are the instructor's own career experiences.

## Where I started

Instead of opening with a textbook definition, the instructor explained big data through two projects from his own career. The first worked perfectly with an ordinary SQL database, and the second didn't. That contrast made the idea click for me: big data isn't a fixed size. It's the point where traditional databases stop coping.

## What I learnt

### Two projects, two very different data problems

| | Project 1: booking replies (Oyo, 2018) | Project 2: "Delhi 2x" conversion |
| --- | --- | --- |
| **Goal** | Work out from WhatsApp replies whether a guest wanted to confirm or cancel a booking | Understand user behaviour to increase bookings in Delhi |
| **Data** | Short text replies, often with spelling mistakes | Time spent viewing each hotel, hotel images, bookings and users, all growing daily |
| **Storage** | One table in a relational database (RDBMS) | Google BigQuery |
| **Result** | Simple SQL queries were enough | Too large and varied for a traditional database |

In the second project, even small signals mattered. A user spending 2 to 3 seconds on one hotel and 0 seconds on another showed which hotels interested them, across hundreds of thousands of hotels.

### Why a traditional database struggles

You *can* keep adding storage to a database such as Oracle (**vertical scaling**), but that runs into four problems:

1. **Hardware limits:** like the RAM in a laptop, you can only expand so far.
2. **Slow, fragile operations:** as tables grow, data must be split up (partitioned). Joining lakhs of users with their hotel views becomes slow and more likely to fail, and users won't wait 10 seconds for an order page.
3. **Unstructured data:** images and videos can be *stored* in a relational database, but not *processed* there. That's where **NoSQL** databases come in, later in the course.
4. **Cost:** storing and processing fast-growing data in traditional systems gets very expensive.

### The definition

> Big data refers to datasets that are **too large, too fast or too complex** for traditional databases to process efficiently.

The lecture made one more point: big data is **both the problem and the solution**. The term covers the data itself and the technologies built to handle it.

### Why big data emerged

- **Growth of the internet:** more users created more data that needed storing and analysing.
- **Social media:** Facebook, Instagram, TikTok and YouTube generate photos, videos and posts at huge scale.
- **IoT and smart devices:** smart bulbs, switches and cars constantly capture data.
- **Real-time services:** Uber tracks millions of riders and drivers, with locations updated every second and processed almost immediately.

The next lecture covers the characteristics of big data: its size, speed and variety.

## How this shows up in financial statement audit work

Audit data is heading the same way. Ledgers for large clients run to millions of journal entries, Excel stops at **1,048,576 rows**, and evidence increasingly arrives as PDFs, emails and system logs rather than tidy tables. The snippets below use small simulated data, but each one shows a big-data idea at audit scale.

**1. When the ledger outgrows Excel: test the full population in chunks.** Reading a large file piece by piece is the first step past the limits of a single tool.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(1)
n = 1_500_000                                  # more rows than Excel can open
pd.DataFrame({
    "je_id": np.arange(n),
    "amount": rng.gamma(2.0, 2000.0, n).round(2),
    "weekend": rng.random(n) < 0.03,
}).to_csv("gl_fy2026.csv", index=False)

rows, flagged = 0, 0
for chunk in pd.read_csv("gl_fy2026.csv", chunksize=250_000):
    rows += len(chunk)
    flagged += (chunk["weekend"] & (chunk["amount"] > 20_000)).sum()

print(rows)       # 1500000: every entry tested, not a sample
print(flagged)    # large entries posted at weekends, for follow-up
```

**2. Split, process, combine: the idea behind distributed systems.** Big data tools spread work across many machines. The same logic works on group entities: summarise each subsidiary separately, then combine the results.

```python
entities = {
    "UK Ltd":  pd.DataFrame({"account": ["Revenue", "Revenue", "Cash"], "amount": [500, 300, 120]}),
    "US Inc":  pd.DataFrame({"account": ["Revenue", "Cash"], "amount": [900, 410]}),
    "IN Pvt":  pd.DataFrame({"account": ["Revenue", "Cash", "Cash"], "amount": [250, 60, 40]}),
}

partials = [df.groupby("account")["amount"].sum() for df in entities.values()]   # each "machine" works alone
group_tb = pd.concat(partials).groupby(level=0).sum()                            # then the results are combined
print(group_tb.to_dict())    # {'Cash': 630, 'Revenue': 1950}
```

Only the small summaries travel between steps, never the full ledgers. That's why this approach scales.

**3. Unstructured evidence: approvals buried in text.** As in the lecture's image example, an email can be stored easily but is hard to analyse in table form. A simple text search is a first step:

```python
approvals = pd.Series([
    "Approved by CFO on 28 Sep for vendor payment JE1042",
    "Please post urgently, approval to follow",
    "Approved by Finance Director, JE1077",
])

missing_approval = approvals[~approvals.str.contains("approved by", case=False)]
print(missing_approval.tolist())   # ['Please post urgently, approval to follow']: entry posted before approval
```

**4. Speed: checking transactions as they arrive.** Like Uber's location updates, continuous controls monitoring tests each transaction as it's posted, instead of waiting for year-end.

```python
def transaction_feed():
    yield from [("T1", 4_200), ("T2", 98_000), ("T3", 650), ("T4", 125_000)]

for txn_id, amount in transaction_feed():
    if amount > 50_000:
        print(f"Alert: {txn_id} for {amount:,} needs review")
# Alert: T2 for 98,000 needs review
# Alert: T4 for 125,000 needs review
```

## My reflection

I liked that this lecture began with a real problem rather than a list of buzzwords. The two Oyo projects showed that the same company, and even the same person, can be fine with SQL one month and need big data tools the next. What changed wasn't the question being asked; it was the volume, speed and variety of the data.

That maps neatly onto audit. Testing 25 samples from a ledger is a "project 1" problem. Testing every journal entry, reading approval emails and monitoring transactions continuously are "project 2" problems, and that's where audit analytics is heading. I'm curious to see which tools the course introduces for them.
