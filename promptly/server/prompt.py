from typing import List

import fastapi
import loguru

from promptly.manager import MongoProfileManger
from promptly.model.profile import Message, History, Profile, Snapshot
from promptly.orm.mongo import client
from promptly.server import api
from promptly.server.app import app
from promptly.server.util import to_message

log = loguru.logger

mongo = MongoProfileManger(client)


@app.on_event("shutdown")
def shutdown_event():
    pass


@app.post("/api/profile/{key}/snapshot")
def add_snapshot(key: str, snapshot: Snapshot):
    p = mongo.get_profile(key)

    mongo.update_snapshot(p, snapshot)

    return mongo.get_profile(key).snapshots


@app.put("/api/profile/{key}")
def create_profile(key: str):
    if mongo.get_profile(key):
        log.warning("existed profile")
        return

    p = Profile(name=key)
    mongo.add_profile(p)
    return


@app.get("/api/profile/{key}/snapshot")
def get_snapshot(key: str):
    p = mongo.get_profile(key)
    if p:
        return [s.dict() for s in p.snapshots]
    return fastapi.HTTPException(status_code=404)


@app.get("/api/profile/{key}")
def load_profile(key: str):
    profile = mongo.get_profile(key=key)
    if not profile:
        return fastapi.HTTPException(status_code=404)
    return profile.dict()


@app.post("/api/profile/{key}")
def update_profile(key: str, update: List[Message]):
    p = mongo.get_profile(key)
    p.messages = update

    mongo.update_message(p)

    p = mongo.get_profile(key)
    return p


@app.post("/api/chat/{key}")
async def chat(key: str, ms: List[Message]):
    p: Profile = mongo.get_profile(key)
    p.messages = ms

    # update
    mongo.update_message(p)

    ms = to_message(p.messages)
    log.info(ms)
    try:
        res = await api.chat(ms)
        content = res["data"]["choices"][0]["message"]["content"]

        mongo.push_history(History(prompt=ms, response=content))

        log.info(content)

        return content

    except Exception as e:
        return fastapi.HTTPException(500)


@app.get("/api/profile")
def list_profile(refresh: bool = False):
    if refresh:
        mongo.reload()
    return dict(keys=mongo.list_profile())
