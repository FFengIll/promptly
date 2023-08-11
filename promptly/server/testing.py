import copy
from typing import List

import fastapi
import loguru
from pydantic import BaseModel

from promptly.model.case import CaseResult
from promptly.model.prompt import Message, Commit
from promptly.server import llm
from promptly.server.app import app
from promptly.server.app import mongo
from promptly.server.llm import to_message

log = loguru.logger


class DebugRequestBody(BaseModel):
    source: str
    messages: List[Message]


@app.post("/api/testing/loop")
async def do_test(count: int, messages: List[Message]):
    res = []
    for idx in range(count):
        ms = to_message(messages)
        response = await llm.chat(ms)

        mongo.history.push(Snapshot(prompt=ms, response=response))

        target = response
        res.append(CaseResult(source="", target=target, id=idx).dict())

    return res


async def batch_test(messages, data):
    res = []
    for idx, source in enumerate(data):
        replaced_ms = copy.deepcopy(messages)
        for m in replaced_ms:
            m.content = m.content.replace("{{}}", source)

        ms = to_message(replaced_ms)

        log.info("debug with\n{}", ms)

        target = await llm.chat(ms)
        log.info("response: {}", target)
        mongo.history.push(Commit(messages=ms, response=target))

        res.append(CaseResult(source=source, target=target, id=idx).dict())

    return res


@app.post("/api/testing/source")
async def run_test_with_source(body: DebugRequestBody):
    source: str = body.source
    messages: List[Message] = body.messages
    data = [source]

    return await batch_test(messages, data)


@app.post("/api/testing/case")
async def run_test_with_case(name: str, messages: List[Message]):
    case = mongo.case.get(name)
    if not case:
        raise fastapi.HTTPException(404)
    data = case.data

    return await batch_test(messages, data)
