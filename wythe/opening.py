from wythe.bricks import BRICK_LENGTH_MM, CLOSER_MM, HEADER_MM, JOINT_MM, MODULE_MM

Piece = dict


def opening_span(opening: dict) -> dict:
    left = (opening["module"] - 1) * MODULE_MM
    return {"left": left, "right": left + opening["width"] * MODULE_MM - JOINT_MM}


def clip_course(pieces: list[Piece], left: int, right: int) -> list[Piece]:
    kept: list[tuple[int, int, Piece]] = []
    x = 0
    for index, piece in enumerate(pieces):
        start = x
        end = x + piece["widthMm"]
        if end <= left or start >= right:
            kept.append((start, end, piece))
        else:
            if start < left:
                kept.append((start, left, {**piece, "widthMm": left - start}))
            if end > right:
                kept.append((right, end, {**piece, "widthMm": end - right}))
        x = end
        if index < len(pieces) - 1:
            x += JOINT_MM

    face_end = x
    out: list[Piece] = []
    cursor = 0
    for start, end, piece in kept:
        if start - cursor > JOINT_MM:
            out.append({"kind": "opening", "widthMm": start - cursor})
        out.append(piece)
        cursor = end
    if face_end - cursor > JOINT_MM:
        out.append({"kind": "opening", "widthMm": face_end - cursor})
    return out


def row_width_mm(pieces: list[Piece]) -> int:
    joints = 0
    for index in range(len(pieces) - 1):
        if pieces[index]["kind"] != "opening" and pieces[index + 1]["kind"] != "opening":
            joints += JOINT_MM
    return sum(piece["widthMm"] for piece in pieces) + joints


def is_cut(piece: Piece) -> bool:
    if piece["kind"] == "stretcher":
        return piece["widthMm"] < BRICK_LENGTH_MM
    if piece["kind"] == "header":
        return piece["widthMm"] < HEADER_MM
    if piece["kind"] == "closer":
        return piece["widthMm"] < CLOSER_MM
    return False
