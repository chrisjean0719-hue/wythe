def format_plan(plan: dict) -> str:
    return "\n".join(
        [
            plan["name"],
            f"{plan['bond']} bond, {plan['modules']} modules, {plan['courses']} courses",
            f"face: {plan['faceLengthMm']} mm wide, {plan['faceHeightMm']} mm high",
            f"bricks: {plan['bricks']}",
            f"stretchers: {plan['stretchers']}",
            f"headers: {plan['headers']}",
            f"closers: {plan['closers']}",
            f"mortar: {plan['mortarLengthMm']} mm",
        ]
    )
