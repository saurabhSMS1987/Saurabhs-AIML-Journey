# The 5 Vs of Big Data: My Big Data Notes

*Oct 30, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **"5 Vs of Big Data"** video lecture from the course ***Master Big Data with Hadoop, Spark, Kafka & Cloud***, summarised from the lecture transcript.

## Where I started

Last lecture defined big data as data that's too large, too fast or too complex for traditional databases. This one broke that idea into five characteristics: **volume, velocity, variety, veracity and value**. The instructor's aim wasn't for us to memorise five words. It was to use them as a checklist when deciding whether a problem actually needs big data tools.

## What I learnt

### 1. Volume: how much data

Volume is the size of the data being generated. A small shop can track sales in a notebook or a small database, but an Amazon-scale store needs systems that store and process data across many servers.

**The myth to avoid:** there is **no fixed size** at which a problem "becomes" big data, and volume isn't the only factor. 30 GB might overwhelm a startup but be routine for Google. A smaller dataset that is complex may need big data tools, while a large but simple one may not. The instructor warned that this question comes up in interviews.

### 2. Velocity: how fast data arrives and must be processed

| Type | How it works | Example from the lecture | Typical tools |
| --- | --- | --- | --- |
| **Real time** | Each event is processed within seconds | Card fraud alerts; the YouTube feed updating straight after you watch a video | Kafka, Spark Streaming |
| **Near real time** | Data arrives continuously and is processed every few minutes | Bank balances or payment status updating after a minute or two | |
| **Batch** | Data is processed on a schedule | The monthly credit card bill; daily or 12-hourly reports | Hadoop, Spark |

Building scheduled batch pipelines is a core part of a data engineer's job.

### 3. Variety: what form the data takes

| Kind | Description | Examples |
| --- | --- | --- |
| **Structured** | Rows and columns with a defined schema | SQL database tables |
| **Semi-structured** | Has some structure, such as tags or nesting, but no fixed table layout | JSON, XML (the lecture also listed CSV here) |
| **Unstructured** | No predefined structure | Videos, images, emails, documents, text files |

One app, like Instagram or LinkedIn, can hold all three: profile details, nested activity data, and photos and videos. Relational databases handle tables well but struggle to *process* unstructured data.

Two points I'd refine from the lecture, based on common usage:

- **CSV** is usually classed as *structured*, because it's plain rows and columns.
- **Unstructured** means data with no predefined data model. An email is easy for a person to read; it's the *computer* that can't query it like a table.

### 4. Veracity: can the data be trusted?

Veracity is the quality and reliability of data, such as an employee record with a **negative age**. Bad data leads to bad decisions, so cleaning and validation must happen *before* analysis.

### 5. Value: is the data worth the effort?

Data should support business decisions. The lecture's example: sales data showing iPhone purchases spiking around payday and Black Friday. Having lots of data isn't a reason to adopt big data technology by itself. The data has to produce actionable insight.

## How this shows up in financial statement audit work

The five Vs work well as a checklist for any audit data request. These snippets use small sample data built in the code.

**1. Velocity: batch, near real time and real time, in audit terms.**

```python
import pandas as pd

payments = pd.DataFrame({
    "time":   pd.to_datetime(["2026-09-30 09:01", "2026-09-30 09:03", "2026-09-30 09:04",
                              "2026-09-30 09:07", "2026-09-30 09:12"]),
    "amount": [4200, 98000, 650, 125000, 3100],
})

# real time: check each payment before release
for t, amt in zip(payments["time"], payments["amount"]):
    if amt > 50_000:
        print(f"{t:%H:%M} hold payment of {amt:,} for approval")      # 09:03 and 09:07

# near real time: totals every 5 minutes (micro-batches)
print(payments.groupby(pd.Grouper(key="time", freq="5min"))["amount"].sum().to_dict())

# batch: one month-end summary, like a period-end journal review
print(payments["amount"].sum())                                      # 230950
```

Most audit testing is still **batch**: period-end, after the fact. Continuous controls monitoring moves towards **near real time** and **real time**.

**2. Variety: three kinds of evidence for one audit.**

```python
import json
import re

# structured: trial balance
tb = pd.DataFrame({"account": ["Revenue", "Receivables"], "balance": [-1_950_000, 640_000]})

# semi-structured: a bank API response (JSON)
bank_json = '{"account": "1234", "transactions": [{"date": "2026-09-30", "amount": 12500}, {"date": "2026-09-30", "amount": -860}]}'
bank = pd.json_normalize(json.loads(bank_json), record_path="transactions", meta="account")
print(bank["amount"].sum())                                          # 11640

# unstructured: a lease clause, read with a pattern
clause = "The lessee shall pay annual rent of $240,000 commencing 1 January 2026 for a term of 5 years."
rent = int(re.search(r"\$([\d,]+)", clause).group(1).replace(",", ""))
term = int(re.search(r"term of (\d+) years", clause).group(1))
print(rent * term)                                                   # 1200000: total commitment, for the lease disclosure
```

**3. Veracity: validate before trusting the ledger.** The lecture's negative age becomes a negative quantity or a future posting date:

```python
gl = pd.DataFrame({
    "je_id":    ["JE1", "JE2", "JE3", "JE4"],
    "debit":    [5000, 0, 1200, 0],
    "credit":   [0, 5000, 0, 1150],
    "posted":   pd.to_datetime(["2026-09-28", "2026-09-28", "2026-09-30", "2027-01-15"]),
    "approver": ["A. Rao", "A. Rao", None, "M. Gomez"],
})

checks = {
    "debits equal credits":      bool(gl["debit"].sum() == gl["credit"].sum()),
    "no posting after year-end": bool((gl["posted"] <= "2026-12-31").all()),
    "every entry approved":      bool(gl["approver"].notnull().all()),
}
print(checks)
# {'debits equal credits': False, 'no posting after year-end': False, 'every entry approved': False}
```

If any check fails, the extract goes back to the client *before* any substantive testing begins. Analysing an extract that doesn't balance produces confident but unreliable conclusions.

**4. Value: turning data into a decision.** Like the payday iPhone insight, a timing pattern can tell me where to focus testing:

```python
revenue = pd.DataFrame({
    "date":   pd.to_datetime(["2026-09-02", "2026-09-15", "2026-09-28", "2026-09-29", "2026-09-30"]),
    "amount": [120_000, 95_000, 210_000, 340_000, 415_000],
})

last_3_days = revenue[revenue["date"] >= "2026-09-28"]["amount"].sum()
share = round(last_3_days / revenue["amount"].sum() * 100, 1)
print(f"{share}% of September revenue was booked in the last 3 days")   # 81.8%: a cut-off risk to test
```

## My reflection

The volume myth was the most useful part for me. I'd assumed big data simply meant "very large". This lecture showed that speed, format and quality can matter as much as size, so whether you need big data tools depends on the organisation as well as the data.

Veracity and value felt the most familiar, because they're audit ideas in different words. Veracity is about whether the data is complete and accurate enough to rely on. Value is about whether the analysis leads to a better-targeted procedure, not just a bigger spreadsheet. It's reassuring that the big data world treats data quality as a core characteristic rather than an afterthought.
