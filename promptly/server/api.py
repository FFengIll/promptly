from copy import deepcopy

import httpx
import requests
from httpx import AsyncClient
from sqlalchemy import func
from sqlmodel import Session, select

from promptly.model.orm import Profile, engine
from promptly.openai.config import key, url

# create_db_and_tables()
payload = {
    "messages": [],
    "key": key,
    "model": "",
}


def new_profile(name):
    with Session(engine) as s:
        p = select([func.count(Profile.id)]).where(Profile.name == name)
        if s.exec(p).one():
            return
        else:
            p = Profile(name=name)
            s.add(p)
            s.commit()


def list_profile():
    res = []
    with Session(engine) as s:
        q = select(Profile)
        for i in s.exec(q):
            res.append(i.name)
    return res


def simple_chat(content):
    messages = [dict(role="user", content=content)]
    return chat(messages)


async def chat(messages):
    headers = {}

    data = deepcopy(payload)
    data["messages"] = messages

    async with AsyncClient() as c:
        response = await c.post(url, headers=headers, json=data, timeout=10)
        if response.status_code != 200:
            return "error"
        answer = response.json()

    return answer
