from wythe.bricks import BRICK_HEIGHT_MM, BRICK_LENGTH_MM, CLOSER_MM, HEADER_MM, JOINT_MM, MODULE_MM

Piece = dict
BONDS = ("running", "stack", "flemish")


def stretcher() -> Piece:
    return {"kind": "stretcher", "widthMm": BRICK_LENGTH_MM}


def closer() -> Piece:
    return {"kind": "closer", "widthMm": CLOSER_MM}


def header() -> Piece:
    return {"kind": "header", "widthMm": HEADER_MM}


def face_length_mm(modules: int) -> int:
    """Face length of the wall. Joints sit between bricks, not past the ends."""
    return modules * MODULE_MM - JOINT_MM


def face_height_mm(courses: int) -> int:
    return courses * BRICK_HEIGHT_MM + (courses - 1) * JOINT_MM


def running_course(modules: int, course_index: int) -> list[Piece]:
    if course_index % 2 == 0:
        return [stretcher() for _ in range(modules)]
    stretchers = max(0, modules - 1)
    return [closer(), *[stretcher() for _ in range(stretchers)], closer()]


def flemish_course(modules: int, course_index: int) -> list[Piece]:
    slots = modules * 2
    pieces: list[Piece] = []
    prefer_header = course_index % 2 == 1
    while slots > 0:
        if not prefer_header and slots >= 2:
            pieces.append(stretcher())
            slots -= 2
        else:
            pieces.append(header())
            slots -= 1
        prefer_header = not prefer_header
    return pieces


def course_pieces(modules: int, course_index: int, bond: str = "running") -> list[Piece]:
    if bond == "stack":
        return [stretcher() for _ in range(modules)]
    if bond == "flemish":
        return flemish_course(modules, course_index)
    return running_course(modules, course_index)


def course_width_mm(pieces: list[Piece]) -> int:
    if not pieces:
        return 0
    return sum(piece["widthMm"] for piece in pieces) + (len(pieces) - 1) * JOINT_MM


def tally(courses: list[list[Piece]]) -> dict:
    stretchers = 0
    closers = 0
    headers = 0
    for course in courses:
        for piece in course:
            if piece["kind"] == "stretcher":
                stretchers += 1
            elif piece["kind"] == "closer":
                closers += 1
            elif piece["kind"] == "header":
                headers += 1
    return {
        "stretchers": stretchers,
        "closers": closers,
        "headers": headers,
        "bricks": stretchers + headers + closers // 2,
    }


def mortar_length_mm(modules: int, courses: int, bond: str = "running") -> int:
    beds = (courses - 1) * face_length_mm(modules)
    perpends = 0
    for course in range(courses):
        perpends += (len(course_pieces(modules, course, bond)) - 1) * BRICK_HEIGHT_MM
    return beds + perpends
