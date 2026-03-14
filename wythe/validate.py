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
    return errors


def _in_range(value: object, low: int, high: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and low <= value <= high
