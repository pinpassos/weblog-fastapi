from http import HTTPStatus


def test_api_healthceck(client):
    """Ensure that app is available."""
    response = client.get("/healthcheck")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": HTTPStatus.OK}
