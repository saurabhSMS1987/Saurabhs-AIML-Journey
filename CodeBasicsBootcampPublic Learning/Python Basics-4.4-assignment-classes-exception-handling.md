# Assignment 4: Classes, Inheritance and Exception Handling

*Oct 28, 2026 · Saurabh S*

> [!NOTE]
> **Source:** Assignment from the **CodeBasics Python course**, covering the Classes, Inheritance and Exception Handling lectures.

As Peter Pandey, I helped Celina, the librarian at AtliQ, automate borrowing and returns for the company's internal library.

## Tasks at a glance

| Task | What I did | Result |
| --- | --- | --- |
| 1 | Built a `LibraryItem` class with `title`, `is_borrowed`, `borrow_item()` and `return_item()` | Raises an exception for an invalid borrow or return |
| 2 | Created a `Book` child class with an `author` | *The Magic of Thinking Big* by David Schwartz |
| 3 | Created a `Journal` child class with an `issue_number` | *Nature*, issue 50 |
| 4 | Borrowed the same book twice and caught the error | `The item 'The Magic of Thinking Big' is already borrowed.` |
| 5 | Returned a journal that was never borrowed and caught the error | `The item 'Nature' is not borrowed.` |

## Final code

```python
class LibraryItem:
    def __init__(self, title):
        self.title = title
        self.is_borrowed = False

    def borrow_item(self):
        if self.is_borrowed:
            raise Exception(f"The item '{self.title}' is already borrowed.")
        self.is_borrowed = True
        print(f"{self.title} has been borrowed.")

    def return_item(self):
        if not self.is_borrowed:
            raise Exception(f"The item '{self.title}' is not borrowed.")
        self.is_borrowed = False
        print(f"{self.title} has been returned.")


class Book(LibraryItem):
    def __init__(self, title, author):
        super().__init__(title)
        self.author = author


class Journal(LibraryItem):
    def __init__(self, title, issue_number):
        super().__init__(title)
        self.issue_number = issue_number


book = Book("The Magic of Thinking Big", "David Schwartz")
journal = Journal("Nature", 50)

try:                                   # Task 4
    book.borrow_item()
    book.borrow_item()
except Exception as e:
    print(e)

try:                                   # Task 5
    journal.return_item()
except Exception as e:
    print(e)
```

Output:

```
The Magic of Thinking Big has been borrowed.
The item 'The Magic of Thinking Big' is already borrowed.
The item 'Nature' is not borrowed.
```

## Where my version differs from the solution

- **Method name:** the task asks for `borrow_item()`, but the solution calls it `borrow()`. I followed the task.
- **Issue number:** the solution stores `"50"` as text, while the task gives `50`, a number. I used the number, so it can be sorted and compared properly.
- **Title:** I used the task's spelling, *The Magic of Thinking Big*.

## What stuck with me

This assignment brought three lectures together. The parent class holds the shared rules, the child classes add their own details, and exceptions stop invalid actions, such as a double borrow, before they corrupt the records. It's the same pattern as a control: a claim can't be paid twice, and a policy can't be cancelled if it was never issued.
