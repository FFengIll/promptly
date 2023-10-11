import sys

import loguru
import typer
import uvicorn

sys.path.insert(0, ".")


log = loguru.logger


def main(
    db: str = typer.Option(None, "--db", help="db url"),
    host: str = typer.Option("127.0.0.1", "--host", help="host"),
):
    from promptly.dao import mongo

    if db:
        mongo.url = db
        log.info("db: {}", mongo.url)

    from promptly.server import app

    uvicorn.run(app, host=host, port=8000)


if __name__ == "__main__":
    typer.run(main)
