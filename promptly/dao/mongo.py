import collections
from collections.abc import Set
from typing import Dict, List, MutableSet

import loguru
from pymongo import MongoClient
from pymongo.collection import Collection

from promptly.dao.base import BaseCaseManager, BaseProfileManager
from promptly.model.case import Case
from promptly.model.prompt import Argument, ArgumentSetting, CommitItem, Prompt

url = "mongodb://localhost:27017/"

client = MongoClient(url)
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

    @staticmethod
    def default():
        return MongoManager(client)

    def reload(self):
        self.case.reload()
        self.prompt.reload()

    def rename(self, left, right):
        self.prompt.rename(left, right)
        self.commit.rename(left, right)
        self.argument.rename(left, right)


class MongoArgumentManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def add_value(self, name, key, value):
        res = self.collection.find_one({"name": name, "args.key": key})
        if not res:
            res = self.collection.update_one(
                {"name": name},
                {
                    "$push": {"args": {"key": key, "value": "", "candidates": [value]}},
                },
            )
        else:
            res = self.collection.update_one(
                {"name": name, "args.key": key},
                {
                    "$addToSet": {"args.$.candidates": value},
                },
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

    def rename(self, left, right):
        res = self.collection.update_one({"name": left}, {"$set": {"name": right}})
        log.info(res)


class MongoCommitManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def star(self, name, md5, value):
        res = self.collection.update_one(
            {"name": name, "commits": {"$elemMatch": {"md5": md5}}},
            {"$set": {"commits.$.star": value}},
        )
        return res

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

    def push(self, name: str, *args: CommitItem):
        data = dict(name=name)
        if args:
            data["commits"] = [c.dict() for c in args]

        res = self.collection.update_one(dict(name=name), {"$set": data}, upsert=True)

        return res

    def get(self, name: str) -> List[CommitItem]:
        res = self.collection.find_one(dict(name=name))
        if res:
            return [CommitItem(**i) for i in res["commits"]]
        return None

    def rename(self, left, right):
        res = self.collection.update_one({"name": left}, {"$set": {"name": right}})
        log.info(res)


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

        self.group: Dict[str, set] = collections.defaultdict(lambda: set())

        self.reload()

    def save(self):
        pass

    def reload(self):
        self.group.clear()
        for i in self.collection.find({}, {"name": 1, "group": 1}):
            s: set = self.group[i.get("group", "")]
            s.add(i["name"])

    def index(self):
        return self.group

    def get(self, key):
        for i in self.collection.find({"name": key}):
            return Prompt(**i)

    def update_args(self, key, args: List[Argument]):
        return self.collection.update_one(
            {"name": key}, {"$set": {"args": [a.dict() for a in args]}}
        )

    def update_history(self, p: Prompt):
        return self.collection.update_one(
            {"name": p.name}, {"$set": {"history": p.history}}
        )

    def update_prompt(self, p: Prompt):
        return self.collection.update_one(
            {"name": p.name}, {"$set": p.dict(by_alias=True)}
        )

    def add_prompt(self, p: Prompt):
        self.collection.insert_one(p.dict())

    def rename(self, left, right):
        res = self.collection.update_one({"name": left}, {"$set": {"name": right}})
        log.info(res)


def test_mongo_manager():
    m = MongoPromptManger(client)
    print(m.index)

    p = m.get("chat")
    print(p)

    p.remove(p.messages[-1].id)
    print(p)

    m.update_prompt(p)

    p = m.get("chat")
    print(p)
