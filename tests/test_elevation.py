from wythe.elevation import elevation_file_name, elevation_svg
from wythe.wall import plan_wall

SAMPLE = {"name": "Sample garden wall", "modules": 10, "courses": 8, "bond": "running"}


def test_the_sample_elevation_is_an_svg_with_course_1_at_the_bottom():
    svg = elevation_svg(plan_wall(SAMPLE))
    assert svg.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "<title>Sample garden wall</title>" in svg
    assert 'viewBox="0 0 1990 542"' in svg
    assert 'width="1990mm"' in svg
    assert svg.count('fill="#a34432"') == 76
    assert svg.count('fill="#8c3a2c"') == 8
    assert 'x="0" y="485" width="190" height="57" fill="#a34432"' in svg
    assert 'x="0" y="418" width="90" height="57" fill="#8c3a2c"' in svg
    assert elevation_file_name(SAMPLE["name"]) == "sample-garden-wall-elevation.svg"


def test_an_opening_and_a_right_return_are_both_in_the_file():
    opened = elevation_svg(
        plan_wall({**SAMPLE, "bond": "stack", "opening": {"module": 3, "width": 2, "course": 2, "height": 3}})
    )
    assert opened.count('fill="#a34432"') == 74
    assert opened.count('fill="#f3efe6"') == 3
    turned = elevation_svg(plan_wall({**SAMPLE, "corner": {"end": "right", "modules": 4}}))
    assert 'viewBox="0 0 2890 542"' in turned
    assert turned.count('fill="#a34432"') == 104
    assert turned.count('fill="#8c3a2c"') == 16
    assert turned.count('fill="#6e5344"') == 8
    assert ">Return</text>" in turned
    left = elevation_svg(plan_wall({**SAMPLE, "corner": {"end": "left", "modules": 4}}))
    assert 'x="900" y="485" width="190" height="57" fill="#a34432"' in left
