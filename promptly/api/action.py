import copy
from typing import List

import fastapi
import loguru
from fastapi_restful.api_model import APIModel
from pydantic import BaseModel

from promptly import llm
from promptly.dao import MongoManager
from promptly.llm import to_message
from promptly.model.prompt import (
    Argument,
    ArgumentSetting,
    CommitItem,
    LLMOption,
    Message,
)
from promptly.model.testcase import TestResult

from .util import check_mongo_result

log = loguru.logger

router = fastapi.APIRouter()
mongo = MongoManager.default()


class TestingRequestBody(APIModel):
    sources: List[str]
    messages: List[Message]
    arg_key: str
    args: List[Argument]
    model: str = ""


def to_placeholder(key):
    return "${" + key + "}"


async def batch_test(messages, key, data, model):
    res = []
    for idx, source in enumerate(data):
        replaced_ms = copy.deepcopy(messages)
        for m in replaced_ms:
            m.content = m.content.replace(to_placeholder(key), source)

        ms = to_message(replaced_ms)

        log.info("debug with\n{}", ms)

        target = await llm.chat(ms, model=model)
        log.info("response: {}", target)

        res.append(TestResult(source=source, target=target, id=idx).dict())

    return res


@router.post("/api/action/testing")
async def run_test_with_source(body: TestingRequestBody, repeat: int = 1):
    messages: List[Message] = body.messages
    sources = body.sources
    key = body.arg_key
    args = body.args
    model = body.model

    for m in messages:
        for arg in args:
            if arg.key == key:
                continue
            m.content = m.content.replace(to_placeholder(arg.key), arg.value)

    res = []
    for _ in range(repeat):
        res += await batch_test(messages, key, sources, model)

    return res


class StarBody(BaseModel):
    name: str
    md5: str
    value: bool


@router.post("/api/action/star")
def new_commit(body: StarBody):
    res = mongo.commit.star(body.name, body.md5, body.value)
    return check_mongo_result(res)


class ChatBody(BaseModel):
    messages: List[Message]
    options: LLMOption


@router.post("/api/action/chat")
async def chat(body: ChatBody):
    ms = to_message(body.messages)
    options = body.options
    log.info(ms)
    log.info(options)

    content = await llm.chat(ms, **options.model_dump(by_alias=False))
    log.info(content)

    return content


@router.post(
    "/api/action/args/clean",
)
async def clean_args(name: str):
    arg_setting: ArgumentSetting = mongo.argument.get_setting(name)
    pending = set()
    for i in arg_setting.args:
        pending.add(i)
    arg_setting.args = list(pending)
    mongo.argument.save_setting(arg_setting)
    return True


class RenameBody(APIModel):
    source: str
    target: str


@router.post(
    "/api/action/rename",
)
async def rename(body: RenameBody):
    target = mongo.prompt.get(body.target)
    if target:
        log.info(target)
        raise fastapi.HTTPException(401)

    source = mongo.prompt.get(body.source)
    if not source:
        raise fastapi.HTTPException(404)

    res = mongo.rename(body.source, body.target)
    # return check_mongo_result(res)
    return True
