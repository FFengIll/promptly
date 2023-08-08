import copy
from typing import List

import fastapi
import loguru
from promptly.server.llm import to_message
from pydantic import BaseModel

from promptly.model.case import CaseResult
from promptly.model.profile import Message, Snapshot
from promptly.server import llm
from promptly.server.app import app
from promptly.server.app import mongo

log = loguru.logger


@app.post("/api/debug/loop")
async def debug(count: int, messages: List[Message]):
    res = []
    for idx in range(count):
        ms = to_message(messages)
        response = await llm.chat(ms)

        mongo.history.push(Snapshot(prompt=ms, response=response))

        target = response
        res.append(CaseResult(source="", target=target, id=idx).dict())

    return res


async def batch_debug(messages, data):
    res = []
    for idx, source in enumerate(data):
        replaced_ms = copy.deepcopy(messages)
        for m in replaced_ms:
            m.content = m.content.replace("{{}}", source)

        ms = to_message(replaced_ms)

        log.info("debug with\n{}", ms)

        target = await llm.chat(ms)
        log.info("response: {}", target)
        mongo.history.push(Snapshot(prompt=ms, response=target))

        res.append(CaseResult(source=source, target=target, id=idx).dict())

    return res


class DebugRequestBody(BaseModel):
    source: str
    messages: List[Message]


@app.post("/api/debug/source")
async def debug(body: DebugRequestBody):
    source: str = body.source
    messages: List[Message] = body.messages
    data = [source]

    return await batch_debug(messages, data)


@app.post("/api/debug/case")
async def debug(name: str, messages: List[Message]):
    case = mongo.case.get(name)
    if not case:
        raise fastapi.HTTPException(404)
    data = case.data

    return await batch_debug(messages, data)
