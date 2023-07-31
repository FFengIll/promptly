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
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from promptly.model.event import ActionEvent, UpdateEvent
from promptly.model.graph import Graph
from promptly.server.app import app

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
