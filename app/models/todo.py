from models import db

class Todo(db.Model):
    __tablename__ = 'todos'

    todo_id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship(
        'User',
        back_populates='todos'
    )
