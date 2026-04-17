import shelve

"""
The big difference with pickle is you can grab partial objects from db
"""

data: dict = {
    "a": 1,
    "b": 2,
    "c": 3,
}

with shelve.open("test") as db:
    db["a"] = 1
    db.update(data)
