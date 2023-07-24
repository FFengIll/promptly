"""
For data:
we can load or store, each data is a fabric json object.
the data can contain
- ui layout (including each inner component)
- component value (e.g. text, select and so on)
- history and snapshot
"""

import glob
import os
from collections import defaultdict
from typing import Dict, List

import fastapi
import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from prompt.model.event import ActionEvent, UpdateEvent
from prompt.model.graph import Graph
from prompt.model.profile import Message, ProfileManager
from prompt.server import api

log = loguru.logger

manager = ProfileManager("./profile")
memory: Dict[str, Graph] = defaultdict(default_factory=lambda: Graph())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.on_event("shutdown")
def shutdown_event():
    manager.save()


@app.post("/load")
def load(name: str):
    graph = load_from_memory(name)
    return graph.json()


@app.get("/profile/{key}")
def load_profile(key: str):
    profile = manager.get(key=key)
    if not profile:
        return fastapi.HTTPException(status_code=404)
    return dict(profile=profile.dict())


@app.post("/profile/{key}")
def update_profile(key: str, update: List[Message]):
    for m in update:
        manager.update_one(key, m)

    p = manager.get(key)
    return p.dict()


@app.post("/chat/{key}")
def chat(key: str, update: List[Message]):
    # manager.update(
    #     key, [UpdateEvent(id=i.id, key="enable", value=i.enable) for i in update]
    # )

    for m in update:
        manager.update_one(key, m)

    profile = manager.get(key)

    ms = to_message(profile.messages)
    log.info(ms)
    res = api.chat(ms)
    return res["data"]["choices"][0]["message"]["content"]


def to_message(ms: List[Message]):
    res = []
    for i in ms:
        if i.enable:
            res.append(dict(role=i.role, content=i.content))
    return res


@app.get("/profile")
def list_profile():
    return dict(keys=manager.list_profile())


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


@app.get("/extensions")
def get_extensions():
    files = glob.glob(os.path.join(app.root_path, "extensions/**/*.js"), recursive=True)
    res = list(
        map(lambda f: "/" + os.path.relpath(f, app.root_path).replace("\\", "/"), files)
    )
    print(res)

    return res


app.mount("/", StaticFiles(directory="web"), name="web")
