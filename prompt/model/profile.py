from typing import List

import loguru
import pickledb
import toml
from path import Path
from pydantic import BaseModel, Field

from prompt.model.event import UpdateEvent

log = loguru.logger


class Message(BaseModel):
    role: str
    content: str
    history: List[str] = Field(default_factory=list)
    id: int
    enable: bool = Field(default=True)
    order: int = Field(default=0)


class Profile(BaseModel):
    name: str
    messages: List[Message]
    history: List[str] = Field(default_factory=list)

    @classmethod
    def generate_demo(cls):
        return Profile(
            name="demo", messages=[Message(id=1, role="user", content="hello")]
        )


class ProfileManager:
    def __init__(self, path) -> None:
        self.path = path
        self.file_map = {}
        self.profiles = []
        self.index = {}

        self.load()

    def load(self):
        path = self.path
        profiles = []
        file_map = {}
        for file in Path(path).listdir("*.toml"):
            with open(file) as fd:
                item = toml.load(fd)
                item = Profile.parse_obj(item)
                item.messages.sort(key=lambda x: x.order)
                profiles.append(item)
                file_map[item.name] = file

        self.file_map = file_map
        self.profiles = [i for i in profiles]

        self.index = {i.name: i for i in self.profiles}

    def list_profile(self):
        return list(self.index.keys())

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
        pending = []
        for msg in ms:
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

            if not found:
                pending.append(msg)
        p.messages.extend(pending)
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

    def save(self):
        for k, path in self.file_map.items():
            with open(path, "w") as fd:
                profile: Profile = self.index[k]
                toml.dump(profile.dict(), fd)

    def history(self, key, history):
        profile: Profile = self.index[key]
        profile.history.append(history)


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
