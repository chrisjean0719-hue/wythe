from fastapi.testclient import TestClient

from wythe.app import app

client = TestClient(app)


def test_the_sample_route_matches_a_posted_wall():
    sample = client.get("/sample")
    posted = client.post("/walls", json={"name": "Sample garden wall", "modules": 10, "courses": 8})
    assert sample.status_code == 200
    assert posted.status_code == 200
    assert posted.json() == sample.json()
    assert posted.json()["bricks"] == 80
    assert posted.json()["mortarLengthMm"] == 18262
    assert client.get("/health").json() == {"status": "ok"}


def test_a_bad_wall_names_the_fields():
    response = client.post("/walls", json={"name": " ", "modules": 0, "courses": 40})
    assert response.status_code == 400
    errors = response.json()["errors"]
    assert "name: Wall needs a name" in errors
    assert any(error.startswith("modules:") for error in errors)
    assert any(error.startswith("courses:") for error in errors)
