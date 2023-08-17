from typing import List

import fastapi
import loguru
from pydantic import BaseModel
from pymongo import results

from promptly.model.prompt import (
    ArgumentSetting,
    CommitItem,
    Message,
    Prompt,
    PromptCommit,
)
from promptly.server import llm
from promptly.server.app import app, mongo
from promptly.server.llm import to_message

log = loguru.logger

manager = mongo.prompt


@app.on_event("shutdown")
def shutdown_event():
    pass


@app.put("/api/prompt")
def create_prompt(key: str):
    if manager.get(key):
        log.warning("existed profile")
        return

    p = Prompt(name=key)
    manager.add_profile(p)
    manager.reload()
    return


@app.get("/api/prompt")
def load_profile(key: str):
    profile = manager.get(key=key)
    if not profile:
        raise fastapi.HTTPException(status_code=404)
    return profile.dict()


@app.post("/api/prompt")
def update_profile(key: str, update: List[Message]):
    p = manager.get(key)
    p.messages = update

    manager.update_message(p)

    p = manager.get(key)
    return p


@app.post("/api/chat/")
async def chat(ms: List[Message]):
    ms = to_message(ms)
    log.info(ms)

    content = await llm.chat(ms)
    log.info(content)

    mongo.history.push(CommitItem(messages=ms, response=content))
    return content


@app.get("/api/list/prompt")
def list_prompt(refresh: bool = False):
    if refresh:
        manager.reload()
    return dict(keys=manager.keys())


class CommitRequest(BaseModel):
    commits: List[CommitItem]


@app.post("/api/commit")
def commit_one(commit: CommitItem, name: str):
    res = mongo.commit.add_commit(
        name,
        commit,
    )
    return check_mongo_result(res)


def check_mongo_result(res: results.UpdateResult):
    if not res.acknowledged:
        raise fastapi.HTTPException(404)

    # if res.modified_count <= 0 and res.matched_count<=0:
    #     raise fastapi.HTTPException(404)


@app.post("/api/prompt/args")
def save_args(args: ArgumentSetting):
    return mongo.argument.save_setting(args)


@app.get("/api/prompt/args")
def get_args(name: str):
    return mongo.argument.get_setting(name)


class ArgRequest(BaseModel):
    key: str
    value: str


@app.post("/api/prompt/arg")
def save_one_arg(item: ArgRequest, name: str):
    mongo.argument.add_value(name, item.key, item.value)


@app.post("/api/commit/all")
def do_commit(
    commits: List[CommitItem],
    name: str,
):
    project = PromptCommit(name=name, iters=commits)
    mongo.commit.push(project)


@app.get("/api/commit")
def get_commit(name: str):
    res = mongo.commit.get(name)
    if not res:
        raise fastapi.HTTPException(404)
    return res
