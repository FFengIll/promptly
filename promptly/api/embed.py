from enum import auto
from typing import List

import fastapi
import loguru
from pydantic import BaseModel
from strenum import StrEnum

from promptly import llm
from promptly.dao import MongoManager
from promptly.llm import to_message
from promptly.model.prompt import CommitItem, Message, Prompt

log = loguru.logger

mongo = MongoManager.default()
manager = mongo.embed
router = fastapi.APIRouter()


class RoleEnum(StrEnum):
    user = auto()
    assistant = auto()
    system = auto()


RELATED_CONTENT_ROLE = RoleEnum.assistant


class RetrieveBody(BaseModel):
    name: str
    messages: List[Message]


@router.post("/api/action/retrieve")
def action_retrieve(body: RetrieveBody):
    data: Prompt = manager.get(body.name)
    res = retrieve(body.messages[-1].content, data.docs)
    return to_retrieved(res)


def to_retrieved(ms: List[str]):
    return """===Related===
{}
""".format(
        "\n\n".join(ms)
    )


def to_rag_message(ins, last_response):
    return """You are a helpful AI assistant.

    If `Instruction` is a question:
    - Use `Related` to answer the `Question`.
    - If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
    - If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
    - Answer start with `according to your reading article`.

    If `Instruction` is a task:
    - Try to complete the task with `Last Response`.

    ===Last Response===
    {}

    ===Instruction===
    {}
    """.format(
        last_response, ins
    )

    return """You are a helpful AI assistant. 
    
    If `Instruction` is a question:
    - Use `Related` to answer the `Question`.
    - If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
    - If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
    - Answer start with `according to your reading article`.
    
    If `Instruction` is a task:
    - Try to complete the task with `Last Response`.
    
    ===Instruction===
    {}
    """.format(
        last_response, ins
    )

    return """You are a helpful AI assistant. Use `Related` to answer the `Question` at the end.
If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.

If you CAN answer, then answer start with `according to your reading article`.
If you CANNOT answer, you can try the question with `Last` response.

===Last===
{}

===Question===
{}
""".format(
        last_response, ins
    )


@router.post("/api/action/retrieve/generate")
async def generate(body: RetrieveBody, model: str = ""):
    assistant = ""
    user = ""
    uid = 0
    aid = 0
    for idx, m in enumerate(body.messages):
        if not m.enable:
            continue
        if m.role == RoleEnum.user:
            user = m.content
            uid = idx
        elif m.role == RoleEnum.assistant:
            assistant = m.content

    body.messages[uid].content = to_rag_message(user, assistant)
    ms = to_message(body.messages)

    data: Prompt = manager.get(body.name)
    # TODO: no retrieve in fact and just get all docs
    # from promptly.embed import retrieve
    # res = retrieve(user, data.docs)
    res = data.docs
    retrieved = to_retrieved(res)

    ms.insert(0, dict(role=RELATED_CONTENT_ROLE, content=retrieved))

    log.info(ms)

    content = await llm.chat(ms, model=model)
    log.info(content)

    mongo.history.push(CommitItem(messages=ms, response=content))
    return content
