# Python Classes and Objects: My Lecture 11 Notes

*Oct 28, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Classes and Objects** lecture from the **CodeBasics Python course**.

## Where I started

The lecture solved the same problem twice. First, without a class: each cricket player was a dictionary, and separate functions like `get_age(player)` worked on it. That works, but the data and the functions that use it are scattered. Then it used a class, where the data and the actions on it live together in one place. It felt like moving from loose working papers to a properly bound audit file.

## What I learnt

**A class is a blueprint, and an object is one thing built from it.** `CricketPlayer` is the blueprint, and `virat` and `david` are objects.

```python
class CricketPlayer:
    team_size = 11                       # class attribute, shared by every player

    def __init__(self, fname, lname, birth_year, team):
        self.first_name = fname          # instance attributes, specific to each player
        self.birth_year = birth_year
        self.scores = []

    def add_score(self, score):          # a method: a function that belongs to the class
        self.scores.append(score)

virat = CricketPlayer('virat', 'kohli', 1988, 'India')
virat.add_score(100)
```

**Key ideas:**

| Term | Meaning |
| --- | --- |
| `__init__` | Runs automatically when an object is created and sets its starting data |
| `self` | The object itself, so `self.scores` means *this* player's scores |
| Instance attribute | Data belonging to one object (`self.birth_year`) |
| Class attribute | Data shared by all objects (`team_size = 11`) |
| Method | A function defined inside the class (`get_average_score()`) |

**Special (dunder) methods** teach Python how my objects should behave:

- `__str__` controls what `print(virat)` shows: `virat kohli, the cricket player from India`.
- `__lt__` defines `<`. The lecture compared players by average score: Virat averaged 53.3 and David 48.3, so `virat < david` was `False`.
- `__eq__` defines `==`. The lecture compared players by **age**, so two players born in 1988 count as "equal". That's legal, but surprising, so I'll make sure `==` means something sensible in my own classes.

The lecture also used the `datetime` module to work out each player's age from the current year.

## How this shows up in insurance audit work

Claims and policies are natural objects: each has its own data (amount, limit, adjuster) and its own checks. These snippets build them as classes.

**1. A `Claim` class with its own audit checks.**

```python
class Claim:
    authority_limit = 50000                      # one firm-wide rule, shared by every claim

    def __init__(self, claim_id, policy, amount, sum_insured):
        self.claim_id = claim_id
        self.policy = policy
        self.amount = amount
        self.sum_insured = sum_insured

    def exceeds_sum_insured(self):
        return self.amount > self.sum_insured

    def needs_escalation(self):
        return self.amount > Claim.authority_limit

    def __str__(self):
        return f"{self.claim_id} on {self.policy}: {self.amount}"

    def __lt__(self, other):                     # lets Python sort claims by amount
        return self.amount < other.amount


c1 = Claim("CL-01", "P101", 42000, 50000)
c2 = Claim("CL-02", "P102", 260000, 250000)
print(c2, c2.exceeds_sum_insured(), c2.needs_escalation())   # CL-02 on P102: 260000 True True
```

**2. Sorting claims for high-value testing.** Because of `__lt__`, `sorted()` knows how to order claims.

```python
c3 = Claim("CL-03", "P103", 95000, 100000)
for claim in sorted([c1, c2, c3], reverse=True):
    print(claim)          # largest first: CL-02, CL-03, CL-01
```

**3. A `Policy` that holds its own claims.** The policy works out its own loss ratio.

```python
class Policy:
    def __init__(self, policy_id, premium):
        self.policy_id = policy_id
        self.premium = premium
        self.claims = []

    def add_claim(self, claim):
        self.claims.append(claim)

    def loss_ratio(self):
        total = 0
        for claim in self.claims:
            total += claim.amount
        return round(total / self.premium * 100, 1)


p = Policy("P101", 60000)
p.add_claim(Claim("CL-04", "P101", 30000, 50000))
p.add_claim(Claim("CL-05", "P101", 45000, 50000))
print(p.loss_ratio())   # 125.0: claims exceed premium
```

## My reflection

Classes made me think about how I already organise audit work. Each claim file holds its facts, and every claim gets the same checks. A class puts that structure into code: the rules live in one place, and changing `authority_limit` once updates the check for every claim. The `__eq__`-by-age example was also a useful warning. Code can define "equal" any way it likes, so in audit I'll always check *what* is being compared, not just the result.

Next, I want to practise:

- [ ] Build a `Claim` class and load a few claims from a CSV into objects
- [ ] Add a `__str__` so each claim prints as a readable working-paper line
- [ ] Give the `Policy` class a method that lists every claim needing escalation
