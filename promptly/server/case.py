import copy
from typing import List

import loguru
from pydantic import BaseModel

from promptly.manager.memory import CaseManager
from promptly.model.case import Case
from promptly.model.profile import Message
from promptly.server import api
from promptly.server.app import app
from promptly.server.util import to_message

log = loguru.logger

manager = CaseManager("./profile/case")


@app.get("/case")
def list_case():
    return [i.dict() for i in manager.values()]


@app.get("/case/{key}")
def get_case(key: int):
    c: Case = manager.get(key)
    return c.dict()


@app.get("/api/case/refresh")
def refresh_case():
    manager.refresh()


class CaseResult(BaseModel):
    id: int
    source: str
    target: str


@app.post("/api/debug/loop")
async def debug(count: int, messages: List[Message]):
    res = []
    for idx in range(count):
        ms = to_message(messages)
        response = await api.chat(ms)

        target = response["data"]["choices"][0]["message"]["content"]
        res.append(CaseResult(source="", target=target, id=idx).dict())

    return res


async def batch_debug(messages, data):
    res = []
    for idx, source in enumerate(data):
        replaced_ms = copy.deepcopy(messages)
        for m in replaced_ms:
            m.content = m.content.replace("{{}}", source)

        ms = to_message(replaced_ms)

        response = await api.chat(ms)

        source = source
        target = response["data"]["choices"][0]["message"]["content"]

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
async def debug(case_id: int, messages: List[Message]):
    case = manager.get(case_id)
    data = case.data

    return await batch_debug(messages, data)
