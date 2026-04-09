def format_plan(plan: dict) -> str:
    lines = [
        plan["name"],
        f"{plan['bond']} bond, {plan['modules']} modules, {plan['courses']} courses",
        f"face: {plan['faceLengthMm']} mm wide, {plan['faceHeightMm']} mm high",
        f"bricks: {plan['bricks']}",
        f"stretchers: {plan['stretchers']}",
        f"headers: {plan['headers']}",
        f"closers: {plan['closers']}",
        f"cuts: {plan['cuts']}",
        (
            f"opening: module {plan['opening']['module']}, {plan['opening']['width']} wide, "
            f"course {plan['opening']['course']}, {plan['opening']['height']} high"
            if plan["opening"]
            else "opening: none"
        ),
        (
            f"corner: {plan['corner']['end']}, {plan['corner']['modules']} modules"
            if plan["corner"]
            else "corner: none"
        ),
    ]
    if plan["corner"]:
        lines.append(f"return face: {plan['returnFaceLengthMm']} mm")
    lines.append(f"mortar: {plan['mortarLengthMm']} mm")
    return "\n".join(lines)
