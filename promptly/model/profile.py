from typing import List, Any
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


class PromptItem(BaseModel):
    role: str
    content: str


@autocomplete
class Snapshot(BaseModel):
    prompt: List[PromptItem] = Field(default_factory=list)
    response: str = ""


@autocomplete
class Message(PromptItem):
    id: int = Field(default_factory=generate_id)
    enable: bool = Field(default=True)
    order: int = Field(default=0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.id = generate_id()

    def __hash__(self):
        return self.id

    @classmethod
    def sample(cls):
        return Message(role="user", content="sample")


@autocomplete
class Profile(BaseModel):
    name: str = Field(default="")
    messages: List[Message] = Field(default_factory=list)
    history: List[str] = Field(default_factory=list)
    snapshots: List[Snapshot] = Field(default_factory=list)

    def __init__(self, **data: Any):
        # compatibility
        snapshots = data["snapshots"]
        if snapshots:
            res = []
            for s in snapshots:
                log.info(s)
                if isinstance(s, List):
                    tmp = Snapshot()
                    tmp.prompt = s
                    res.append(tmp.dict())
                else:
                    res.append(s)
            data["snapshots"] = res

        super().__init__(**data)

    @classmethod
    def sample(cls) -> "Profile":
        return Profile(name="sample", messages=[Message.sample()])

    @classmethod
    def generate_demo(cls):
        return Profile(
            name="demo", messages=[Message(id=1, role="user", content="hello")]
        )

    def add_snapshot(self, s: Snapshot):
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
