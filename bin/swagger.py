import json
import re

import loguru
from fastapi import FastAPI
from fastapi.routing import APIRoute

from promptly.server import app


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            # route.operation_id = route.name  # in this case, 'read_items'

            # operation_id = route.name + route.path
            operation_id = route.path + "_" + list(route.methods)[0]
            operation_id = re.sub(r"\W", "_", operation_id)
            operation_id = operation_id.strip("_")
            operation_id = operation_id.lower()
            loguru.logger.info(operation_id)
            route.operation_id = operation_id


use_route_names_as_operation_ids(app)

if __name__ == "__main__":
    with open("../data/swagger.json", "w") as fd:
        use_route_names_as_operation_ids(app)
        schema = app.openapi()
        json.dump(schema, fd, indent=4, ensure_ascii=False)
