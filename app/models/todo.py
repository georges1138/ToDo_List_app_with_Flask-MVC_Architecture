from datetime import datetime, timezone
from models import db


def utc_now():
    return datetime.now(timezone.utc)


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

    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    completed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
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
