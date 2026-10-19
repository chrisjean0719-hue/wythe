def compare_walls(left: dict, right: dict) -> dict:
    return {
        "bricks": [left["bricks"], right["bricks"]],
        "mortarLengthMm": [left["mortarLengthMm"], right["mortarLengthMm"]],
    }


def format_compare(left: dict, right: dict, diff: dict) -> str:
    return "\n".join(
        [
            f"{left['name']} vs {right['name']}",
            f"bricks: {diff['bricks'][0]} vs {diff['bricks'][1]}",
            f"mortar: {diff['mortarLengthMm'][0]} mm vs {diff['mortarLengthMm'][1]} mm",
        ]
    )
