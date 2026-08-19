def test_unknown_api_route_returns_json_404(client):
    response = client.get(
        "/api/v1/does-not-exist"
    )

    assert response.status_code == 404
    assert response.is_json

    data = response.get_json()
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_unknown_non_api_route_still_returns_html(client):
    response = client.get(
        "/does-not-exist"
    )

    assert response.status_code == 404
    assert not response.is_json
    assert "text/html" in response.content_type