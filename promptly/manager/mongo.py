from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection

from promptly.manager.base import BaseCaseManager, BaseProfileManager
from promptly.model.case import Case
from promptly.model.prompt import Argument, Commit, Profile, Project


class MongoManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client["promptly"]

        self.prompt: MongoPromptManger = MongoPromptManger(self.db["prompt"])
        self.case: MongoCaseManager = MongoCaseManager(self.db["case"])
        self.history: MongoHistoryManager = MongoHistoryManager(self.db["history"])
        self.commit: MongoCommitManager = MongoCommitManager(self.db["commit"])

    def reload(self):
        self.case.reload()
        self.prompt.reload()


class MongoCommitManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def append_commit(self, name, commit: Commit):
        res = self.collection.update_one(
            {"name": name}, {"$push": {"commits": commit.dict()}}, upsert=True
        )
        return res.acknowledged

    def add_commit(self, name, commit: Commit):
        res = self.collection.update_one(
            {"name": name},
            {
                "$push": {
                    "commits": {
                        "$each": [commit.dict()],
                        "$position": 0,
                    }
                }
            },
        )
        return res.acknowledged

    def add_args(self, name, args: List[Argument]):
        res = self.collection.update_one(
            {"name": name},
            {"$push": {"cases": [a.dict() for a in args]}},
        )

        return res.acknowledged

    def update_args(self, name, args: List[Argument]):
        res = self.collection.update_one(
            {"name": name},
            {"$set": {"args": [a.dict() for a in args]}},
        )
        return res.acknowledged

    def push(self, project: Project):
        data = dict(name=project.name)
        if project.commits:
            data["commits"] = [c.dict() for c in project.commits]
        if project.args:
            data["args"] = [a.dict() for a in project.args]

        res = self.collection.update_one(
            dict(name=project.name), {"$set": data}, upsert=True
        )

        return res.acknowledged

    def get(self, name: str):
        res = self.collection.find_one(dict(name=name))
        if res:
            return Project(**res)
        return None


class MongoCaseManager(BaseCaseManager):
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

        self.reload()

    def reload(self):
        self.index.clear()
        for i in self.collection.find({}, {"name": 1, "description": 1}):
            self.index.add(Case(**i))

    def keys(self):
        return list(self.index)

    def get(self, key):
        for i in self.collection.find({"name": key}):
            return Case(**i)
        return None


class MongoHistoryManager:
    def __init__(self, col: Collection):
        self.collection = col

    def push(self, item: Commit):
        self.collection.insert_one(item.dict())


class MongoPromptManger(BaseProfileManager):
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

        self.reload()

    def save(self):
        pass

    def reload(self):
        self.index.clear()
        for i in self.collection.find({}, {"name": 1}):
            self.index.add(i["name"])

    def keys(self):
        return list(self.index)

    def get(self, key):
        for i in self.collection.find({"name": key}):
            return Profile(**i)

    def update_history(self, p: Profile):
        self.collection.update_one({"name": p.name}, {"$set": {"history": p.history}})

    def update_message(self, p: Profile):
        messages = [m.dict() for m in p.messages]
        for idx, m in enumerate(messages):
            m["id"] = idx
        self.collection.update_one({"name": p.name}, {"$set": {"messages": messages}})



    def add_profile(self, p: Profile):
        self.collection.insert_one(p.dict())


def test_mongo_manager():
    from promptly.orm.mongo import client

    m = MongoPromptManger(client)
    print(m.index)

    p = m.get("chat")
    print(p)

    p.remove(p.messages[-1].id)
    print(p)

    m.update_message(p)

    p = m.get("chat")
    print(p)
