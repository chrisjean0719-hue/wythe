import re

from wythe.bricks import BRICK_HEIGHT_MM, JOINT_MM
from wythe.corner import QUOIN_MM

LABEL_BAND = 16
MORTAR = "#d9d2c5"
INK = "#2b241c"
FILL = {
    "stretcher": "#a34432",
    "closer": "#8c3a2c",
    "header": "#6e5344",
    "quoin": "#6e5344",
    "opening": "#f3efe6",
}


def elevation_svg(plan: dict) -> str:
    """The elevation in millimetres. Course 1 is the bottom row."""
    drawing = _drawing(plan)
    rects = [mark for face in drawing["faces"] for course in face["courses"] for mark in course["marks"]]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {drawing["width"]} {drawing["height"]}" '
            f'width="{drawing["width"]}mm" height="{drawing["height"]}mm">'
        ),
        f"  <title>{_escape_xml(plan['name'])}</title>",
        f'  <rect width="{drawing["width"]}" height="{drawing["height"]}" fill="{MORTAR}"/>',
    ]
    for face in drawing["faces"]:
        lines.append(f'  <text x="{face["x"]}" y="12" font-size="11" fill="{INK}">{_escape_xml(face["label"])}</text>')
    for mark in rects:
        stroke = ' stroke="#b7ad9e" stroke-width="1"' if mark["kind"] == "opening" else ""
        lines.append(
            f'  <rect x="{mark["x"]}" y="{mark["y"]}" width="{mark["width"]}" height="{mark["height"]}" '
            f'fill="{FILL[mark["kind"]]}"{stroke}/>'
        )
    lines.append("</svg>")
    lines.append("")
    return "\n".join(lines)


def elevation_file_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return f"{slug or 'wall'}-elevation.svg"


def _drawing(plan: dict) -> dict:
    columns = _face_columns(plan)
    x = 0
    faces = []
    for index, column in enumerate(columns):
        faces.append(
            {
                "label": column["label"],
                "x": x,
                "courses": [
                    {
                        "number": course_index + 1,
                        "marks": _course_marks(pieces, x, plan["courses"], course_index),
                    }
                    for course_index, pieces in enumerate(column["courses"])
                ],
            }
        )
        x += column["width"]
        if index < len(columns) - 1:
            x += JOINT_MM
    return {"width": x, "height": LABEL_BAND + plan["faceHeightMm"], "faces": faces}


def _face_columns(plan: dict) -> list[dict]:
    front = {"label": "Front", "width": plan["faceLengthMm"], "courses": plan["coursesOfPieces"]}
    if not plan["corner"]:
        return [front]
    turned = {"label": "Return", "width": plan["returnFaceLengthMm"], "courses": plan["returnCourses"]}
    corner = {
        "label": "Corner",
        "width": QUOIN_MM,
        "courses": [[{"kind": "quoin", "widthMm": QUOIN_MM}] for _ in range(plan["courses"])],
    }
    if plan["corner"]["end"] == "left":
        return [turned, corner, front]
    return [front, corner, turned]


def _course_marks(pieces: list[dict], origin_x: int, course_count: int, course_index: int) -> list[dict]:
    y = LABEL_BAND + (course_count - 1 - course_index) * (BRICK_HEIGHT_MM + JOINT_MM)
    marks = []
    x = origin_x
    for piece_index, piece in enumerate(pieces):
        marks.append({"kind": piece["kind"], "x": x, "y": y, "width": piece["widthMm"], "height": BRICK_HEIGHT_MM})
        x += piece["widthMm"]
        if piece_index < len(pieces) - 1 and piece["kind"] != "opening" and pieces[piece_index + 1]["kind"] != "opening":
            x += JOINT_MM
    return marks


def _escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
