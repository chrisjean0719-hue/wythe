import uvicorn

from wythe.app import app


def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8023)


if __name__ == "__main__":
    main()
