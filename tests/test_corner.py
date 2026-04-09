from wythe.format import format_plan
from wythe.validate import validate_wall
from wythe.wall import plan_wall

SAMPLE = {"name": "Sample garden wall", "modules": 10, "courses": 8, "bond": "running"}


def test_a_right_return_adds_its_bricks_and_the_joint_at_the_corner():
    solid = plan_wall(SAMPLE)
    turned = plan_wall({**SAMPLE, "corner": {"end": "right", "modules": 4}})
    assert turned["bricks"] - solid["bricks"] == 32
    assert turned["stretchers"] - solid["stretchers"] == 28
    assert turned["closers"] - solid["closers"] == 8
    assert turned["headers"] == 0
    assert turned["returnFaceLengthMm"] == 790
    assert turned["faceLengthMm"] == solid["faceLengthMm"]
    assert len(turned["returnCourses"]) == 8
    assert len(turned["returnCourses"][0]) == 4
    assert turned["mortarLengthMm"] - solid["mortarLengthMm"] == 7126 + 8 * 57
    text = format_plan(turned)
    assert "corner: right, 4 modules" in text
    assert "return face: 790 mm" in text
    assert "corner: none" in format_plan(solid)


def test_the_same_return_can_sit_on_the_left_and_a_half_set_corner_is_rejected():
    right = plan_wall({**SAMPLE, "corner": {"end": "right", "modules": 4}})
    left = plan_wall({**SAMPLE, "corner": {"end": "left", "modules": 4}})
    assert left["bricks"] == right["bricks"]
    assert left["mortarLengthMm"] == right["mortarLengthMm"]
    assert left["corner"] == {"end": "left", "modules": 4}
    assert "corner: set the end and the modules, or leave the corner empty" in validate_wall(
        {**SAMPLE, "corner": {"end": "right"}}
    )
    assert "corner.end: corner end must be left or right" in validate_wall({**SAMPLE, "corner": {"end": "both", "modules": 2}})
