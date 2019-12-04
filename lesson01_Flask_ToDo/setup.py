#!/usr/bin/env python3

# Russell Felts
# Flask To Do Activity 01

""" Scripts to run to set up our database """

from datetime import datetime

from passlib.hash import pbkdf2_sha256

from model import DB, User, Task

# Create the database tables for our model
DB.connect()
DB.drop_tables([User, Task])
DB.create_tables([User, Task])

Task(name="Do the laundry.").save()
Task(name="Do the dishes.", performed=datetime.now()).save()

User(name="admin", password=pbkdf2_sha256.hash("password")).save()
User(name="bob", password=pbkdf2_sha256.hash("bobbob")).save()
