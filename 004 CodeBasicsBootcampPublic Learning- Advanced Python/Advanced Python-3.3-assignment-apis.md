# Advanced Python Assignment 3: Working with APIs

*Nov 2, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Advanced Python course**, covering APIs in Python with the `requests` library.

As Peter Pandey, I took on two API tasks: brewery details for Tony Sharma's US client call, and a user-profile helper for one of Loki's AtliQ client applications. Both use free public APIs, so no data files or API keys are involved.

## The APIs in brief

| API | What it provides | Used in |
| --- | --- | --- |
| [Open Brewery DB](https://www.openbrewerydb.org/) | Public data on US breweries: name, type, city and state | Task 1 |
| [JSONPlaceholder](https://jsonplaceholder.typicode.com/) | Fake practice data (users, posts) for testing HTTP requests | Task 2 |

---

## Task 1: Brewery details by state

**The ask:** Tony Sharma needs the breweries in a given state for a client call tomorrow, showing each brewery's name, type and city, with errors handled gracefully.

```python
import requests

def fetch_breweries_by_state(state):
    """Fetch brewery data for a specified state from Open Brewery DB API."""
    url = f"https://api.openbrewerydb.org/breweries?by_state={state.replace(' ', '_')}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful
        breweries = response.json()
        if not breweries:
            return "No breweries found in the specified state."
        return breweries
    except requests.exceptions.HTTPError as err:
        return f"HTTP error occurred: {err}"
    except Exception as err:
        return f"An error occurred: {err}"

# Usage
state = "New York"
breweries_info = fetch_breweries_by_state(state)

print(f"Breweries in {state}:")
for brewery in breweries_info:
    name = brewery['name']
    brew_type = brewery['brewery_type']
    location = f"{brewery['city']}, {brewery['state']}"
    print(f"- {name} ({brew_type}) located in {location}")
```

**Result:** the first page of New York results, 50 breweries, listed alphabetically:

```text
Breweries in New York:
- 12 Gates Brewing Company (brewpub) located in Williamsville, New York
- 16 Stone Brewpub (brewpub) located in Holland Patent, New York
- 1940's Brewing Company (micro) located in Holbrook, New York
...
- Bottomless Brewing, LLC (brewpub) located in Geneva, New York
```

| Brewery type | Count |
| --- | --- |
| Micro | 24 |
| Brewpub | 14 |
| Planning | 4 |
| Contract | 3 |
| Large | 3 |
| Proprietor | 2 |

**Key takeaways:**

- **Format inputs to suit the API.** `state.replace(' ', '_')` turns "New York" into `New_York`, the underscore form the API expects in place of a space.
- **`raise_for_status()` turns a failed request into an exception,** so a `404` or `500` is caught instead of producing bad data.
- **Two layers of error handling:** `HTTPError` catches bad responses from the server, and the general `Exception` catches anything else, such as a lost network connection.
- **Check for an empty result.** An empty list means the request worked but found nothing, which deserves its own message.

---

## Task 2: A user-profile helper

**The ask:** Loki needs a function, `fetch_user_data`, that fetches a user from JSONPlaceholder and returns just their name, email and address as a dictionary.

```python
import requests

def fetch_user_data(user_id):
    """Fetch user data for a specified user ID from JSONPlaceholder API."""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        user_name = data['name']
        user_email = data['email']
        user_address = f"{data['address']['street']}, {data['address']['city']}"
        return {
            'name': user_name,
            'email': user_email,
            'address': user_address
        }
    except requests.exceptions.HTTPError as err:
        return f"HTTP error occurred: {err}"
    except Exception as err:
        return f"An error occurred: {err}"

# Usage
user_id = 1
user_info = fetch_user_data(user_id)
user_info
```

**Result:**

```python
{'name': 'Leanne Graham',
 'email': 'Sincere@april.biz',
 'address': 'Kulas Light, Gwenborough'}
```

This matches the expected output exactly.

**Key takeaways:**

- **The user ID goes in the URL path** (`/users/1`), the standard way to ask a REST API for one specific record.
- **Nested JSON is read in steps.** The street and city sit inside an `address` object, so `data['address']['street']` reaches one level down.
- **Return only what's needed.** The full user record has many more fields (phone, website, company, coordinates). Shaping it into three clean fields gives the client application exactly what it asked for.

---

## Overall

| Skill | Task 1 | Task 2 |
| --- | --- | --- |
| Building the request URL | Query parameter (`?by_state=New_York`) | Path parameter (`/users/1`) |
| Parsing the response | `response.json()` → a list of breweries | `response.json()` → one user dictionary |
| Extracting fields | Name, type, city and state | Name, email, and the nested street and city |
| Handling errors | `raise_for_status()` plus `try` / `except` | `raise_for_status()` plus `try` / `except` |

Both tasks follow the same four-step pattern: **build the URL, send the request, check it worked, and extract the fields that matter.** Once that pattern is familiar, any JSON API, from brewery listings to exchange rates or bank feeds, works the same way.
