# Takeaways: Advanced Python: APIs

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** *Python Advanced: APIs – Takeaways* from the **CodeBasics Advanced Python course** ([codebasics.io](https://codebasics.io)).

My one-page recap of the APIs module, kept handy for quick revision.

## What is an API?

- **API** stands for **Application Programming Interface**: a way for different software programs to talk to each other.
- **`requests`** is the popular Python package for **calling** APIs.
- **FastAPI** is a popular Python web framework for **building** APIs.
- The four most common REST API calls:

| Method | Purpose | Example |
| --- | --- | --- |
| `GET` | Read data | Fetch a list of invoices |
| `POST` | Create data | Submit a new record |
| `PUT` | Update data | Replace an existing record |
| `DELETE` | Remove data | Delete a record |

## Calling APIs with `requests`

- `requests` makes HTTP calls simple, and supports `GET`, `POST`, `PUT`, `DELETE` and more.
- `requests.get()` fetches data and `requests.post()` sends it, with parameters or data passed as arguments.
- Check **`response.status_code`** to confirm success, and use **`response.json()`** to turn the reply into Python data.
- **Exception handling is crucial:** networks fail, servers return errors and data can be missing.

## Building APIs with FastAPI

- FastAPI builds servers that answer requests, including **inference requests** from machine-learning models.
- Its advantages over alternatives such as Flask:
  - **Speed**
  - **Built-in data validation**, through type hints
  - **Built-in documentation**, an interactive page at `/docs`
  - **Faster development**

## All together

```python
import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()                                      # build an API

@app.get("/materiality/{revenue}")
def materiality(revenue: float):                     # type hint = built-in validation
    return {"overall_materiality": revenue * 0.01}

client = TestClient(app)                             # call it without starting a server
response = client.get("/materiality/25000000")
if response.status_code == 200:
    print(response.json())                           # {'overall_materiality': 250000.0}

try:                                                 # calling an external API safely
    r = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
    r.raise_for_status()
    print(r.json()["name"])                          # Leanne Graham
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```
