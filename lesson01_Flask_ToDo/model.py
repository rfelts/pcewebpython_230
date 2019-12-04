#!/usr/bin/env python3

# Russell Felts
# Flask To Do Activity 01

""" Database Model """

from peewee import Model, CharField, DateTimeField, ForeignKeyField
import os

from playhouse.db_url import connect

DB = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class User(Model):
    """
    User table
    """
    name = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = DB


class Task(Model):
    """
    Task table
    """
    name = CharField(max_length=255)
    performed = DateTimeField(null=True)
    performed_by = ForeignKeyField(model=User, null=True)

    class Meta:
        database = DB
