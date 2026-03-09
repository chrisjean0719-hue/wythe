# Wythe

An HTTP API for a brick wall. It lays 190 by 57 mm bricks with 10 mm joints in running bond and counts the stretchers, closers, and mortar.

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

A wall is a name, a module count, and a course count. One module is a 190 mm brick plus a 10 mm joint. The face is one joint shorter than the module count, because the joints sit between bricks and not past the ends. Running bond lays stretchers, and every other course starts and ends with a 90 mm closer. Two closers are cut from one brick. Course 1 is the first course in the response, and it is the bottom row. The mortar length is the bed joints between courses plus the vertical joints, in millimetres. The sample garden wall is 10 modules by 8 courses: 1990 by 526 mm, 80 bricks, and 18262 mm of mortar. Stack bond, Flemish bond, and an opening are later work.

## Layout

```
wythe/          brick size, running bond, checks, the HTTP API
examples/       a fictional wall
tests/          unit tests
```

## Next

Five updates remain. About 38 hours of later work stay in [ROADMAP.md](ROADMAP.md) after those six.

## License

MIT
