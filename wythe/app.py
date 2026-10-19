from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from wythe.compare import compare_walls, format_compare
from wythe.elevation import elevation_file_name, elevation_svg
from wythe.sample import SAMPLE_WALL
from wythe.wall import PlanError, plan_wall

app = FastAPI(title="Wythe", version="0.6.0")


class OpeningRequest(BaseModel):
    module: int | None = None
    width: int | None = None
    course: int | None = None
    height: int | None = None


class CornerRequest(BaseModel):
    end: str | None = None
    modules: int | None = None


class WallRequest(BaseModel):
    name: str
    modules: int
    courses: int
    bond: str | None = None
    opening: OpeningRequest | None = None
    corner: CornerRequest | None = None


class CompareRequest(BaseModel):
    left: WallRequest
    right: WallRequest


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/sample")
def sample() -> dict:
    return plan_wall(SAMPLE_WALL)


@app.post("/walls")
def create_wall(wall: WallRequest) -> JSONResponse:
    try:
        plan = plan_wall(wall.model_dump())
    except PlanError as error:
        return JSONResponse(status_code=400, content={"errors": error.errors})
    return JSONResponse(status_code=200, content=plan)


@app.get("/sample/elevation")
def sample_elevation() -> Response:
    return _elevation_response(plan_wall(SAMPLE_WALL))


@app.post("/walls/elevation")
def wall_elevation(wall: WallRequest) -> Response:
    try:
        plan = plan_wall(wall.model_dump())
    except PlanError as error:
        return JSONResponse(status_code=400, content={"errors": error.errors})
    return _elevation_response(plan)


@app.post("/walls/compare")
def compare(body: CompareRequest) -> JSONResponse:
    left, left_errors = _plan_side("left", body.left.model_dump())
    right, right_errors = _plan_side("right", body.right.model_dump())
    errors = left_errors + right_errors
    if errors:
        return JSONResponse(status_code=400, content={"errors": errors})
    assert left is not None and right is not None
    diff = compare_walls(left, right)
    return JSONResponse(
        status_code=200,
        content={
            "left": left["name"],
            "right": right["name"],
            "bricks": diff["bricks"],
            "mortarLengthMm": diff["mortarLengthMm"],
            "text": format_compare(left, right, diff),
        },
    )


def _plan_side(side: str, wall: dict) -> tuple[dict | None, list[str]]:
    try:
        return plan_wall(wall), []
    except PlanError as error:
        return None, [_label_error(side, message) for message in error.errors]


def _label_error(side: str, message: str) -> str:
    field, separator, rest = message.partition(":")
    return f"{side}.{field}{separator}{rest}"


def _elevation_response(plan: dict) -> Response:
    name = elevation_file_name(plan["name"])
    return Response(
        content=elevation_svg(plan),
        media_type="image/svg+xml",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
