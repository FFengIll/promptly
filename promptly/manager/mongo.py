from pymongo import MongoClient
from pymongo.collection import Collection

from promptly.manager.base import BaseProfileManager, BaseCaseManager
from promptly.model.case import Case
from promptly.model.prompt import Profile, Snapshot, Project


class MongoManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client["promptly"]

        self.prompt: MongoPromptManger = MongoPromptManger(self.db["prompt"])
        self.case: MongoCaseManager = MongoCaseManager(self.db["case"])
        self.history: MongoHistoryManager = MongoHistoryManager(self.db["history"])
        self.commit: MongoIterationManager = MongoIterationManager(self.db["commit"])

    def reload(self):
        self.case.reload()
        self.prompt.reload()


class MongoIterationManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def push(self, project: Project):
        data = dict(name=project.name)
        if project.commits:
            data["commits"] = [c.dict() for c in project.commits]
        if project.args:
            data["args"] = [a.dict() for a in project.args]

        self.collection.update_one(dict(name=project.name), {"$set": data}, upsert=True)

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

    def push(self, item: Snapshot):
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

    def update_snapshot(self, p, snapshot: Snapshot):
        self.collection.update_one(
            {"name": p.name}, {"$push": {"snapshots": snapshot.dict()}}
        )

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
