from typing import List

import fastapi
import loguru
from pydantic import BaseModel, Field

from promptly.model.prompt import (
    Argument,
    Commit,
    Project,
    Message,
    Profile,
    Snapshot,
)
from promptly.server import llm
from promptly.server.app import app, mongo
from promptly.server.llm import to_message

log = loguru.logger

manager = mongo.prompt


@app.on_event("shutdown")
def shutdown_event():
    pass


@app.post("/api/prompt/{key}/snapshot")
def add_snapshot(key: str, snapshot: Snapshot):
    p = manager.get(key)

    manager.update_snapshot(p, snapshot)

    return manager.get(key).snapshots


@app.put("/api/prompt/{key}")
def create_prompt(key: str):
    if manager.get(key):
        log.warning("existed profile")
        return

    p = Profile(name=key)
    manager.add_profile(p)
    manager.reload()
    return


@app.get("/api/prompt/{key}/snapshot")
def get_snapshot(key: str):
    p = manager.get(key)
    if p:
        return [s.dict() for s in p.snapshots]
    raise fastapi.HTTPException(status_code=404)


@app.get("/api/prompt/{key}")
def load_profile(key: str):
    profile = manager.get(key=key)
    if not profile:
        raise fastapi.HTTPException(status_code=404)
    return profile.dict()


@app.post("/api/prompt/{key}")
def update_profile(key: str, update: List[Message]):
    p = manager.get(key)
    p.messages = update

    manager.update_message(p)

    p = manager.get(key)
    return p


@app.post("/api/chat/{key}")
async def chat_with_key(key: str, ms: List[Message]):
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


@app.post("/api/chat/")
async def chat(ms: List[Message]):
    ms = to_message(ms)
    log.info(ms)

    content = await llm.chat(ms)
    log.info(content)

    mongo.history.push(Snapshot(prompt=ms, response=content))
    return content


@app.get("/api/prompt")
def list_prompt(refresh: bool = False):
    if refresh:
        manager.reload()
    return dict(keys=manager.keys())


class CommitRequest(BaseModel):
    iters: List[Commit]
    args: List[Argument]


@app.post("/api/commit")
def do_commit(
    req: CommitRequest,
    name: str,
):
    project = Project(name=name, iters=req.iters, args=req.args)
    mongo.commit.push(project)


@app.get("/api/commit")
def get_commit(name: str):
    res = mongo.commit.get(name)
    if not res:
        raise fastapi.HTTPException(404)
    return res
