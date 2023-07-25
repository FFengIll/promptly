import copy
from typing import List

import loguru
from pydantic import BaseModel

from prompt.model.case import CaseManager, Case
from prompt.model.profile import Message
from prompt.server import api
from prompt.server.app import app
from prompt.server.util import to_message

log = loguru.logger

manager = CaseManager('./profile/case')


@app.get('/case')
def list_case():
    return [i.dict() for i in manager.values()]


@app.get('/case/{key}')
def get_case(key: int):
    c: Case = manager.get(key)
    return c.dict()


@app.get("/case/refresh")
def refresh_case():
    manager.refresh()


class CaseResult(BaseModel):
    id: int
    source: str
    target: str


@app.post('/debug')
async def debug(case_id: int, messages: List[Message]):
    case = manager.get(case_id)

    res = []
    for idx, source in enumerate(case.data):
        replaced_ms = copy.deepcopy(messages)
        for m in replaced_ms:
            m.content = m.content.replace('{{}}', source)

        ms = to_message(replaced_ms)

        response = await api.chat(ms)

        source = source
        target = response["data"]["choices"][0]["message"]['content']

        res.append(CaseResult(source=source, target=target, id=idx).dict())

    return res
