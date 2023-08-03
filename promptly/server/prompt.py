from typing import List

import fastapi
import loguru
from pydantic import BaseModel

from promptly.manager import ProfileManager, TinyDBProfileManager
from promptly.model.profile import Message, PromptItem, History
from promptly.server import api
from promptly.server.app import app
from promptly.server.util import to_message

log = loguru.logger

manager = ProfileManager("./profile")
tinydb = TinyDBProfileManager("./db/tinydb")


@app.on_event("shutdown")
def shutdown_event():
    tinydb.save()
    manager.save()


class SnapshotRequest(BaseModel):
    snapshot: List[PromptItem]


@app.post("/api/profile/{key}/snapshot")
def add_snapshot(key: str, request: SnapshotRequest):
    p = manager.get(key)
    if p:
        p.add_snapshot(request.snapshot)


@app.get("/api/profile/{key}/snapshot")
def get_snapshot(key: str):
    p = manager.get(key)
    if p:
        return [s.dict() for s in p.snapshots]
    return fastapi.HTTPException(status_code=404)


@app.get("/api/profile/{key}")
def load_profile(key: str):
    profile = manager.get(key=key)
    if not profile:
        return fastapi.HTTPException(status_code=404)
    return profile.dict()


@app.post("/api/profile/{key}")
def update_profile(key: str, update: List[Message]):
    for m in update:
        manager.update_one(key, m)

    p = manager.get(key)
    return p.dict()


@app.post("/api/chat/{key}")
async def chat(key: str, update: List[Message]):
    manager.update_all(key, update)

    profile = manager.get(key)

    ms = to_message(profile.messages)
    log.info(ms)
    try:
        res = await api.chat(ms)
        content = res["data"]["choices"][0]["message"]["content"]

        manager.push_history(History(prompt=ms, response=content))

        return content

    except Exception as e:
        return fastapi.HTTPException(500)


@app.delete("/api/profile/{key}/{id}")
def delete_prompt_item(key: str, id: int):
    p = manager.get(key)
    p.remove(id)

    return p.dict()


@app.get("/api/profile")
def list_profile(refresh: bool = False):
    if refresh:
        manager.load()
    return dict(keys=manager.list_profile())
