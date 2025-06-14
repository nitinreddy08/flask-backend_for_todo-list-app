# app/models/task_model.py

from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    priority = db.Column(db.String(20), nullable=False, default="medium")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author": self.author.username
        }

    def __repr__(self):
        return f'<Task {self.name}>'



















# tasks = {
#     1: {
#         "name": "Sample Task",
#         "description": "Do something useful",
#         "status": "pending"
#     }
# }
# task_id_counter = 2  # simulate auto-increment


# def get_all_tasks():
#     return tasks


# def get_task(task_id):
#     return tasks.get(task_id)


# def create_task(data):
#     global task_id_counter
#     tasks[task_id_counter] = data
#     task_id_counter += 1
#     return tasks[task_id_counter - 1]


# def update_task(task_id, data):
#     if task_id in tasks:
#         tasks[task_id].update(data)
#         return tasks[task_id]
#     return None

# def remove_task(task_id):
#     if task_id in tasks:
#         deleted  = tasks.pop(task_id)
#         return deleted
#     return None