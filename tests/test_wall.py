import pytest

from wythe.format import format_plan
from wythe.sample import SAMPLE_WALL
from wythe.validate import validate_wall
from wythe.wall import PlanError, plan_wall


def test_the_sample_plan():
    plan = plan_wall(SAMPLE_WALL)
    assert plan["stretchers"] == 76
    assert plan["closers"] == 8
    assert plan["headers"] == 0
    assert len(plan["coursesOfPieces"]) == 8
    assert plan["coursesOfPieces"][0][0]["kind"] == "stretcher"
    text = format_plan(plan)
    assert "running bond" in text
    assert "face: 1990 mm wide, 526 mm high" in text
    assert "mortar: 18262 mm" in text


def test_bad_fields_are_named_and_a_list_is_rejected():
    assert validate_wall([]) == ["wall: Wall must be an object"]
    errors = validate_wall({"name": "  ", "modules": 0, "courses": 40})
    assert "name: Wall needs a name" in errors
    assert any(error.startswith("modules:") for error in errors)
    assert any(error.startswith("courses:") for error in errors)
    with pytest.raises(PlanError):
        plan_wall({**SAMPLE_WALL, "modules": 31})
    assert validate_wall({**SAMPLE_WALL, "bond": "english"}) == ["bond: bond must be running, stack, or flemish"]
    flemish = plan_wall({**SAMPLE_WALL, "bond": "flemish"})
    assert flemish["bricks"] == 108
    assert flemish["headers"] == 56
    assert flemish["closers"] == 0
    assert flemish["faceLengthMm"] == plan_wall(SAMPLE_WALL)["faceLengthMm"]
    assert flemish["mortarLengthMm"] == 19630
