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
    rejected = client.post("/walls", json={"name": "Sample garden wall", "modules": 10, "courses": 8, "bond": "english"})
    assert rejected.status_code == 400
    assert "bond: bond must be running, stack, or flemish" in rejected.json()["errors"]
    flemish = client.post(
        "/walls",
        json={"name": "Boundary wall", "modules": 10, "courses": 8, "bond": "flemish"},
    )
    assert flemish.status_code == 200
    assert flemish.json()["bricks"] == 108
    assert flemish.json()["mortarLengthMm"] == 19630
    opened = client.post(
        "/walls",
        json={
            "name": "Sample garden wall",
            "modules": 10,
            "courses": 8,
            "bond": "stack",
            "opening": {"module": 3, "width": 2, "course": 2, "height": 3},
        },
    )
    assert opened.status_code == 200
    assert opened.json()["bricks"] == 74
    assert opened.json()["opening"]["course"] == 2
    partial = client.post(
        "/walls",
        json={"name": "Sample garden wall", "modules": 10, "courses": 8, "opening": {"module": 3}},
    )
    assert partial.status_code == 400
    assert partial.json()["errors"] == ["opening: set module, width, course, and height, or leave the opening empty"]
