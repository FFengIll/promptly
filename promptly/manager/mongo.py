from typing import Dict, List

import loguru
from pymongo import MongoClient
from pymongo.collection import Collection

from promptly.manager.base import BaseCaseManager, BaseProfileManager
from promptly.model.case import Case
from promptly.model.prompt import (
    Argument,
    ArgumentSetting,
    CommitItem,
    Prompt,
    PromptCommit,
)

log = loguru.logger


class MongoManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client["promptly"]

        self.prompt: MongoPromptManger = MongoPromptManger(self.db["prompt"])
        self.case: MongoCaseManager = MongoCaseManager(self.db["case"])
        self.history: MongoHistoryManager = MongoHistoryManager(self.db["history"])
        self.commit: MongoCommitManager = MongoCommitManager(self.db["commit"])
        self.argument: MongoArgumentManager = MongoArgumentManager(self.db["argument"])

    def reload(self):
        self.case.reload()
        self.prompt.reload()


class MongoArgumentManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def add_value(self, name, key, value):
        flatten_key = "args.{}".format(key)

        res = self.collection.update_one(
            {"name": name},
            {
                "$addToSet": {flatten_key: value},
                # "$set": {flatten_key: {"$ifNull": [flatten_key, []]}},
            },
            upsert=True,
        )
        return res

    def save_setting(self, s: ArgumentSetting):
        res = self.collection.update_one(
            {
                "name": s.name,
            },
            {"$set": s.dict()},
            upsert=True,
        )
        return res

    def get_setting(self, name):
        res = self.collection.find_one({"name": name})
        log.info(res)
        return ArgumentSetting(**res)


class MongoCommitManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def append_commit(self, name, commit: CommitItem):
        res = self.collection.update_one(
            {"name": name}, {"$push": {"commits": commit.dict()}}, upsert=True
        )
        return res

    def add_commit(self, name, commit: CommitItem):
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
            upsert=True,
        )
        return res

    def add_args(self, name, args: List[Argument]):
        res = self.collection.update_one(
            {"name": name},
            {"$push": {"cases": [a.dict() for a in args]}},
        )

        return res

    def update_args(self, name, args: List[Argument]):
        res = self.collection.update_one(
            {"name": name},
            {"$set": {"args": [a.dict() for a in args]}},
        )
        return res

    def push(self, project: PromptCommit):
        data = dict(name=project.name)
        if project.commits:
            data["commits"] = [c.dict() for c in project.commits]

        res = self.collection.update_one(
            dict(name=project.name), {"$set": data}, upsert=True
        )

        return res

    def get(self, name: str):
        res = self.collection.find_one(dict(name=name))
        if res:
            return PromptCommit(**res)
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

    def push(self, item: CommitItem):
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
            return Prompt(**i)

    def update_args(self, key, args: List[Argument]):
        self.collection.update_one(
            {"name": key}, {"$set": {"args": [a.dict() for a in args]}}
        )

    def update_history(self, p: Prompt):
        self.collection.update_one({"name": p.name}, {"$set": {"history": p.history}})

    def update_message(self, p: Prompt):
        messages = [m.dict() for m in p.messages]
        for idx, m in enumerate(messages):
            m["id"] = idx
        self.collection.update_one({"name": p.name}, {"$set": {"messages": messages}})

    def add_profile(self, p: Prompt):
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
