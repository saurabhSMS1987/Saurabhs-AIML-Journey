# Python File Handling: Notes

*Oct 27, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **File Handling** lecture from the **CodeBasics Python course**.

## Where I started

Until now, all my data lived inside the code: lists I typed in by hand. Real audit data doesn't work like that. It comes as exports, CSVs and text files. This lecture taught me to read files into Python and write results back out. It felt like the moment my practice code could finally meet real client data.

## What I learnt

**Reading a file.** `open()` opens it, a loop reads it line by line, and `close()` releases it. `with` closes the file automatically, so it's the safer habit:

```python
with open("funny.txt", "r") as f:
    for line in f:
        print(line)
```

The printout had blank lines between rows because each line already ends with `\n`, and `print` adds another one. `readlines()` reads every line into a list at once.

**File modes:**

| Mode | Meaning | Watch out |
| --- | --- | --- |
| `"r"` | Read | The file must already exist |
| `"w"` | Write | **Replaces** everything already in the file |
| `"a"` | Append | Adds to the end and keeps what's there |

`write()` writes one string, and `writelines()` writes a list of strings. Neither adds `\n` for me.

**Analysing a CSV.** The cricket example read `scores.csv` (player, match, score) into a dictionary of lists, then used `min()`, `max()` and `sum()/len()` for each player:

```python
player, _, score = line.split(",")   # _ means "I don't need this column"
score = int(score.strip())           # strip() removes the line ending first
```

Rohit came out with a minimum of 9, a maximum of 140 and an average of 100.8.

**Deleting files.** `os.remove()` deletes a file. Checking `os.path.exists()` first avoids an error if it isn't there.

One thing I spotted: `file_tutorial.py` reads the score from `tokens[1]`, but in this CSV that column is the match name (`match#1`). The notebook version, which takes the third column, is the one that works.

## How this shows up in insurance audit work

These snippets use the same steps on a small claims extract: read, analyse, then write the results.

**1. Reading a claims extract and profiling each adjuster.** This uses the same pattern as the cricket scores, applied to claims.

```python
# claims.csv rows look like: adjuster,claim_id,amount
with open("claims.csv", "w") as f:   # sample extract, so the code runs
    f.writelines(["anita,CL-01,12000\n", "rahul,CL-02,95000\n",
                  "anita,CL-03,8000\n", "rahul,CL-04,88000\n"])

adjuster_claims = {}
with open("claims.csv", "r") as f:
    for line in f:
        adjuster, _, amount = line.split(",")
        amount = int(amount.strip())
        if adjuster in adjuster_claims:
            adjuster_claims[adjuster].append(amount)
        else:
            adjuster_claims[adjuster] = [amount]

for adjuster, amounts in adjuster_claims.items():
    avg = sum(amounts) / len(amounts)
    print(f"{adjuster} ==> Claims: {len(amounts)}, Max: {max(amounts)}, Avg: {avg}")
```

An adjuster whose average is far above their peers' is worth a closer look.

**2. Writing an exception report.** `"w"` creates a fresh report on every run.

```python
exceptions = ["CL-02: exceeds authority limit\n", "CL-04: exceeds authority limit\n"]
with open("exceptions_report.txt", "w") as f:
    f.write("Claims Exception Report\n")
    f.writelines(exceptions)
```

**3. Keeping an audit trail with append mode.** `"a"` adds a line each time a test runs and never erases the history.

```python
with open("audit_log.txt", "a") as f:
    f.write("2026-10-26: authority limit test run on claims.csv, 2 exceptions\n")
```

**4. Checking that the data arrived before testing.** A missing extract should be reported, not left to crash the script.

```python
import os

if os.path.exists("claims.csv"):
    print("Extract received: starting tests")
else:
    print("claims.csv missing: follow up with the client")
```

## My reflection

The difference between `"w"` and `"a"` is the lesson I'll remember. One wrong letter, and a whole audit log is gone without any warning. So I'll use `"a"` for logs and `"w"` only for reports I mean to recreate, and I'll never write over the client's original extract. I was also pleased to catch the `tokens[1]` bug myself. Checking that the column you read is the one you meant is good practice in audit, not just in code.
