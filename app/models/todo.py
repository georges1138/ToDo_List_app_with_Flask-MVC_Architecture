from models import db

class Todo(db.Model):
    __tablename__ = 'todos'

    todo_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description
