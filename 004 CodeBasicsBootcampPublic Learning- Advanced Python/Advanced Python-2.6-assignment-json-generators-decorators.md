# Advanced Python Assignment: JSON, Generators and Decorators

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Advanced Python course**, covering JSON, generators and decorators.

As Peter Pandey, I took on five more ad-hoc tasks from Loki at AtliQ: analysing a retail client's sales data, monitoring equipment sensors and cutting the cost of a paid financial data API.

## The data in brief

The data files aren't stored in this repository. Here's what they contained:

| File | Contents |
| --- | --- |
| `sales_data.json` | 5 sales records (Laptop, Jeans, Blender, Smartphone, Jacket), each with product, category, quantity and price per unit, across 3 categories |
| `sensor_data.txt` | 6 lines of `sensor,temperature` readings from 3 sensors, ranging from 15.0°C to 24.1°C |
| `aggregated_sales.json` | The output of Task 3: total sales per category |

---

## Task 1: Load the client's sales data

**The ask:** a retail client urgently needs their sales data analysed while the usual developer is on vacation. Step one is loading the JSON file.

```python
import json

with open("sales_data.json", "r") as file:
    sales_data = json.load(file)
```

**Result:** a list of 5 dictionaries, one per product sold. For example: `{'product': 'Laptop', 'category': 'Electronics', 'quantity': 15, 'price_per_unit': 1200}`.

**Key takeaway:** `json.load()` reads a JSON file straight into Python objects. A JSON array becomes a list, and each JSON object becomes a dictionary, ready to loop over.

---

## Task 2: Total sales by category

**The ask:** break down total sales (quantity × price per unit) for each product category.

```python
category_sales = {}
for item in sales_data:
    category = item["category"]
    total_sale = item["quantity"] * item["price_per_unit"]
    if category in category_sales:
        category_sales[category] += total_sale
    else:
        category_sales[category] = total_sale
```

**Result:**

| Category | Total sales |
| --- | --- |
| Electronics | 42,000 |
| Apparel | 4,400 |
| Home Appliances | 3,750 |

**Key takeaway:** a dictionary works as a running-total table. If the category already exists, add to it; if not, create it. Electronics alone brings in 84% of the 50,150 total.

---

## Task 3: Write the totals to a JSON file

**The ask:** deliver the category totals in a structured format the client's systems can import: a list of dictionaries, saved as `aggregated_sales.json`.

```python
aggregated_sales = [{"category": key, "total_sales": value} for key, value in category_sales.items()]

with open("aggregated_sales.json", "w") as file:
    json.dump(aggregated_sales, file, indent=4)
```

**Result:** a neatly indented file with one entry per category, such as `{"category": "Electronics", "total_sales": 42000}`, matching the expected format exactly.

**Key takeaway:** a list comprehension reshapes the data into the structure the client asked for, and `json.dump(..., indent=4)` writes it in a readable layout. Shaping data to the receiving system's format is as important as getting the numbers right.

---

## Task 4: Flag overheating sensor readings with a generator

**The ask:** monitor an equipment sensor file for readings above a temperature threshold. The file is imagined to be huge, too big to read all at once, so the solution must process it line by line.

```python
def read_and_filter_temperatures(filename, threshold):
    """Generator function to read and filter temperatures from a file."""
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            temp = float(parts[1])
            if temp > threshold:
                yield temp

filtered_temperatures = read_and_filter_temperatures("sensor_data.txt", 20.0)

print("Filtered Temperatures (Above 20.0°C):")
for temperature in filtered_temperatures:
    print(f"{temperature}°C")
```

**Result:**

```text
Filtered Temperatures (Above 20.0°C):
21.8°C
22.5°C
24.1°C
```

Three of the six readings exceed 20°C.

**Key takeaway:** `yield` turns the function into a generator. It reads one line, hands back a hot reading, and pauses, so only one line is ever in memory however large the file grows. Each critical reading is printed the moment it's found, which allows immediate action.

---

## Task 5: Cut API costs with a caching decorator

**The ask:** a fintech client looks up company names from tickers through the Bloomberg API, and every call costs money. A decorator should cache results, so each ticker is only ever looked up once.

```python
def cache_decorator(func):
    """Decorator to cache API call results."""
    cache = {}
    def wrapper(ticker):
        if ticker in cache:
            print(f"Cache hit for {ticker}")
            return cache[ticker]
        else:
            print(f"API call for {ticker}")
            result = func(ticker)
            cache[ticker] = result
            return result
    return wrapper

@cache_decorator
def get_company_name(ticker):
    """Simulated API function to fetch a company name based on the ticker symbol."""
    api_responses = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOGL": "Alphabet Inc.",
    }
    return api_responses.get(ticker, "Unknown Company")

# Test the decorated function
print(get_company_name("AAPL"))   # Expected to trigger an API call
print(get_company_name("AAPL"))   # Expected to use cached data
print(get_company_name("MSFT"))   # Expected to trigger an API call
print(get_company_name("MSFT"))   # Expected to use cached data
print(get_company_name("GOOGL"))  # Expected to trigger an API call
print(get_company_name("GOOGL"))  # Expected to use cached data
```

**Result:**

```text
API call for AAPL
Apple Inc.
Cache hit for AAPL
Apple Inc.
API call for MSFT
Microsoft Corporation
Cache hit for MSFT
Microsoft Corporation
API call for GOOGL
Alphabet Inc.
Cache hit for GOOGL
Alphabet Inc.
```

Six lookups, but only **three paid API calls**: half the cost.

**Key takeaway:** the `cache` dictionary is created once, when the decorator is applied, and the inner `wrapper` keeps access to it between calls. Each call checks the cache first and only calls the real function when the answer isn't stored yet. The lookup function itself never had to change.

---

## Overall

| Task | Concept | Tool |
| --- | --- | --- |
| 1 | Reading structured data | `json.load()` |
| 2 | Aggregating by category | A dictionary as a running total |
| 3 | Writing structured output | List comprehension and `json.dump()` |
| 4 | Processing a huge file efficiently | A generator with `yield` |
| 5 | Avoiding repeated costly calls | A caching decorator |

This assignment tied the module together around real client requests. JSON handled data going in and out, a generator kept memory low for a file that could be huge, and a decorator added caching without touching the original function. Each tool solved a practical problem: speed, memory or cost.
