# Python Inheritance: My Lecture 12 Notes

*Oct 28, 2026 · Saurabh S*

> [!NOTE]
> **Source:** These notes are based on the **Inheritance** lecture from the **CodeBasics Python course**.

## Where I started

The lecture opened with two classes, `TennisPlayer` and `CricketPlayer`, that repeated the same code: name, birth year and `get_age()`, copied word for word. Inheritance fixes this. The shared parts go into a parent class, `Player`, and each sport only adds what is unique to it. It reminded me of a firm's audit methodology: one core program that applies everywhere, plus extra procedures for each industry.

## What I learnt

**Parent and child classes.** A child class inherits everything from its parent, then adds its own extras.

```python
class Player:                                    # parent: what every player has
    def __init__(self, fname, lname, birth_year):
        self.first_name = fname
        self.last_name = lname
        self.birth_year = birth_year

    def get_age(self):
        return datetime.datetime.now().year - self.birth_year


class CricketPlayer(Player):                     # child: (Player) means "inherits from"
    def __init__(self, fname, lname, team, birth_year):
        super().__init__(fname, lname, birth_year)   # let the parent set up the shared parts
        self.team = team
        self.scores = []
```

**Key ideas:**

| Term | Meaning |
| --- | --- |
| Parent (base) class | Holds the shared attributes and methods (`Player`) |
| Child (derived) class | Inherits from the parent and adds its own (`CricketPlayer`, `TennisPlayer`) |
| `class Child(Parent)` | The syntax for inheriting |
| `super().__init__(...)` | Calls the parent's setup, so the shared code isn't repeated |

`virat.get_age()` works even though `CricketPlayer` never defines `get_age()`. Python finds it in `Player`.

**Why it matters:** in `no_inheritance.py`, `get_age()` was written twice. With inheritance, it's written once, so a fix in `Player` reaches every sport automatically.

One thing I spotted: the `TennisPlayer` in `inheritance.py` lost the `add_ace()` method it had in `no_inheritance.py`, so Roger has no way to record aces. The refactor removed duplicate code, but it also dropped a feature. That's a good reminder to check that nothing gets lost when restructuring code.

## How this shows up in insurance audit work

Every claim shares basics like the claim ID, amount and sum insured. Each line of business then has its own rules. That maps neatly onto parent and child classes.

**1. A base `Claim` class with motor and health versions.**

```python
class Claim:
    def __init__(self, claim_id, amount, sum_insured):
        self.claim_id = claim_id
        self.amount = amount
        self.sum_insured = sum_insured

    def exceeds_sum_insured(self):               # shared check: every claim gets it
        return self.amount > self.sum_insured


class MotorClaim(Claim):
    def __init__(self, claim_id, amount, sum_insured, vehicle_value):
        super().__init__(claim_id, amount, sum_insured)
        self.vehicle_value = vehicle_value

    def is_total_loss(self):                     # motor-only rule
        return self.amount >= 0.75 * self.vehicle_value


class HealthClaim(Claim):
    def __init__(self, claim_id, amount, sum_insured, room_rent, room_rent_cap):
        super().__init__(claim_id, amount, sum_insured)
        self.room_rent = room_rent
        self.room_rent_cap = room_rent_cap

    def room_rent_breached(self):                # health-only rule
        return self.room_rent > self.room_rent_cap
```

**2. Shared and specific checks working together.**

```python
motor = MotorClaim("MC-01", 480000, 600000, 600000)
health = HealthClaim("HC-01", 320000, 300000, 9000, 5000)

print(motor.exceeds_sum_insured(), motor.is_total_loss())         # False True
print(health.exceeds_sum_insured(), health.room_rent_breached())  # True True
```

Both claim types get `exceeds_sum_insured()` from the parent, without repeating it.

**3. One test across every claim type.** Because every claim inherits from `Claim`, a single loop can test a mixed population.

```python
for claim in [motor, health]:
    if claim.exceeds_sum_insured():
        print(f"{claim.claim_id}: paid above the sum insured")   # HC-01
```

## My reflection

Inheritance felt like the biggest step in thinking so far. It's less about new syntax and more about organising rules sensibly. Firm-wide checks belong in the parent class, and line-specific checks belong in the child classes. When the firm-wide rule changes, I update it once. The missing `add_ace()` was a useful lesson too: when you restructure anything, whether code or an audit program, confirm that the new version still does everything the old one did.
