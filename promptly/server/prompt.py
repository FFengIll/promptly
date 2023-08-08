from typing import List

import fastapi
import loguru

from promptly.model.profile import Message, Profile, Snapshot
from promptly.server import llm
from promptly.server.app import mongo
from promptly.server.app import app
from promptly.server.llm import to_message

log = loguru.logger

manager = mongo.profile


@app.on_event("shutdown")
def shutdown_event():
    pass


@app.post("/api/profile/{key}/snapshot")
def add_snapshot(key: str, snapshot: Snapshot):
    p = manager.get(key)

    manager.update_snapshot(p, snapshot)

    return manager.get(key).snapshots


@app.put("/api/profile/{key}")
def create_profile(key: str):
    if manager.get(key):
        log.warning("existed profile")
        return

    p = Profile(name=key)
    manager.add_profile(p)
    manager.reload()
    return


@app.get("/api/profile/{key}/snapshot")
def get_snapshot(key: str):
    p = manager.get(key)
    if p:
        return [s.dict() for s in p.snapshots]
    raise fastapi.HTTPException(status_code=404)


@app.get("/api/profile/{key}")
def load_profile(key: str):
    profile = manager.get(key=key)
    if not profile:
        raise fastapi.HTTPException(status_code=404)
    return profile.dict()


@app.post("/api/profile/{key}")
def update_profile(key: str, update: List[Message]):
    p = manager.get(key)
    p.messages = update

    manager.update_message(p)

    p = manager.pro.get(key)
    return p


@app.post("/api/chat/{key}")
async def chat(key: str, ms: List[Message]):
    p: Profile = manager.get(key)
    if not p:
        raise fastapi.HTTPException(404)
    p.messages = ms

    for m in p.messages:
        if m.content not in p.history:
            p.history.append(m.content)

    # update
    manager.update_message(p)
    manager.update_history(p)

    ms = to_message(p.messages)
    log.info(ms)

    content = await llm.chat(ms)
    log.info(content)

    mongo.history.push(Snapshot(prompt=ms, response=content))

    log.info(content)

    return content


@app.get("/api/profile")
def list_profile(refresh: bool = False):
    if refresh:
        manager.reload()
    return dict(keys=manager.keys())
