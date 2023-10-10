import collections
from typing import Dict, List

import loguru
from pydantic_mongo import AbstractRepository
from pymongo import MongoClient
from pymongo.collection import Collection

from promptly.model.testcase import TestCase
from promptly.model.prompt import Argument, ArgumentSetting, CommitItem, Prompt

url = "mongodb://localhost:27017/"

client = MongoClient(url, timeoutMS=1000)
log = loguru.logger


class MongoManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = client["promptly"]

        self.prompt: MongoPromptManger = MongoPromptManger(self.db["prompt"], self.db)
        self.case: MongoCaseManager = MongoCaseManager(self.db["case"])
        self.history: MongoHistoryManager = MongoHistoryManager(self.db["history"])
        self.commit: MongoCommitManager = MongoCommitManager(self.db["commit"])
        self.argument: MongoArgumentManager = MongoArgumentManager(self.db["argument"])
        self.embed: MongoEmbedManager = MongoEmbedManager(self.db["prompt"])

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


class MongoEmbedManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

    def get(self, name):
        res = self.collection.find_one({"name": name})
        return EmbedData(**res)


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

    def set_values(self, name, key, *values):
        res = self.collection.find_one({"name": name, "args.key": key})
        if not res:
            res = self.collection.update_one(
                {"name": name},
                {
                    "$set": {"args": [{"key": key, "value": "", "candidates": values}]},
                },
                upsert=True,
            )
        else:
            res = self.collection.update_one(
                {"name": name, "args.key": key},
                {
                    "$set": {"args.$.candidates": values},
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
        if not res:
            return ArgumentSetting(name=name)
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


class MongoCaseManager:
    def __init__(self, col: Collection):
        self.collection = col

        self.index = set()

        self.reload()

    def reload(self):
        self.index.clear()
        for i in self.collection.find({}, {"name": 1, "description": 1}):
            self.index.add(TestCase(**i))

    def keys(self):
        return list(self.index)

    def get(self, key):
        for i in self.collection.find({"name": key}):
            return TestCase(**i)
        return None


class MongoHistoryManager:
    def __init__(self, col: Collection):
        self.collection = col

    def push(self, item: CommitItem):
        self.collection.insert_one(item.dict())


class PromptODM(AbstractRepository[Prompt]):
    class Meta:
        collection_name = "prompt"


class MongoPromptManger:
    def __init__(self, col: Collection, database):
        self.collection = col

        # FIXME: DO NOT use it since `swagger-codegen` error.
        # self.odm = PromptODM(database=database)

        self.group: Dict[str, set] = collections.defaultdict(lambda: set())
        self.values = []

        self.reload()

    def save(self):
        pass

    def reload(self):
        self.group.clear()
        for i in self.collection.find({}, {"_id": 1, "name": 1, "group": 1}):
            s: set = self.group[i.get("group", "")]
            s.add(i["name"])

    def index(self):
        return self.group

    def get(self, key):
        res = self.collection.find_one(
            {"name": key},
        )
        if not res:
            return None
        return Prompt(**res)
        # return self.odm.find_one_by({"name": key})

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
