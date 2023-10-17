import sys

import loguru
import typer
import uvicorn

from promptly.config import SystemConfigModel
from promptly.dao import mongo

sys.path.insert(0, ".")


log = loguru.logger


def main(
    db: str = typer.Option(None, "--db", help="db url"),
    config: str = typer.Option(
        "", "-c", "--config", is_eager=True, help="config file path"
    ),
    host: str = typer.Option("127.0.0.1", "--host", help="host"),
):
    config = SystemConfigModel.parse_from(config)
    log.info(config)

    if db:
        mongo.url = db
        log.info("db: {}", mongo.url)

    from promptly.server import app

    uvicorn.run(app, host=host, port=8000)


if __name__ == "__main__":
    typer.run(main)
