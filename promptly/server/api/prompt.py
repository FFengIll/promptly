from typing import Dict, List

import fastapi
import loguru
import pydantic
from pydantic import BaseModel

from promptly.model.prompt import Argument, ArgumentSetting, CommitItem, Message, Prompt
from promptly.schema import autocomplete
from promptly.server.api.util import check_mongo_result
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


@autocomplete
class ListPromptResponse(BaseModel):
    data: Dict[str, List]


@app.get("/api/prompt", response_model=ListPromptResponse)
def list_prompt(refresh: bool = False):
    if refresh:
        manager.reload()

    data = {}
    for k, v in manager.index().items():
        data[k] = list(v)

    return ListPromptResponse(data=data)


class UpdatePromptBody(BaseModel):
    messages: List[Message] = pydantic.Field(default="")
    model: str = ""
    args: List[Argument] = pydantic.Field(default_factory=list)
    default_model: str = pydantic.Field(default="", alias="defaultModel")
    group: str = ""


@app.post("/api/prompt")
def create_prompt(body: UpdatePromptBody, name: str):
    if manager.get(name):
        log.warning("existed profile")
        return

    p = Prompt(name=name, group=body.group)
    manager.add_prompt(p)
    manager.reload()
    return


@app.get("/api/prompt/{name}")
def load_prompt(name: str):
    prompt: Prompt = manager.get(key=name)
    if not prompt:
        raise fastapi.HTTPException(status_code=404)
    return prompt.dict(by_alias=True)


@app.put("/api/prompt/{name}")
def update_prompt(
    body: UpdatePromptBody,
    name: str,
):
    log.info(body)

    p = manager.get(name)
    p.messages = body.messages or p.messages
    p.model = body.model or p.model
    p.args = body.args or p.args
    p.default_model = body.default_model or p.default_model

    manager.update_prompt(p)

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
