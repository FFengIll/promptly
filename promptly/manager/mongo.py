from typing import List

from pymongo import MongoClient

from promptly.manager.base import BaseProfileManager
from promptly.model.profile import History, Profile, PromptItem


class MongoProfileManger(BaseProfileManager):
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client["promptly"]
        self.c_profile = self.db["profile"]

        self.index = set()

        self.reload()

    def save(self):
        pass

    def reload(self):
        for i in self.c_profile.find({}, {"name": 1}):
            self.index.add(i["name"])

    def list_profile(self):
        return list(self.index)

    def get_profile(self, key):
        for i in self.c_profile.find({"name": key}):
            return Profile(**i)

    def push_history(self, item: History):
        pass

    def update_message(self, p:Profile):
        messages = [m.dict() for m in p.messages]
        for idx, m in enumerate(messages):
            m['id'] = idx
        self.c_profile.update_one({'name':p.name}, {'$set' :{'messages':messages}})

    def update_snapshot(self, p, snapshot:List[PromptItem]):
        res  =[i.dict() for i in snapshot]
        self.c_profile.update_one({'name':p.name}, {'$push' :{'snapshots': res }})


def test_mongo_manager():
    from promptly.orm.mongo import client

    m = MongoProfileManger(client)
    print(m.index)

    p = m.get_profile("chat")
    print(p)

    p.remove(p.messages[-1].id)
    print(p)

    m.update_message(p)

    p = m.get_profile("chat")
    print(p)
