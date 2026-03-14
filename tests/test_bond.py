from wythe.bond import BONDS, course_pieces, course_width_mm, face_height_mm, face_length_mm, mortar_length_mm, running_course, tally
from wythe.bricks import CLOSER_MM


def test_even_course_is_stretchers_and_odd_course_starts_with_a_closer():
    even = running_course(10, 0)
    odd = running_course(10, 1)
    assert len(even) == 10
    assert {piece["kind"] for piece in even} == {"stretcher"}
    assert odd[0]["kind"] == "closer"
    assert odd[-1]["kind"] == "closer"
    assert odd[0]["widthMm"] == CLOSER_MM
    assert face_length_mm(10) == 1990
    assert face_height_mm(8) == 526


def test_two_closers_count_as_one_brick():
    courses = [running_course(10, index) for index in range(8)]
    counts = tally(courses)
    assert counts["stretchers"] == 76
    assert counts["closers"] == 8
    assert counts["bricks"] == 80
    assert mortar_length_mm(10, 8) == 18262


def test_every_bond_fills_the_same_face_and_flemish_uses_headers():
    for bond in BONDS:
        for modules in range(1, 11):
            for course in (0, 1):
                assert course_width_mm(course_pieces(modules, course, bond)) == face_length_mm(modules)
    stacked = course_pieces(10, 1, "stack")
    assert {piece["kind"] for piece in stacked} == {"stretcher"}
    assert mortar_length_mm(10, 8, "stack") == 18034
    assert course_pieces(10, 0, "flemish")[0]["kind"] == "stretcher"
    assert course_pieces(10, 0, "flemish")[1]["kind"] == "header"
    assert course_pieces(10, 1, "flemish")[0]["kind"] == "header"
