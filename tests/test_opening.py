import pytest

from wythe.bond import face_length_mm
from wythe.opening import row_width_mm
from wythe.wall import plan_wall

WALL = {"name": "Sample garden wall", "modules": 10, "courses": 8, "bond": "stack"}


def test_a_stack_opening_removes_whole_bricks_and_keeps_the_face_length():
    solid = plan_wall(WALL)
    opened = plan_wall({**WALL, "opening": {"module": 3, "width": 2, "course": 2, "height": 3}})
    assert solid["bricks"] - opened["bricks"] == 6
    assert opened["cuts"] == 0
    assert opened["mortarLengthMm"] == 16701
    assert opened["mortarLengthMm"] < solid["mortarLengthMm"]
    for course in opened["coursesOfPieces"]:
        assert row_width_mm(course) == face_length_mm(10)
    assert not any(piece["kind"] == "opening" for piece in opened["coursesOfPieces"][0])
    assert any(piece["kind"] == "opening" for piece in opened["coursesOfPieces"][1])
    assert opened["opening"] == {"module": 3, "width": 2, "course": 2, "height": 3}


def test_a_partial_opening_is_rejected_and_a_solid_wall_reports_none():
    with pytest.raises(Exception, match="opening:"):
        plan_wall({**WALL, "opening": {"module": 3}})
    solid = plan_wall({"name": "Sample garden wall", "modules": 10, "courses": 8})
    assert solid["bricks"] == 80
    assert solid["mortarLengthMm"] == 18262
    assert solid["opening"] is None
    assert solid["cuts"] == 0
