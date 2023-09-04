from typing import List

import loguru
import openai

from promptly.config import key, url
from promptly.model.prompt import Message

log = loguru.logger


def to_message(ms: List[Message]):
    res = []
    for i in ms:
        if i.enable:
            res.append(dict(role=i.role, content=i.content))
    return res


def simple_chat(content):
    messages = [dict(role="user", content=content)]
    return chat(messages)


async def chat(messages, model=""):
    openai.api_base = url
    openai.api_key = key

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        headers={"HTTP-Referer": "https://test.com", "X-Title": "test"},
    )

    log.info(response)

    res = response["choices"][0]["message"]["content"]
    log.info(res)

    return res
