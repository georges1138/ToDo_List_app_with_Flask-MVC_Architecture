from datetime import datetime, timezone
from models import db


def utc_now():
    return datetime.now(timezone.utc)


class ApiToken(db.Model):
    __tablename__ = 'api_tokens'

    token_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        nullable=False,
        unique=True,
        index=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    last_used_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    expires_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )
