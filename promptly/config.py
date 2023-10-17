import os
from typing import ClassVar, List

import yaml
from pydantic import BaseModel, Field


class SystemConfigModel(BaseModel):
    __parsed: ClassVar["SystemConfigModel"] = None

    models: List[str] = []
    default_model: str = Field(alias="defaultModel", default="")
    api_key: str = ""
    api_base: str = ""

    @classmethod
    def singleton(cls) -> "SystemConfigModel":
        if not cls.__parsed:
            cls.__parsed = SystemConfigModel()
        return cls.__parsed

    @classmethod
    def parse_from(cls, file):
        with open(file) as fd:
            data = yaml.load(fd, yaml.SafeLoader)
            cls.__parsed = SystemConfigModel(**data)
        return cls.__parsed
