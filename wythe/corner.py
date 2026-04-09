from wythe.bond import course_pieces, face_length_mm, mortar_length_mm
from wythe.bricks import BRICK_HEIGHT_MM, HEADER_MM

QUOIN_MM = HEADER_MM


def return_courses(modules: int, courses: int, bond: str) -> list[list[dict]]:
    return [course_pieces(modules, index, bond) for index in range(courses)]


def return_face_length_mm(modules: int) -> int:
    return face_length_mm(modules)


def return_mortar_length_mm(modules: int, courses: int, bond: str) -> int:
    """Mortar in the return, plus the vertical joint where it meets the corner brick."""
    return mortar_length_mm(modules, courses, bond) + courses * BRICK_HEIGHT_MM
