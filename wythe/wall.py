from wythe.bond import course_pieces, face_height_mm, face_length_mm, mortar_length_mm, tally
from wythe.validate import validate_wall


class PlanError(Exception):
    def __init__(self, errors: list[str]) -> None:
        super().__init__("\n".join(errors))
        self.errors = errors


def plan_wall(wall: object) -> dict:
    errors = validate_wall(wall)
    if errors:
        raise PlanError(errors)
    assert isinstance(wall, dict)
    modules = wall["modules"]
    courses = wall["courses"]
    bond = wall.get("bond") or "running"
    courses_of_pieces = [course_pieces(modules, index, bond) for index in range(courses)]
    counts = tally(courses_of_pieces)
    return {
        "name": wall["name"].strip(),
        "bond": bond,
        "modules": modules,
        "courses": courses,
        "faceLengthMm": face_length_mm(modules),
        "faceHeightMm": face_height_mm(courses),
        "bricks": counts["bricks"],
        "stretchers": counts["stretchers"],
        "headers": counts["headers"],
        "closers": counts["closers"],
        "mortarLengthMm": mortar_length_mm(modules, courses, bond),
        "coursesOfPieces": courses_of_pieces,
    }
