from typing import Dict

from path import Path
from tinydb import TinyDB, Query

from promptly.manager.base import BaseProfileManager
from promptly.model.profile import Profile, History


class TinyDBProfileManager(BaseProfileManager):
    def push_history(self, item: History):
        pass

    def __init__(self, path):
        super().__init__()

        base = Path(path)

        self.index: Dict[str, Profile] = {}

        self.db = TinyDB(base.joinpath("profile.json"))
        self.history_db = TinyDB(base.joinpath("history.json"))

        self.reload()

    def save(self):
        db = self.db
        self.db = None
        db.close()

    def reload(self):
        q: Profile = Query()
        res = self.db.search(q.name != "")

        for data in res:
            profile = Profile(**data)
            self.index[profile.name] = profile

    def keys(self):
        return list(self.index.keys())

    def get(self, key):
        p = self.index.get(key, None)
        return p

    def refresh(self):
        self.reload()


def test_tinydb():
    m = TinyDBProfileManager("db/tinydb/profile.json")
    m.db.insert(Profile.sample().dict())

    q: Profile = Query()
    res = m.db.search(q.name != "")
    for i in res:
        print(res)
