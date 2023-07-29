from typing import List

import fastapi
import loguru

from prompt.model.profile import Message, ProfileManager
from prompt.server import api
from prompt.server.app import app
from prompt.server.util import to_message

log = loguru.logger

manager = ProfileManager("./profile")


@app.on_event("shutdown")
def shutdown_event():
    manager.save()


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
    res = await api.chat(ms)
    return res["data"]["choices"][0]["message"]["content"]


@app.delete("/api/profile/{key}/{id}")
def delete_prompt_item(key: str, id: int):
    p = manager.get(key)
    p.remove(id)

    return p.dict()


@app.get("/api/profile")
def list_profile():
    return dict(keys=manager.list_profile())
