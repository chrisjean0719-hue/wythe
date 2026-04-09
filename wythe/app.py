from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from wythe.sample import SAMPLE_WALL
from wythe.wall import PlanError, plan_wall

app = FastAPI(title="Wythe", version="0.4.0")


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
