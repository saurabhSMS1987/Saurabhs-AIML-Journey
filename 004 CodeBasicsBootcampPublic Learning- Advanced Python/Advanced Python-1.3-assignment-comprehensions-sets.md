# Advanced Python Assignment 1: Comprehensions and Sets

*Nov 1, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Advanced Python course**, covering comprehensions and sets.

As Peter Pandey, I helped Loki's team at AtliQ with eight quick tasks for different clients. Each one uses a set, or a list, set or dictionary comprehension.

---

## Task 1: Unique product categories

**The ask:** an e-commerce client wants to see which product categories exist in their inventory of 7 products.

```python
products = [
    {"product_name": "Laptop", "category": "Electronics", "price": 1200},
    {"product_name": "Jeans", "category": "Apparel", "price": 40},
    {"product_name": "Coffee Maker", "category": "Home Appliances", "price": 80},
    {"product_name": "Smartphone", "category": "Electronics", "price": 999},
    {"product_name": "Jacket", "category": "Apparel", "price": 60},
    {"product_name": "Blender", "category": "Home Appliances", "price": 150},
    {"product_name": "Book", "category": "Literature", "price": 15},
]

unique_categories = {product["category"] for product in products}

print("Unique Product Categories:")
for category in unique_categories:
    print(f"- {category}")
```

**Result:** 4 categories: Electronics, Apparel, Home Appliances and Literature.

**Key takeaway:** a set comprehension collects unique values in one line, so repeated categories (two Electronics, two Apparel, two Home Appliances) appear only once.

---

## Task 2: Audience overlap between concerts

**The ask:** a music festival organiser wants to know who attended only one concert, and who attended all three.

```python
concert_a_attendees = {"Alice", "Bob", "Charlie", "Diana"}
concert_b_attendees = {"Bob", "Diana", "Eve", "Frank"}
concert_c_attendees = {"Alice", "George", "Elle", "Frank", "Bob"}

unique_a = concert_a_attendees - (concert_b_attendees | concert_c_attendees)
unique_b = concert_b_attendees - (concert_a_attendees | concert_c_attendees)
unique_c = concert_c_attendees - (concert_a_attendees | concert_b_attendees)

common_all = concert_a_attendees & concert_b_attendees & concert_c_attendees
```

**Result:**

| Group | Attendees |
| --- | --- |
| Concert A only | Charlie |
| Concert B only | Eve |
| Concert C only | George, Elle |
| All three concerts | Bob |

**Key takeaway:** set operators can be combined. "Only in A" means A minus *everyone else*, so the other two concerts are joined with `|` first and then subtracted with `-`. `&` finds the people common to all three.

---

## Task 3: Days above 70°F

**The ask:** a client tracking a month of daily temperatures wants the readings above 70°F.

```python
daily_temperatures = [68, 71, 74, 69, 70, 71, 68, 73, 72, 71, 70, 74, 72, 68]

filtered_temperatures = [temp for temp in daily_temperatures if temp > 70]
```

**Result:** `[71, 74, 71, 73, 72, 71, 74, 72]`, so 8 of the 14 readings are above 70°F.

**Key takeaway:** a list comprehension with an `if` replaces a loop, a condition and `append()` in one line. A list keeps every value and the original order.

---

## Task 4: Unique temperatures

**The ask:** find the distinct temperature values, using a set comprehension.

```python
unique_temperatures = {temp for temp in filtered_temperatures}
```

**Result:** `{71, 72, 73, 74}`, the distinct values among the readings above 70°F.

**Key takeaway:** the same comprehension pattern works for sets. Changing the square brackets `[...]` to curly braces `{...}` removes the duplicates.

---

## Task 5: How often each temperature was recorded

**The ask:** count how many times each temperature was recorded, using a dictionary comprehension.

```python
temperature_count = {temp: filtered_temperatures.count(temp) for temp in unique_temperatures}
```

**Result:** `{72: 2, 73: 1, 74: 2, 71: 3}`. 71°F was the most frequent reading above 70°F, recorded 3 times.

**Key takeaway:** a dictionary comprehension builds `key: value` pairs in one line. Looping over the *unique* values (from Task 4) and counting each in the full list gives a frequency table.

---

## Task 6: Posts with more than 100 likes

**The ask:** a social media client wants the posts that got more than 100 likes.

```python
posts = [
    {"content": "Loving the sunny weather today! #sunny #happy", "likes": 120},
    {"content": "Nothing beats a beach day. #beachday #sunny", "likes": 350},
    {"content": "A rainy day at home. #rainy #lazyday", "likes": 75},
    {"content": "Best coffee in town. #coffeelove #morning", "likes": 180},
    {"content": "Can't wait for the weekend. #weekend #party", "likes": 90},
]

popular_posts = [post["content"] for post in posts if post["likes"] > 100]

print("Popular Posts (Likes > 100):")
for post in popular_posts:
    print(f"- '{post}'")
```

**Result:** 3 of the 5 posts: the sunny weather post, the beach day post and the coffee post.

**Key takeaway:** a comprehension can filter on one field (`likes`) and keep a different one (`content`) in the same line.

---

## Task 7: Unique hashtags in popular posts

**The ask:** list every unique hashtag used in the popular posts.

```python
hashtags = set(tag for post in popular_posts for tag in post.split() if tag.startswith("#"))
```

**Result:** `{'#beachday', '#coffeelove', '#happy', '#morning', '#sunny'}`, 5 unique hashtags.

**Key takeaway:** comprehensions can be nested. The `for` clauses read left to right, like nested loops: for each post, for each word in it, keep the words that start with `#`. Wrapping the result in `set()` removes the repeated `#sunny`.

---

## Task 8: How often each hashtag appears

**The ask:** count how often each hashtag appears across the popular posts, using a dictionary comprehension.

```python
hashtag_frequency = {tag: sum(tag in post for post in popular_posts) for tag in hashtags}
```

**Result:** `{'#sunny': 2, '#beachday': 1, '#morning': 1, '#happy': 1, '#coffeelove': 1}`. `#sunny` is the most used hashtag.

**Key takeaway:** `tag in post` gives `True` or `False`, and Python counts `True` as 1. So `sum()` over those checks gives the number of posts that use each hashtag.

---

## Overall

| Tool | Best for | Used in |
| --- | --- | --- |
| Set comprehension `{x for ...}` | Unique values | Tasks 1, 4, 7 |
| Set operators `-`, `\|`, `&` | Comparing groups | Task 2 |
| List comprehension `[x for ... if ...]` | Filtering, keeping every value and the order | Tasks 3, 6 |
| Dictionary comprehension `{k: v for ...}` | Counts and lookups | Tasks 5, 8 |

The assignment showed how much a single line can do. Each task would normally take a loop, a condition and a few lines of setup, and comprehensions and set operators fold all of that into one readable expression.
