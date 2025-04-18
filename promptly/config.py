import os
from typing import ClassVar, List

import yaml
from pydantic import BaseModel, Field


class ProviderModel(BaseModel):
    name: str = ""
    api_base: str = ""
    api_key: str = ""
    models: List[str] = []
    proxy: str = ""


class SystemConfigModel(BaseModel):
    __parsed: ClassVar["SystemConfigModel"] = None

    models: List[str] = []
    default_model: str = Field(alias="default_model", default="")
    api_key: str = ""
    api_base: str = ""
    providers: List[ProviderModel] = []
    file: str = ""

    def get_provider(self, model):
        for provider in self.providers:
            if model in provider.models:
                return provider
        return None

    def list_models(self):
        models = []
        for provider in self.providers:
            models.extend(provider.models)
        return models

    @classmethod
    def singleton(cls) -> "SystemConfigModel":
        return cls.__parsed

    @classmethod
    def parse_from(cls, file):
        with open(file) as fd:
            data = yaml.load(fd, yaml.SafeLoader)
            cls.__parsed = SystemConfigModel(**data)
        cls.__parsed.file = file
        return cls.__parsed
