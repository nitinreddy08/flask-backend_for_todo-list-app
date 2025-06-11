# app/models/user_model.py

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to the Task model
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'