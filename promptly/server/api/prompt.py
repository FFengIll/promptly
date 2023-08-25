from typing import List

import fastapi
import loguru
from pydantic import BaseModel
from pymongo import results

from promptly.model.prompt import CommitItem, Message, Prompt, ArgumentSetting
from promptly.server.app import app, mongo

log = loguru.logger

manager = mongo.prompt


class CommitRequest(BaseModel):
    commits: List[CommitItem]


class ArgRequest(BaseModel):
    key: str
    value: str


@app.on_event("shutdown")
def shutdown_event():
    pass


@app.get("/api/prompt")
def list_prompt(refresh: bool = False):
    if refresh:
        manager.reload()
    return dict(keys=manager.keys())


@app.post("/api/prompt")
def create_prompt(name: str):
    if manager.get(name):
        log.warning("existed profile")
        return

    p = Prompt(name=name)
    manager.add_profile(p)
    manager.reload()
    return


@app.get("/api/prompt/{name}")
def load_profile(name: str):
    profile = manager.get(key=name)
    if not profile:
        raise fastapi.HTTPException(status_code=404)
    return profile.dict()


@app.put("/api/prompt/{name}")
def update_profile(
    update: List[Message],
    name: str,
):
    p = manager.get(name)
    p.messages = update

    manager.update_message(p)

    p = manager.get(name)
    return p


def check_mongo_result(res: results.UpdateResult):
    if not res.acknowledged:
        raise fastapi.HTTPException(404)

    # if res.modified_count <= 0 and res.matched_count<=0:
    #     raise fastapi.HTTPException(404)

    return True


@app.get("/api/prompt/args/{name}", response_model=ArgumentSetting)
def get_argument(name: str):
    res = mongo.argument.get_setting(name)
    return res.json()


@app.put("/api/prompt/args/{name}")
def update_argument(item: ArgRequest, name: str):
    mongo.argument.add_value(name, item.key, item.value)


class NewCommitBody(BaseModel):
    commit: CommitItem
    name: str


@app.post("/api/commit")
def new_commit(body: NewCommitBody):
    res = mongo.commit.add_commit(
        name=body.name,
        commit=body.commit,
    )
    return check_mongo_result(res)


@app.put("/api/commit/{name}")
def commit_prompt(
    commits: List[CommitItem],
    name: str,
):
    mongo.commit.push(name, *commits)


@app.get("/api/commit/{name}")
def get_commit(name: str):
    res = mongo.commit.get(name)
    if not res:
        raise fastapi.HTTPException(404)
    return res
