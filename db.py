from fasthtml.common import database

db = database("data/users.db")

users = db.t.users

if users not in db.t:
    users.create(dict(email=str, password=str), pk="email")
