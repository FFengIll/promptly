from typing import List

import loguru
import openai

from promptly.config import ProviderModel, SystemConfigModel
from promptly.model.prompt import Message

log = loguru.logger


def to_message(ms: List[Message]):
    res = []
    for i in ms:
        if i.enable:
            res.append(dict(role=i.role, content=i.content))
    return res


async def simple_chat(content):
    messages = [dict(role="user", content=content)]
    return await chat(messages)


async def chat(messages, model="", **kwargs):
    config = SystemConfigModel.singleton()

    if not model:
        model = SystemConfigModel.singleton().default_model

    provider: ProviderModel = config.get_provider(model)

    openai.api_base = provider.api_base
    openai.api_key = provider.api_key

    response = openai.ChatCompletion.create(
        messages=messages,
        headers={"HTTP-Referer": "https://test.com", "X-Title": "test"},
        timeout=3,
        model=model,
        **kwargs
    )

    log.info("response: {}", response)

    choice = response["choices"][0]
    log.info("choice: {}", choice)

    try:
        return choice["message"]["content"]
    except Exception as e:
        log.exception(e)

    return choice["text"]
