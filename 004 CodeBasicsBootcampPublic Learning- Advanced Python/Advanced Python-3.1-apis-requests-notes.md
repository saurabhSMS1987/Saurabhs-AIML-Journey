# Working with APIs Using `requests`: Notes

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Interacting with API** lecture from the **CodeBasics Advanced Python course**. Timeouts and `raise_for_status()` come from the [Requests documentation](https://requests.readthedocs.io/en/latest/user/quickstart/), and the historical-rates URL pattern from the [Open Exchange Rates documentation](https://docs.openexchangerates.org/). **API keys are masked throughout these notes.**

## Where I started

Until now, every bit of data I worked with came from a file: CSV, Excel or JSON on my own machine. This lecture showed how to ask another system for data directly, over the internet, through an **API**. A few lines with the `requests` library send a request, get a reply in JSON, and turn it into Python dictionaries I already know how to work with.

## The data in brief

The lecture used three public APIs:

- **JSONPlaceholder** (`jsonplaceholder.typicode.com`): a free practice API with sample "posts". It was used for GET, POST and query parameters.
- **CoinDesk Bitcoin Price Index:** the Bitcoin price in USD, GBP and EUR. On the day of the recording it showed about 60,814 USD.
- **Open Exchange Rates:** live currency rates against the US dollar (for example, 1 USD = 3.673 AED). It needs a personal **app ID**, which is shown here as `YOUR_APP_ID`.

## What I learnt

**GET: ask for data.**

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")
if response.status_code == 200:
    data = response.json()        # JSON text -> Python list of dictionaries
    print(data[0]["title"])
```

**POST: send data.** The `json=` argument converts a dictionary to JSON. The server replied `201 Created` and gave the new post `id: 101`.

```python
new_post = {"title": "foo", "body": "bar", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
print(response.status_code, response.json())   # 201 {'title': 'foo', 'body': 'bar', 'userId': 1, 'id': 101}
```

**Query parameters: filter on the server.** `params=` builds the `?userId=1` part of the address for you:

```python
response = requests.get("https://jsonplaceholder.typicode.com/posts", params={"userId": 1})
```

**Status codes tell you what happened:**

| Code | Meaning |
| --- | --- |
| 200 | OK: the request worked |
| 201 | Created: new data was saved |
| 400 | Bad request: the server couldn't understand it |
| 401 | Unauthorized: a valid key or login is needed |
| 404 | Not found |
| 500 | Server error |

The lecture checked `response.status_code` with `if` / `elif` so each case gets a sensible message, instead of the code failing later on missing data.

**Reading nested JSON:** the Bitcoin price sat three levels deep: `data["bpi"]["USD"]["rate"]`.

**API keys:** Open Exchange Rates needs an app ID in the address:

```python
app_id = "YOUR_APP_ID"   # masked: never publish a real key
url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
```

A key works like a password, and it often carries usage limits or costs. It should never be committed to GitHub. Read it from an environment variable instead, as the audit snippets below do.

**One note on the CoinDesk example:** the original `api.coindesk.com/v1/bpi` endpoint is reported to no longer respond, and CoinDesk's newer API requires a key. The lecture code may need a different source if you run it today.

## How this shows up in financial statement audit work

APIs let me pull **independent evidence** straight from the source, such as exchange rates or bank and invoice data, instead of relying on figures the client typed into a spreadsheet. These snippets keep the key out of the code and save what was retrieved, so the evidence is reproducible.

**1. A safe, reusable request.** It has a timeout so it never hangs, raises an error on bad status codes, and keeps a record of what was retrieved, with the key removed:

```python
import os
from datetime import datetime

import requests

APP_ID = os.environ.get("OXR_APP_ID", "YOUR_APP_ID")   # set OXR_APP_ID on your machine; never hardcode it

def fetch_json(url, params=None, evidence_log=None):
    """GET a JSON resource and record the request as audit evidence (with the key removed)."""
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()                          # turns 4xx/5xx into an exception
    if evidence_log is not None:
        safe_params = {k: ("****" if k in ("app_id", "api_key", "token") else v) for k, v in (params or {}).items()}
        evidence_log.append({"url": url, "params": safe_params, "status": response.status_code,
                             "retrieved_at": datetime.now().isoformat(timespec="seconds")})
    return response.json()
```

**2. Year-end exchange rates for translating foreign-currency balances.** Open Exchange Rates offers historical rates by date, with US dollars as the base:

```python
def year_end_rates(date="2026-12-31", evidence_log=None):
    data = fetch_json(f"https://openexchangerates.org/api/historical/{date}.json",
                      params={"app_id": APP_ID, "symbols": "GBP,EUR,INR"}, evidence_log=evidence_log)
    return data["rates"]              # e.g. {'GBP': 0.79, 'EUR': 0.92, 'INR': 83.2}: units per 1 USD

def to_usd(balances, rates):
    """Translate {currency: amount} balances into USD."""
    return {ccy: round(amount / rates[ccy], 2) for ccy, amount in balances.items()}
```

**3. Re-performing the client's translation.** Compare the rate the client used with the independent rate, and flag differences above a tolerance:

```python
def compare_rates(client_rates, independent_rates, tolerance_pct=0.5):
    exceptions = []
    for ccy, client_rate in client_rates.items():
        diff_pct = (client_rate - independent_rates[ccy]) / independent_rates[ccy] * 100
        if abs(diff_pct) > tolerance_pct:
            exceptions.append((ccy, client_rate, independent_rates[ccy], round(diff_pct, 2)))
    return exceptions

# example rates, as they might be returned for the year-end date
independent = {"GBP": 0.79, "EUR": 0.92, "INR": 83.20}
client_used = {"GBP": 0.79, "EUR": 0.95, "INR": 83.25}

print(to_usd({"GBP": 1_250_000, "EUR": 480_000}, independent))   # {'GBP': 1582278.48, 'EUR': 521739.13}
print(compare_rates(client_used, independent))                   # [('EUR', 0.95, 0.92, 3.26)]: the EUR rate is off by 3.3%
```

**4. Pulling records page by page with query parameters.** Many systems, such as invoicing platforms, return data in pages. A loop with `params=` collects them all. This uses the lecture's practice API, so it runs without a key:

```python
def fetch_all(url, page_size=20):
    records, page = [], 1
    while True:
        batch = fetch_json(url, params={"_page": page, "_limit": page_size})
        if not batch:
            break
        records.extend(batch)
        page += 1
    return records

# posts = fetch_all("https://jsonplaceholder.typicode.com/posts")   # 100 records, in 5 pages of 20
```

Once collected, the records are just a list of dictionaries, ready for the comprehensions, sets and pandas tools from earlier lectures.

## My reflection

APIs change where audit evidence can come from. Instead of asking a client for a rate table or an export and then checking it, I can go to the independent source myself, and record exactly what I retrieved and when. That's stronger evidence, and it's repeatable.

The lecture's `xxxxxxxxxxxxx` placeholder for the app ID was also a good habit to copy. A key in a notebook is easy to share by accident, so keys belong in environment variables, never in code or on GitHub. And the CoinDesk endpoint going quiet was a reminder that external sources change. Saving what you retrieved, as the evidence log does, matters as much as retrieving it.
