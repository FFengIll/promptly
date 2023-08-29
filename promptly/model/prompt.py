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
    role: str
    content: str
    enable: bool = Field(default=True)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def __hash__(self):
        return self.id

    @classmethod
    def sample(cls):
        return Message(role="user", content="sample")


class Argument(BaseModel):
    key: str
    value: str


@autocomplete
class CommitItem(BaseModel):
    args: List[Argument] = Field(default_factory=list)
    messages: List[Message] = Field(default_factory=list)
    response: str = Field(default="")
    model: str = Field(default="")
    md5: str = Field(default="")

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
    name: str = Field(default="")
    model: str = Field(default="")
    messages: List[Message] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)

    @classmethod
    def sample(cls) -> "Prompt":
        return Prompt(name="sample", messages=[Message.sample()])

    @classmethod
    def generate_demo(cls):
        return Prompt(
            name="demo", messages=[Message(id=1, role="user", content="hello")]
        )

    def remove(self, id):
        found = None
        for i in self.messages:
            if i.id == id:
                found = i
                break
        if found:
            self.messages.remove(found)


def test_model():
    res = Prompt.parse_obj(dict(name="", messages=[]))
    print(res)


def test_json():
    for i in range(5):
        m = Message(role="1", content="123")
        print(m.json())


def test_commit():
    for i in range(5):
        c = CommitItem()
        print(c.md5)
