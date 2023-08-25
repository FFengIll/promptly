from copy import deepcopy
from typing import List

import loguru
from httpx import AsyncClient

from promptly.config import key, url
from promptly.model.prompt import Message

log = loguru.logger


payload = {
    "messages": [],
    "key": key,
    "model": "",
}


def to_message(ms: List[Message]):
    res = []
    for i in ms:
        if i.enable:
            res.append(dict(role=i.role, content=i.content))
    return res


def simple_chat(content):
    messages = [dict(role="user", content=content)]
    return chat(messages)


client = AsyncClient()


async def chat(messages, model=""):
    headers = {}

    data = deepcopy(payload)
    data["messages"] = messages
    data["model"] = model

    response = await client.post(url=url, headers=headers, json=data, timeout=30)
    log.info(response)
    response.raise_for_status()

    answer = response.json()

    res = answer["data"]["choices"][0]["message"]["content"]
    log.info(res)

    return res
