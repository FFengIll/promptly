from typing import List
from uuid import uuid1

import loguru
from pydantic import BaseModel, Field

from promptly.schema import autocomplete

log = loguru.logger


def generate_id():
    u = uuid1()
    return u.int


class PromptItem(BaseModel):
    role: str
    content: str


@autocomplete
class Message(PromptItem):
    history: List[str] = Field(default_factory=list)
    id: int = Field(default_factory=generate_id)
    enable: bool = Field(default=True)
    order: int = Field(default=0)

    def __hash__(self):
        return self.id

    @classmethod
    def sample(cls):
        return Message(role="user", content="sample")


@autocomplete
class Profile(BaseModel):
    name: str = Field(default="")
    messages: List[Message]
    history: List[str] = Field(default_factory=list)
    snapshots: List[List[PromptItem]] = Field(default_factory=list)

    @classmethod
    def sample(cls) -> "Profile":
        return Profile(name="sample", messages=[Message.sample()])

    @classmethod
    def generate_demo(cls):
        return Profile(
            name="demo", messages=[Message(id=1, role="user", content="hello")]
        )

    def add_snapshot(self, s: List[PromptItem]):
        self.snapshots.append(s)

    def remove(self, id):
        found = None
        for i in self.messages:
            if i.id == id:
                found = i
                break
        if found:
            self.messages.remove(found)


@autocomplete
class History(BaseModel):
    prompt: List[PromptItem] = Field(default_factory=List)
    response: str = ""


def test_model():
    res = Profile.parse_obj(dict(name="", messages=[]))
    print(res)
