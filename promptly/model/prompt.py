from hashlib import md5
from typing import Any, Dict, List
from uuid import uuid1

import loguru
from pydantic import BaseModel, Field

from promptly.schema import autocomplete

log = loguru.logger


def generate_id():
    u = uuid1()

    # 转换为字节对象
    uuid_bytes = u.bytes

    # 取前8个字节
    trimmed_bytes = uuid_bytes[:8]

    return int.from_bytes(trimmed_bytes, byteorder="big")


@autocomplete
class Message(BaseModel):
    role: str = ...
    content: str = ...
    enable: bool = False

    @classmethod
    def sample(cls):
        return Message(role="user", content="sample")


class Argument(BaseModel):
    key: str
    value: str


@autocomplete
class CommitItem(BaseModel):
    args: List[Argument] = Field(default_factory=list)
    messages: List[Message] = ...
    response: str = ""
    model: str = ""
    md5: str = ""
    star: bool = False
    tag: str = ""

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.md5 = self.calc_md5()

    def calc_md5(self):
        items = [m.json() for m in self.messages]
        h = md5()

        # firstly, process model
        h.update(self.model.encode())

        # then for the messages
        for it in items:
            h.update(it.encode())

        # done
        return h.hexdigest()


class ArgumentSetting(BaseModel):
    name: str
    args: Dict[str, List[str]] = Field(default_factory=dict)


@autocomplete
class Prompt(BaseModel):
    name: str = ...
    model: str = Field(default="")
    messages: List[Message] = ...
    history: List[str] = Field(default_factory=list)

    def __init__(self, **kwargs):
        messages = kwargs.pop("messages", list())
        super().__init__(messages=messages, **kwargs)

    @classmethod
    def sample(cls) -> "Prompt":
        return Prompt(name="sample", messages=[Message.sample()])

    @classmethod
    def generate_demo(cls):
        return Prompt(
            name="demo", messages=[Message(id=1, role="user", content="hello")]
        )
