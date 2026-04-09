from wythe.bond import course_pieces, face_height_mm, face_length_mm, tally
from wythe.corner import return_courses, return_face_length_mm, return_mortar_length_mm
from wythe.bricks import BRICK_HEIGHT_MM
from wythe.opening import clip_course, is_cut, opening_span
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
    opening = _complete_opening(wall.get("opening"))
    span = opening_span(opening) if opening else None
    courses_of_pieces = []
    for index in range(courses):
        solid = course_pieces(modules, index, bond)
        course_number = index + 1
        if opening and span and opening["course"] <= course_number < opening["course"] + opening["height"]:
            courses_of_pieces.append(clip_course(solid, span["left"], span["right"]))
        else:
            courses_of_pieces.append(solid)
    corner = _complete_corner(wall.get("corner"))
    turned = return_courses(corner["modules"], courses, bond) if corner else []
    counts = tally(courses_of_pieces)
    extra = tally(turned)
    face = face_length_mm(modules)
    mortar = _mortar_from_rows(courses_of_pieces, face)
    if corner:
        mortar += return_mortar_length_mm(corner["modules"], courses, bond)
    return {
        "name": wall["name"].strip(),
        "bond": bond,
        "modules": modules,
        "courses": courses,
        "faceLengthMm": face,
        "faceHeightMm": face_height_mm(courses),
        "bricks": counts["bricks"] + extra["bricks"],
        "stretchers": counts["stretchers"] + extra["stretchers"],
        "headers": counts["headers"] + extra["headers"],
        "closers": counts["closers"] + extra["closers"],
        "cuts": sum(1 for course in courses_of_pieces for piece in course if is_cut(piece)),
        "opening": opening,
        "corner": corner,
        "returnFaceLengthMm": return_face_length_mm(corner["modules"]) if corner else 0,
        "mortarLengthMm": mortar,
        "coursesOfPieces": courses_of_pieces,
        "returnCourses": turned,
    }


def _complete_corner(corner: object) -> dict | None:
    if not isinstance(corner, dict) or corner.get("end") is None or corner.get("modules") is None:
        return None
    return {"end": corner["end"], "modules": corner["modules"]}


def _complete_opening(opening: object) -> dict | None:
    if not isinstance(opening, dict):
        return None
    fields = ("module", "width", "course", "height")
    if any(opening.get(field) is None for field in fields):
        return None
    return {field: opening[field] for field in fields}


def _mortar_from_rows(rows: list[list[dict]], face: int) -> int:
    length = 0
    for index, row in enumerate(rows):
        for piece_index in range(len(row) - 1):
            if row[piece_index]["kind"] != "opening" and row[piece_index + 1]["kind"] != "opening":
                length += BRICK_HEIGHT_MM
        if index < len(rows) - 1:
            hole = next((piece for piece in row if piece["kind"] == "opening"), None)
            next_hole = next((piece for piece in rows[index + 1] if piece["kind"] == "opening"), None)
            lost = min(hole["widthMm"], next_hole["widthMm"]) if hole and next_hole else 0
            length += face - lost
    return length
