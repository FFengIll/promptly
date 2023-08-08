from typing import List

import pickledb

from promptly.model.event import UpdateEvent
from promptly.model.profile import Profile, Message


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
