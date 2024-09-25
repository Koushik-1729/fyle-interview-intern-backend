import pytest
@pytest.fixture
def h_principal():
    return {"X-Principal": '{"teacher_id": 1, "user_id": 3}'}  # Example headers
def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "ready"


def test_invalid_endpoint(client, h_principal):
    response = client.get("/other", headers=h_principal)
    assert response.status_code == 404
    assert response.json["error"] == "NotFound"