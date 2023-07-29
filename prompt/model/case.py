import json
from typing import List

import loguru
from path import Path
from pydantic import BaseModel, Field

log = loguru.logger


class Case(BaseModel):
    id: int = Field(default=0)
    name: str
    data: List[str]
    description: str = Field(default="")


class CaseManager:
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
        self.save()
        self.load()

    def get(self, key) -> Case:
        return self.index.get(key, None)
