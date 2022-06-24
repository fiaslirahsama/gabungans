from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app_hospital import db

# This file work for define and initialize model for the database.

class auth(UserMixin, db.Model):
    id_auth = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_auth = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(99), nullable=False)
    password = db.Column(db.String(99), nullable=False)
    flag = db.Column(db.String(2), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, status_auth, username, password, flag, created_date, updated_date):
        self.status_auth = status_auth
        self.username = username
        self.password = password
        self.flag = flag
        self.created_date = created_date
        self.updated_date = updated_date
    
    def __repr__(self):
        return '<auth %r>' % self.id_auth

    def get_id(self):
        return self.id_auth