import json
from abc import ABC, abstractmethod
from typing import List

from path import Path

from promptly.manager.base import BaseProfileManager
from promptly.model.event import UpdateEvent
from promptly.model.profile import Profile, Message, History

import loguru

log = loguru.logger

class ProfileManager(BaseProfileManager):
    def __init__(self, path) -> None:
        self.path = path
        self.file_map = {}
        self.profiles: List[Profile] = []

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
        for p in self.profiles:
            if p.name == key:
                return p
        return None

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

    # def update(self, name, events: List[UpdateEvent]):
    #     p: Profile = self.index[name]
    #
    #     for e in events:
    #         for m in p.messages:
    #             if m.id == e.id:
    #                 if e.value not in m.history:
    #                     m.history.append(e.value)
    #                 m.content = e.value
    #                 break
    def push_history(self, item: History):
        pass


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