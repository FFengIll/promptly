import json
from typing import List
from uuid import uuid1

import loguru
import pickledb
from path import Path
from pydantic import BaseModel, Field

from prompt.model.event import UpdateEvent

log = loguru.logger


def generate_id():
    u = uuid1()
    return u.int


class Message(BaseModel):
    role: str
    content: str
    history: List[str] = Field(default_factory=list)
    id: int = Field(default_factory=generate_id)
    enable: bool = Field(default=True)
    order: int = Field(default=0)

    def __hash__(self):
        return self.id


class Profile(BaseModel):
    name: str = Field(default="")
    messages: List[Message]
    history: List[str] = Field(default_factory=set)

    @classmethod
    def generate_demo(cls):
        return Profile(
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


class ProfileManager:
    def __init__(self, path) -> None:
        self.path = path
        self.file_map = {}
        self.profiles = []

        self.load()

    def save(self):
        for path, profile in self.file_map.items():
            with open(path, "w") as fd:
                json.dump(profile.dict(), fd, indent=4, ensure_ascii=False)

    def load(self):
        path = self.path
        profiles = []
        location = {}
        for file in Path(path).listdir("*.json"):
            with open(file) as fd:
                obj = json.load(fd)
                profile = Profile.parse_obj(obj)
                for idx, m in enumerate(profile.messages):
                    m.order = idx

                name = file.basename().removesuffix(".json")
                profile.name = name

                profiles.append(profile)

                location[file] = profile

        profiles.sort(key=lambda p: p.name)

        self.file_map = location
        self.profiles = profiles

    def list_profile(self):
        return [p.name for p in self.profiles]

    def refresh(self):
        self.save()
        self.load()

    def get(
        self,
        key=None,
    ) -> Profile:
        return self.index.get(key, None)

    def update_all(self, key: str, ms: List[Message]):
        p: Profile = self.get(key)

        to_add = []
        for msg in ms:
            found = False
            for m in p.messages:
                if m.id == msg.id:
                    found = True
                    for k, v in msg.dict().items():
                        log.info("{}={}", k, v)
                        # FIXME: ignore any none data
                        m.__setattr__(k, v)

                    if msg.content not in p.history:
                        p.history.append(msg.content)
                    log.info(m)

            if not found:
                to_add.append(msg)

        p.messages.extend(to_add)
        p.messages.sort(key=lambda x: x.order)

    def update_one(self, key: str, msg: Message):
        p: Profile = self.get(key)
        found = False
        for m in p.messages:
            if m.id == msg.id:
                found = True
                for k, v in msg.dict().items():
                    log.info("{}={}", k, v)
                    # FIXME: ignore any none data
                    m.__setattr__(k, v)

                if msg.content not in m.history:
                    m.history.append(msg.content)
                log.info(m)

        p.messages.sort(key=lambda x: x.order)

    def update(self, name, events: List[UpdateEvent]):
        p: Profile = self.index[name]

        for e in events:
            for m in p.messages:
                if m.id == e.id:
                    if e.value not in m.history:
                        m.history.append(e.value)
                    m.content = e.value
                    break


class PickleProfileManager:
    def __init__(self, path):
        self.path = path
        self.db = pickledb.load(path, False)
        self.index = {k: Profile(**self.db.get(k)) for k in self.db.getall()}

    def list_profile(self):
        return list(self.index.keys())

    def get(self, name) -> Profile:
        res = self.db.get(name)
        if res:
            return Profile(**res)
        return None

    def add(self, name, profile: Profile = None):
        if not profile:
            profile = Profile.generate_demo()
        self.index[name] = profile

    def update(self, name, events: List[UpdateEvent]):
        p: Profile = self.index[name]

        for e in events:
            for m in p.messages:
                if m.id == e.id:
                    if e.value not in m.history:
                        m.history.append(e.value)
                    m.content = e.value
                    break

    def save(self):
        for k, v in self.index.items():
            self.db.set(k, v.dict())
        self.db.dump()


def test_pickledb():
    m = PickleProfileManager("../server/database.pickle.db")
    print(m.index)

    p = Profile(name="demo", messages=[Message(id=1, role="user", content="hello")])
    m.add("demo", p)

    m.save()


def test_update():
    m = ProfileManager("profile")

    e = UpdateEvent(id=1, value="test")
    m.update("demo", [e])

    print(m.index["demo"])


def test_profile():
    m = ProfileManager("profile")
    print(m.list_profile())

    for p in m.profiles:
        print(p)


def test_model():
    res = Profile.parse_obj(dict(name="", messages=[]))
    print(res)
