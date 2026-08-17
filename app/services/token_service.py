import secrets
import hashlib

from datetime import datetime, timezone
from models import db
from models.api_token import ApiToken


def utc_now():
    return datetime.now(timezone.utc)


class TokenService:

    @staticmethod
    def hash_token(raw_token):
        return hashlib.sha256(raw_token.encode()).hexdigest()

    @staticmethod
    def issue_token(user_id, name, expires_at=None):
        raw_token = secrets.token_urlsafe(32)
        token_hash = TokenService.hash_token(raw_token)

        api_token = ApiToken(
            user_id=user_id,
            token_hash=token_hash,
            name=name,
            expires_at=expires_at
        )

        db.session.add(api_token)
        db.session.commit()

        return raw_token, api_token

    @staticmethod
    def resolve_token(raw_token):
        hashed_token = TokenService.hash_token(raw_token)

        stmt = db.select(ApiToken).where(
            ApiToken.token_hash == hashed_token
        )
        result = db.session.execute(
            stmt
        ).scalar_one_or_none()

        now = utc_now()
        if result is None or (result.expires_at and result.expires_at <= now):
            return None

        result.last_used_at = now
        db.session.commit()

        return result