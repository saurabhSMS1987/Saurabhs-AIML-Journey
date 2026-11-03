# Building APIs with FastAPI: Notes

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **FastAPI** lecture from the **CodeBasics Advanced Python course**. Query validation, `HTTPException` and request bodies in the audit examples come from the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/).

## Where I started

In the last lecture, I *used* other people's APIs with `requests`. This one flipped it around: with **FastAPI**, I can *build* an API myself, so other people and programs can ask my Python code for data. The whole lecture example fits in one short file, and FastAPI even writes an interactive documentation page for it automatically.

## The code in brief

The lecture's `main.py` has two endpoints:

- **`/get_items/{cuisine}`** returns two dishes for Indian, American or Italian food, such as `["Samosa", "Dosa"]`.
- **`/get_coupon/{code}`** returns a discount for coupon codes 1, 2 and 3 (10%, 20% and 30%).

## What I learnt

**Creating an app and an endpoint:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/get_items/{cuisine}")          # a GET endpoint; {cuisine} is a path parameter
def get_items(cuisine: AvailableCuisines):
    return food_items.get(cuisine)        # dictionaries and lists are returned as JSON automatically
```

**Running it:** `uvicorn main:app --reload` starts a local server. `main` is the file name, `app` is the FastAPI object, and `--reload` restarts it whenever the code changes. Then:

- `http://127.0.0.1:8000/get_items/indian` returns `["Samosa", "Dosa"]`.
- `http://127.0.0.1:8000/docs` opens interactive documentation where every endpoint can be tried in the browser.

**Type hints do the validation.** This was the standout idea:

```python
from enum import Enum

class AvailableCuisines(str, Enum):        # only these three values are allowed
    indian = "indian"
    american = "american"
    italian = "italian"

@app.get("/get_coupon/{code}")
async def get_coupon(code: int):           # must be a whole number
    return {"discount_amount": coupon_code.get(code)}
```

| Request | Response |
| --- | --- |
| `/get_items/indian` | `200` → `["Samosa", "Dosa"]` |
| `/get_items/french` | `422` → *Input should be 'indian', 'american' or 'italian'* |
| `/get_coupon/2` | `200` → `{"discount_amount": "20%"}` |
| `/get_coupon/abc` | `422` → *Input should be a valid integer* |
| `/get_coupon/9` | `200` → `{"discount_amount": null}` |

FastAPI checked every input against the type hints and rejected bad ones with a clear message, without a single `if` statement. The last row shows the limit: a *valid* integer that isn't a real coupon still returns `null`. Snippet 2 below shows how to return a proper `404` for that.

**`def` vs `async def`:** both work. `async def` lets the server handle other requests while one waits on something slow, like a database or another API.

**A small naming note:** in the lecture file, both functions are called `get_items`. FastAPI still registers both routes, but giving each function its own name, like `get_coupon` above, avoids confusion.

## How this shows up in financial statement audit work

FastAPI could turn audit analytics into a small internal service. Instead of emailing scripts around, a team could call one endpoint for materiality, or for exceptions on a given account. These snippets build a mini audit API with sample data.

```python
from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

audit_api = FastAPI(title="Audit Analytics API")

journal_entries = {
    "JE01": {"account": "4000", "amount": 4_200,   "source": "Automated"},
    "JE02": {"account": "4000", "amount": 98_000,  "source": "Manual"},
    "JE03": {"account": "6300", "amount": 125_000, "source": "Manual"},
    "JE04": {"account": "6300", "amount": 9_950,   "source": "Manual"},
}
```

**1. Allowed values with an Enum.** This follows the lecture's cuisine pattern, here limiting requests to known financial statement line items:

```python
FSLI_ACCOUNTS = {"revenue": ["4000", "4100"], "opex": ["6000", "6100", "6300"], "cash": ["1000"]}

class FSLI(str, Enum):
    revenue = "revenue"
    opex = "opex"
    cash = "cash"

@audit_api.get("/fsli/{fsli}/accounts")
def accounts_for(fsli: FSLI):
    return {"fsli": fsli, "accounts": FSLI_ACCOUNTS[fsli]}
```

**2. A single entry, with a proper "not found".** `HTTPException` returns `404` instead of the lecture's `null`:

```python
@audit_api.get("/journal-entries/{je_id}")
def get_entry(je_id: str):
    if je_id not in journal_entries:
        raise HTTPException(status_code=404, detail=f"{je_id} not found in the ledger")
    return journal_entries[je_id]
```

**3. Exception filtering with validated query parameters.** `Query(ge=0)` rejects a negative threshold before the code even runs:

```python
@audit_api.get("/journal-entries")
def large_entries(min_amount: float = Query(50_000, ge=0), source: str | None = None):
    return [je for je, e in journal_entries.items()
            if e["amount"] >= min_amount and (source is None or e["source"] == source)]
```

**4. A materiality calculator with a validated request body.** A **Pydantic model** describes the JSON the endpoint expects, and FastAPI checks it automatically:

```python
class MaterialityInput(BaseModel):
    benchmark: str
    benchmark_amount: float = Field(gt=0)
    percentage: float = Field(gt=0, le=10)          # % of the benchmark, capped at 10

@audit_api.post("/materiality")
def materiality(inputs: MaterialityInput):
    overall = inputs.benchmark_amount * inputs.percentage / 100
    return {"benchmark": inputs.benchmark,
            "overall_materiality": round(overall, 2),
            "performance_materiality": round(overall * 0.75, 2),     # 75% of overall: a common judgement
            "clearly_trivial": round(overall * 0.05, 2)}
```

**Testing it without starting a server:** FastAPI's `TestClient` calls the endpoints directly from Python:

```python
from fastapi.testclient import TestClient

client = TestClient(audit_api)
print(client.get("/fsli/revenue/accounts").json())        # {'fsli': 'revenue', 'accounts': ['4000', '4100']}
print(client.get("/fsli/goodwill/accounts").status_code)  # 422: not an allowed line item
print(client.get("/journal-entries/JE99").json())         # {'detail': 'JE99 not found in the ledger'}
print(client.get("/journal-entries", params={"min_amount": 50000, "source": "Manual"}).json())   # ['JE02', 'JE03']
print(client.get("/journal-entries", params={"min_amount": -1}).status_code)                     # 422: negative threshold
print(client.post("/materiality", json={"benchmark": "Revenue", "benchmark_amount": 25_000_000, "percentage": 1}).json())
# {'benchmark': 'Revenue', 'overall_materiality': 250000.0, 'performance_materiality': 187500.0, 'clearly_trivial': 12500.0}
```

The materiality percentages here are examples. The real ones come from the firm's methodology and the auditor's judgement.

## My reflection

FastAPI made building an API feel surprisingly small: a decorator, a function and some type hints. What impressed me most was the validation. Every bad input, whether an unknown cuisine, text instead of a number or a negative threshold, was rejected with a clear message, without me writing any checks. In audit terms, that's a preventive control built into the code.

The materiality example is where I can see this going. Calculations like materiality, sampling or standard exception tests could sit behind one consistent, documented endpoint, so everyone on the team gets the same answer from the same logic, and the `/docs` page explains how to use it.
