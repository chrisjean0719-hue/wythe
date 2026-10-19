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
    turned = client.post(
        "/walls",
        json={"name": "Sample garden wall", "modules": 10, "courses": 8, "corner": {"end": "right", "modules": 4}},
    )
    assert turned.status_code == 200
    assert turned.json()["bricks"] == 112
    assert turned.json()["returnFaceLengthMm"] == 790
    assert turned.json()["mortarLengthMm"] == 25844
    elevation = client.get("/sample/elevation")
    assert elevation.status_code == 200
    assert elevation.headers["content-type"].startswith("image/svg+xml")
    assert 'filename="sample-garden-wall-elevation.svg"' in elevation.headers["content-disposition"]
    assert 'viewBox="0 0 1990 542"' in elevation.text
    bad = client.post("/walls/elevation", json={"name": " ", "modules": 0, "courses": 40})
    assert bad.status_code == 400
    assert "name: Wall needs a name" in bad.json()["errors"]
    compared = client.post(
        "/walls/compare",
        json={
            "left": {"name": "Sample garden wall", "modules": 10, "courses": 8},
            "right": {"name": "Boundary wall", "modules": 10, "courses": 8, "bond": "flemish"},
        },
    )
    assert compared.status_code == 200
    assert compared.json()["bricks"] == [80, 108]
    assert compared.json()["mortarLengthMm"] == [18262, 19630]
    assert compared.json()["text"].startswith("Sample garden wall vs Boundary wall")
    rejected = client.post(
        "/walls/compare",
        json={
            "left": {"name": " ", "modules": 10, "courses": 8},
            "right": {"name": "Boundary wall", "modules": 0, "courses": 8, "bond": "flemish"},
        },
    )
    assert rejected.status_code == 400
    assert "left.name: Wall needs a name" in rejected.json()["errors"]
    assert any(error.startswith("right.modules:") for error in rejected.json()["errors"])
