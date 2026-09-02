from fastapi.testclient import TestClient

from ai_music_open.api import app


def test_openapi_is_available() -> None:
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "AI Music Open API"
