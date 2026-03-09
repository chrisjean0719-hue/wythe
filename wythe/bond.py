from wythe.bricks import BRICK_HEIGHT_MM, BRICK_LENGTH_MM, CLOSER_MM, JOINT_MM, MODULE_MM

Piece = dict


def stretcher() -> Piece:
    return {"kind": "stretcher", "widthMm": BRICK_LENGTH_MM}


def closer() -> Piece:
    return {"kind": "closer", "widthMm": CLOSER_MM}


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


def tally(courses: list[list[Piece]]) -> dict:
    stretchers = 0
    closers = 0
    for course in courses:
        for piece in course:
            if piece["kind"] == "stretcher":
                stretchers += 1
            elif piece["kind"] == "closer":
                closers += 1
    return {
        "stretchers": stretchers,
        "closers": closers,
        "headers": 0,
        "bricks": stretchers + closers // 2,
    }


def mortar_length_mm(modules: int, courses: int) -> int:
    beds = (courses - 1) * face_length_mm(modules)
    perpends = 0
    for course in range(courses):
        perpends += (len(running_course(modules, course)) - 1) * BRICK_HEIGHT_MM
    return beds + perpends
