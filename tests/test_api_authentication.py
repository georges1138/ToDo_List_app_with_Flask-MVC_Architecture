import pytest
from flask import Flask, g
from unittest.mock import patch, MagicMock

from middlewares.api_authentication import require_api_token


@pytest.fixture
def app():
    test_app = Flask(__name__)
    test_app.testing = True

    @test_app.route("/test-api")
    @require_api_token
    def protected_test_route():
        return {"user_id": g.user_id}

    return test_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_missing_authorization_header(client):
    """Test what happens when no header is sent."""
    response = client.get("/test-api")

    # In Pytest, you just use standard 'assert' statements
    assert response.status_code == 401
    assert response.json["error"] == "Missing or malformed Authorization header"


def test_malformed_authorization_header(client):
    """Test what happens when the header doesn't say 'Bearer'."""
    headers = {"Authorization": "JustSomeRandomString"}
    response = client.get("/test-api", headers=headers)

    assert response.status_code == 401
    assert response.json["error"] == "Missing or malformed Authorization header"


# 3. Mocking the database/token service for a successful test!
@patch("middlewares.api_authentication.TokenService.resolve_token")
def test_successful_authentication(mock_resolve_token, client):
    """Test a valid token login using a mock."""

    # Set up our fake 'resolved' object that the mock will return
    fake_resolved_token = MagicMock()
    fake_resolved_token.user_id = 999
    mock_resolve_token.return_value = fake_resolved_token

    # Make the request with a properly formatted token
    headers = {"Authorization": "Bearer super_secret_valid_token"}
    response = client.get("/test-api", headers=headers)

    mock_resolve_token.assert_called_once_with(
        "super_secret_valid_token"
    )

    # Assert it was successful and returned the mocked user_id!
    assert response.status_code == 200
    assert response.json == {"user_id": 999}


@patch("middlewares.api_authentication.TokenService.resolve_token")
def test_invalid_token(mock_resolve_token, client):
    mock_resolve_token.return_value = None

    response = client.get(
        "/test-api",
        headers={"Authorization": "Bearer bad-token"}
    )

    mock_resolve_token.assert_called_once_with(
        "bad-token"
    )

    assert response.status_code == 401
    assert response.json["error"] == "Invalid or expired token"
