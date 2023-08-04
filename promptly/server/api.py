from copy import deepcopy

import loguru
import requests
from httpx import Client

from promptly.manager import MongoProfileManger
from promptly.openai.config import key, url
from promptly.orm.mongo import client

log = loguru.logger
mongo = MongoProfileManger(client)


payload = {
    "messages": [],
    "key": key,
    "model": "",
}


def simple_chat(content):
    messages = [dict(role="user", content=content)]
    return chat(messages)


client = Client()


def chat(messages):
    headers = {}

    data = deepcopy(payload)
    data["messages"] = messages

    response = requests.post(url=url, headers=headers, json=data, timeout=30)
    log.info(response)
    response.raise_for_status()

    answer = response.json()

    res = answer["data"]["choices"][0]["message"]["content"]
    log.info(res)

    return res
