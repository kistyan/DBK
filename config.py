import sqlite3
from peewee import *
from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db = SqliteDatabase('ebibl.db')


class BaseModel(Model):
    class Meta:
        database = db
