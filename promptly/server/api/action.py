import copy
from typing import List

import loguru
from pydantic import BaseModel

from promptly.model.case import CaseResult
from promptly.model.prompt import Argument, CommitItem, Message, ArgumentSetting
from promptly.server import llm
from promptly.server.app import app, mongo
from promptly.server.llm import to_message

log = loguru.logger


class TestingRequestBody(BaseModel):
    sources: List[str]
    messages: List[Message]
    key: str
    args: List[Argument]


def to_placeholder(key):
    return "${" + key + "}"


async def batch_test(messages, key, data):
    res = []
    for idx, source in enumerate(data):
        replaced_ms = copy.deepcopy(messages)
        for m in replaced_ms:
            m.content = m.content.replace(to_placeholder(key), source)

        ms = to_message(replaced_ms)

        log.info("debug with\n{}", ms)

        target = await llm.chat(ms)
        log.info("response: {}", target)
        mongo.history.push(CommitItem(messages=ms, response=target))

        res.append(CaseResult(source=source, target=target, id=idx).dict())

    return res


@app.post("/api/action/testing")
async def run_test_with_source(body: TestingRequestBody, repeat: int = 1):
    messages: List[Message] = body.messages
    sources = body.sources
    key = body.key
    args = body.args

    for m in messages:
        for arg in args:
            if arg.key == key:
                continue
            m.content = m.content.replace(to_placeholder(arg.key), arg.value)

    res = []
    for _ in range(repeat):
        res += await batch_test(messages, key, sources)

    return res


@app.post("/api/action/chat")
async def chat(ms: List[Message], model: str = ""):
    ms = to_message(ms)
    log.info(ms)

    content = await llm.chat(ms, model=model)
    log.info(content)

    mongo.history.push(CommitItem(messages=ms, response=content))
    return content
