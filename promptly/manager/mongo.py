from pymongo import MongoClient

from promptly.manager.base import BaseProfileManager, BaseCaseManager
from promptly.model.profile import  Profile, Snapshot


class MongoProfileManger(BaseProfileManager):
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client["promptly"]
        self.c_profile = self.db["profile"]
        self.c_history = self.db['history']

        self.index = set()

        self.reload()

    def save(self):
        pass

    def reload(self):
        self.index.clear()
        for i in self.c_profile.find({}, {"name": 1}):
            self.index.add(i["name"])

    def list_profile(self):
        return list(self.index)

    def get_profile(self, key):
        for i in self.c_profile.find({"name": key}):
            return Profile(**i)

    def push_history(self, item: Snapshot):
        self.c_history.insert_one(item.dict())

    def update_message(self, p:Profile):
        messages = [m.dict() for m in p.messages]
        for idx, m in enumerate(messages):
            m['id'] = idx
        self.c_profile.update_one({'name':p.name}, {'$set' :{'messages':messages}})

    def update_snapshot(self, p, snapshot:Snapshot):
        self.c_profile.update_one(
            {'name':p.name},
            {
                '$push' :{'snapshots': snapshot.dict() }
             }
        )

    def add_profile(self, p:Profile):
        self.c_profile.insert_one(p.dict())


class MongoCaseManager(BaseCaseManager):
    def __init__(self):
        pass

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
