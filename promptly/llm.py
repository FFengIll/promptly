from typing import List

import httpx
import loguru
from openai import OpenAI

from promptly.config import ProviderModel, SystemConfigModel
from promptly.model.prompt import Message

log = loguru.logger

client_pool = {}


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

    proxy = provider.proxy

    key = "{}+{}".format(provider.api_base, proxy)
    client = client_pool.get(key, None)

    if not client:
        # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=provider.api_base)'
        if proxy:
            client = OpenAI(
                api_key=provider.api_key,
                base_url=provider.api_base,
                http_client=httpx.Client(proxy=str(proxy)),
            )
        else:
            client = OpenAI(api_key=provider.api_key, base_url=provider.api_base)

        client_pool[key] = client

    response = client.chat.completions.create(model=model, messages=messages, timeout=3)

    log.info("response: {}", response)

    choice = response.choices[0]
    log.info("choice: {}", choice)

    return choice.message.content
