import os

import pytest

from app import create_app
from models import db


@pytest.fixture
def app():
    test_database_url = os.environ.get("TEST_DATABASE_URL")

    if not test_database_url:
        raise RuntimeError(
            "TEST_DATABASE_URL environment variable is required"
        )

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": test_database_url,
        "SECRET_KEY": "test-secret",
    })

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
