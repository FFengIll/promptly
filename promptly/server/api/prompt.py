from typing import List

import fastapi
import loguru
import pydantic
from pydantic import BaseModel
from pymongo import results

from promptly.model.prompt import ArgumentSetting, CommitItem, Message, Prompt
from promptly.server.app import app, mongo
from promptly.server.api.util import check_mongo_result

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


@app.get("/api/prompt/{name}", response_model=Prompt)
def load_prompt(name: str):
    prompt = manager.get(key=name)
    if not prompt:
        raise fastapi.HTTPException(status_code=404)
    return prompt.dict()


class UpdatePromptBody(BaseModel):
    messages: List[Message]
    model: str = pydantic.Field(default="")


@app.put("/api/prompt/{name}")
def update_profile(
    body: UpdatePromptBody,
    name: str,
):
    p = manager.get(name)
    p.messages = body.messages
    p.model = body.model

    manager.update_message(p)

    p = manager.get(name)
    return p


@app.get("/api/prompt/args/{name}", response_model=ArgumentSetting)
def get_argument(name: str):
    res = mongo.argument.get_setting(name)
    return res


@app.put("/api/prompt/args/{name}")
def update_argument(item: ArgRequest, name: str):
    mongo.argument.add_value(name, item.key, item.value)


class NewCommitBody(BaseModel):
    commit: CommitItem
    name: str
    model: str = pydantic.Field(default="")


@app.post("/api/commit")
def new_commit(body: NewCommitBody):
    res = mongo.commit.add_commit(
        name=body.name,
        commit=body.commit,
    )
    return check_mongo_result(res)


@app.get("/api/commits/{name}")
def get_commit(name: str):
    res = mongo.commit.get(name)
    if not res:
        raise fastapi.HTTPException(404)
    return res


@app.put("/api/commits/{name}")
def commit_prompt(
    commits: List[CommitItem],
    name: str,
):
    mongo.commit.push(name, *commits)
