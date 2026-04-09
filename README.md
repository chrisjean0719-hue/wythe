# Wythe

An HTTP API for a brick wall. It lays 190 by 57 mm bricks with 10 mm joints in running bond, stack bond, or Flemish bond, can leave a rectangular opening, can turn one end into a return, and counts the stretchers, headers, closers, and mortar.

It is for someone setting out a garden wall at home. The sample wall is made up. The service does not store names, addresses, or customer orders.

Written in Python 3.11 or newer, with FastAPI. Tests use pytest.

## Run

```bash
python -m venv .venv
.venv\Scripts\pip install -e ".[dev]"
.venv\Scripts\pytest
.venv\Scripts\python -m wythe
```

On macOS or Linux, use `.venv/bin/` instead of `.venv\Scripts\`.

The server is at http://127.0.0.1:8023.

```bash
curl http://127.0.0.1:8023/sample
curl -X POST http://127.0.0.1:8023/walls -H "Content-Type: application/json" -d "{\"name\":\"Sample garden wall\",\"modules\":10,\"courses\":8}"
```

A wall is a name, a bond, a module count, and a course count. Leave the bond out to keep running bond. One module is a 190 mm brick plus a 10 mm joint. The face is one joint shorter than the module count, because the joints sit between bricks and not past the ends. Running bond lays stretchers, and every other course starts and ends with a 90 mm closer. Two closers are cut from one brick. Stack bond repeats that stretcher course with no offset. Flemish bond alternates stretchers and 90 mm headers, and the next course starts with a header so the joints do not line up. Course 1 is the first course in the response, and it is the bottom row. The mortar length is the bed joints between courses plus the vertical joints, in millimetres. The sample garden wall is 10 modules by 8 courses in running bond: 1990 by 526 mm, 80 bricks, and 18262 mm of mortar. The same wall in Flemish bond uses 108 bricks and 19630 mm of mortar. Leave the opening out for a solid wall. An opening gives the first module and the first course, counted from the left and from the bottom, then the width and height. Bricks fully inside that rectangle are left out of the count. A brick the hole cuts through still counts, and the plan reports it as a cut. On the sample wall in stack bond, an opening at module 3, two modules wide, from course 2 and three courses high, leaves 74 bricks and 16701 mm of mortar. Leave the corner empty for a straight wall. A corner names the left or right end and how many modules continue past it. The corner brick is the end brick of the front wall, counted once. The return uses the same bond and the same courses, and its mortar includes the vertical joint against that corner. A return of 4 modules on the sample wall adds 32 bricks, a 790 mm return face, and brings the mortar to 25844 mm. An elevation file is later work.

## Layout

```
wythe/          brick size, running bond, checks, the HTTP API
examples/       a fictional wall
tests/          unit tests
```

## Next

Two updates remain. About 38 hours of later work stay in [ROADMAP.md](ROADMAP.md) after those six.

## License

MIT
