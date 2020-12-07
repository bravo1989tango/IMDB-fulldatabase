import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))  # this connects to a database either on Heroku or on localhost


class Imdbuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String, unique=True)


class Filmadatb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cim = db.Column(db.String)
    leiras = db.Column(db.String)
    link = db.Column(db.String, unique=True)