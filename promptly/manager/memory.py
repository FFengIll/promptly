import json
from typing import List

import loguru
from path import Path

from promptly.manager.base import BaseProfileManager, BaseCaseManager
from promptly.model.case import Case
from promptly.model.event import UpdateEvent
from promptly.model.prompt import Profile, Message, Snapshot

log = loguru.logger


class ProfileManager(BaseProfileManager):
    def __init__(self, path) -> None:
        self.path = path
        self.file_map = {}
        self.profiles: List[Profile] = []

        self.reload()

    def save(self):
        for path, profile in self.file_map.items():
            with open(path, "w") as fd:
                json.dump(profile.dict(), fd, indent=4, ensure_ascii=False)

    def reload(self):
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

    def keys(self):
        return [p.name for p in self.profiles]

    def refresh(self):
        self.save()
        self.reload()

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
    def push_history(self, item: Snapshot):
        pass


class CaseManager(BaseCaseManager):
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
        for file in Path(path).listdir("*.json"):
            with open(file) as fd:
                obj = json.load(fd)
                item: Case = Case.parse_obj(obj)
                profiles.append(item)
                file_map[item.id] = file

        self.file_map = file_map
        self.profiles = [i for i in profiles]

        self.index = {i.id: i for i in self.profiles}

    def keys(self):
        return list(self.index.keys())

    def values(self) -> List[Case]:
        return list(self.index.values())

    def refresh(self):
        pass
        # self.save()
        # self.load()

    def get(self, key) -> Case:
        return self.index.get(key, None)


def test_update():
    m = ProfileManager("profile")

    e = UpdateEvent(id=1, value="test")
    m.update("demo", [e])

    print(m.index["demo"])


def test_profile():
    m = ProfileManager("profile")
    print(m.keys())

    for p in m.profiles:
        print(p)
