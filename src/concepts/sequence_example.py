## TypedDict: Defines exactly what keys and value types a dictionary must have.
## Sequence: Defines that you have a collection of those dictionaries.
## This is the standard way to type-hint a "List of Objects," like a JSON response from an API.

from typing import TypedDict, Sequence

# 1. Define the structure of a single dictionary
class User(TypedDict):
    name: str
    age: int
    is_active: bool

# 2. Use Sequence to define a collection of those dictionaries
def process_users(user_list: Sequence[User]):
    for user in user_list:
        status = "Online" if user["is_active"] else "Offline"
        print(f"{user['name']} ({user['age']}) is {status}")



# 3. This is a Sequence (list) of User dictionaries
my_users: Sequence[User] = [
    {"name": "Alice", "age": 30, "is_active": True},
    {"name": "Bob", "age": 25, "is_active": False}
]

process_users(my_users)