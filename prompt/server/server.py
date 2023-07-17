import glob
import os
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from prompt.server.event import UpdateEvent, ActionEvent
from prompt.server.graph import Graph

app = FastAPI()

"""
For data:
we can load or store, each data is a fabric json object.
the data can contain 
- ui layout (including each inner component)
- component value (e.g. text, select and so on)
- history and snapshot
"""

from collections import defaultdict

memory: Dict[str, Graph] = defaultdict(default_factory=lambda: Graph())


class GPT35Template():
    pass


def load_from_memory(name):
    graph = memory[name]
    if graph.is_empty():
        graph.from_template(GPT35Template)
    return graph


@app.post("/load")
def load(name: str):
    graph = load_from_memory(name)
    return graph.json()


class EventRequest(BaseModel):
    name: str
    updates: List[UpdateEvent]
    actions: List[ActionEvent]


@app.post("/event")
def event(event: EventRequest):
    name = event.name
    graph = load_from_memory(name)

    for update in event.updates:
        graph.update(update.node, update.id, update.value)

    for action in event.actions:
        graph.action(action.node, action.name)

    return


@app.get("/")
def index():
    return RedirectResponse(url=app.url_path_for("/index.html"))


import loguru

log = loguru.logger


@app.get("/extensions")
def get_extensions():
    files = glob.glob(os.path.join(app.root_path, 'extensions/**/*.js'), recursive=True)
    res = list(map(lambda f: "/" + os.path.relpath(f, app.root_path).replace("\\", "/"), files))
    print(res)

    return res


app.mount("/", StaticFiles(directory="web"), name="web")
