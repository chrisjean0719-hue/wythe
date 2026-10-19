from wythe.compare import compare_walls, format_compare
from wythe.sample import BOUNDARY_WALL, SAMPLE_WALL
from wythe.wall import plan_wall


def test_a_flemish_wall_uses_more_bricks_and_more_mortar_than_the_running_sample():
    left = plan_wall(SAMPLE_WALL)
    right = plan_wall(BOUNDARY_WALL)
    diff = compare_walls(left, right)
    assert diff == {"bricks": [80, 108], "mortarLengthMm": [18262, 19630]}
    assert format_compare(left, right, diff) == "\n".join(
        [
            "Sample garden wall vs Boundary wall",
            "bricks: 80 vs 108",
            "mortar: 18262 mm vs 19630 mm",
        ]
    )


def test_a_return_is_included_in_the_brick_count_being_compared():
    left = plan_wall(SAMPLE_WALL)
    right = plan_wall({**SAMPLE_WALL, "name": "Turned wall", "corner": {"end": "right", "modules": 4}})
    assert compare_walls(left, right)["bricks"] == [80, 112]
