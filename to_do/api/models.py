from to_do import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    tasks = db.relationship('Task', backref='owner')


    def __repr__(self):
        return f'User{self.first_name}{self.email}'





today =datetime.today()
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    due_date = db.Column(db.DateTime(),default=datetime.utcnow)
    status = db.Column(db.String(255))
    todo_owner = db.Column(db.Integer,db.ForeignKey('user.id'))


    def __repr__(self):
        return f'Task{self.task_name}{self.due_date}'