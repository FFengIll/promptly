"""
For data:
we can load or store, each data is a fabric json object.
the data can contain
- ui layout (including each inner component)
- component value (e.g. text, select and so on)
- history and snapshot
"""

from collections import defaultdict
from typing import Dict, List

import loguru
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from prompt.model.event import ActionEvent, UpdateEvent
from prompt.model.graph import Graph
from prompt.server.app import app

log = loguru.logger

memory: Dict[str, Graph] = defaultdict(default_factory=lambda: Graph())


class GPT35Template:
    pass


class EventRequest(BaseModel):
    name: str
    updates: List[UpdateEvent]
    actions: List[ActionEvent]


def load_from_memory(name):
    graph = memory[name]
    if graph.is_empty():
        graph.from_template(GPT35Template)
    return graph


@app.post("/load")
def load(name: str):
    graph = load_from_memory(name)
    return graph.json()


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
