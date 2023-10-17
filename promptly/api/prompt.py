from typing import Dict, List

import fastapi
import loguru
import pydantic
from fastapi_restful.api_model import APIModel
from pydantic import BaseModel

from promptly.dao import MongoManager
from promptly.model.prompt import (
    Argument,
    ArgumentSetting,
    CommitItem,
    LLMOption,
    Message,
    Prompt,
)
from promptly.schema import autocomplete

from .util import check_mongo_result

log = loguru.logger

mongo = MongoManager.default()
manager = mongo.prompt
router = fastapi.APIRouter()


class CommitRequest(BaseModel):
    commits: List[CommitItem]


class ArgRequest(BaseModel):
    key: str
    value: str


@router.on_event("shutdown")
def shutdown_event():
    pass


@autocomplete
class ListPromptResponse(BaseModel):
    data: Dict[str, List]


@router.get("/api/prompt", response_model=ListPromptResponse)
def list_prompt(refresh: bool = False):
    if refresh:
        manager.reload()

    data = {}
    for k, v in manager.index().items():
        data[k] = list(v)

    return ListPromptResponse(data=data)


class UpdatePromptBody(APIModel):
    group: str = ""

    messages: List[Message] = pydantic.Field(default="")

    args: List[Argument] = pydantic.Field(default_factory=list)
    options: LLMOption = pydantic.Field(default_factory=LLMOption)

    plugins: List[str] = []


@router.post("/api/prompt")
def create_prompt(body: UpdatePromptBody, name: str):
    if manager.get(name):
        log.warning("existed profile")
        return

    p = Prompt(name=name, group=body.group)
    manager.add_prompt(p)
    manager.reload()
    return


@router.get("/api/prompt/{name}", response_model=Prompt, response_model_by_alias=True)
def load_prompt(name: str) -> Prompt:
    prompt: Prompt = manager.get(key=name)
    if not prompt:
        raise fastapi.HTTPException(status_code=404)
    return prompt


@router.put("/api/prompt/{name}", response_model=Prompt)
def update_prompt(
    body: UpdatePromptBody,
    name: str,
):
    log.info(body)

    p = manager.get(name)
    p.messages = body.messages or p.messages

    p.args = body.args or p.args
    p.options = body.options

    p.plugins = body.plugins

    manager.update_prompt(p)

    p = manager.get(name)
    return p


@router.get("/api/prompt/args/{name}", response_model=ArgumentSetting)
def get_argument(name: str):
    res = mongo.argument.get_setting(name)
    return res


@router.put("/api/prompt/args/{name}")
def update_argument(item: ArgRequest, name: str):
    mongo.argument.add_value(name, item.key, item.value)


class NewCommitBody(BaseModel):
    commit: CommitItem
    name: str


@router.post("/api/commit")
def new_commit(body: NewCommitBody):
    res = mongo.commit.add_commit(
        name=body.name,
        commit=body.commit,
    )
    return check_mongo_result(res)


@router.get("/api/commits/{name}", response_model=List[CommitItem])
def get_commit(name: str):
    res = mongo.commit.get(name)
    if not res:
        raise fastapi.HTTPException(404)
    return res


@router.put("/api/commits/{name}")
def commit_prompt(
    commits: List[CommitItem],
    name: str,
):
    mongo.commit.push(name, *commits)
