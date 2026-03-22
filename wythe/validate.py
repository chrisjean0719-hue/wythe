from wythe.bond import BONDS
from wythe.bricks import MAX_COURSES, MAX_MODULES, MIN_COURSES, MIN_MODULES


def validate_wall(wall: object) -> list[str]:
    """Return a list of problems. An empty list means the wall can be planned."""
    if not isinstance(wall, dict):
        return ["wall: Wall must be an object"]
    errors: list[str] = []
    name = wall.get("name")
    if not isinstance(name, str) or name.strip() == "":
        errors.append("name: Wall needs a name")
    if not _in_range(wall.get("modules"), MIN_MODULES, MAX_MODULES):
        errors.append(f"modules: modules must be an integer from {MIN_MODULES} to {MAX_MODULES}")
    if not _in_range(wall.get("courses"), MIN_COURSES, MAX_COURSES):
        errors.append(f"courses: courses must be an integer from {MIN_COURSES} to {MAX_COURSES}")
    bond = wall.get("bond", "running")
    if bond is None:
        bond = "running"
    if bond not in BONDS:
        errors.append("bond: bond must be running, stack, or flemish")
    errors.extend(_opening_errors(wall.get("opening"), wall.get("modules"), wall.get("courses")))
    return errors


def _opening_errors(opening: object, modules: object, courses: object) -> list[str]:
    if opening is None:
        return []
    if not isinstance(opening, dict):
        return ["opening: opening must be an object"]
    fields = ("module", "width", "course", "height")
    present = [field for field in fields if opening.get(field) is not None]
    if not present:
        return []
    if len(present) < len(fields):
        return ["opening: set module, width, course, and height, or leave the opening empty"]
    errors: list[str] = []
    for field in fields:
        value = opening[field]
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            errors.append(f"opening.{field}: opening.{field} must be a positive integer")
    if errors:
        return errors
    module = opening["module"]
    width = opening["width"]
    course = opening["course"]
    height = opening["height"]
    if isinstance(modules, int) and not isinstance(modules, bool) and module + width - 1 > modules:
        errors.append("opening.width: the opening must stay inside the wall length")
    if isinstance(courses, int) and not isinstance(courses, bool) and course + height - 1 > courses:
        errors.append("opening.height: the opening must stay inside the wall height")
    return errors


def _in_range(value: object, low: int, high: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and low <= value <= high
