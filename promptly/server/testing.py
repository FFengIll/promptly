import copy
from typing import List

import fastapi
import loguru
from pydantic import BaseModel

from promptly.model.case import CaseResult
from promptly.model.prompt import Commit, Message
from promptly.server import llm
from promptly.server.app import app, mongo
from promptly.server.llm import to_message

log = loguru.logger


class TestingRequestBody(BaseModel):
    sources: List[str]
    messages: List[Message]


@app.post("/api/testing")
async def run_test_with_source(body: TestingRequestBody, repeat: int = 1):
    data = body.sources
    messages: List[Message] = body.messages

    res = []
    for idx in range(repeat):
        res += await batch_test(messages, data)

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
