from typing import List

import fastapi
import loguru
import pydantic
from pydantic import BaseModel

from promptly.config import SystemConfigModel
from promptly.dao import MongoManager
from promptly.model.prompt import (
    ArgumentSetting,
)

log = loguru.logger

mongo = MongoManager.default()
manager = mongo.prompt
router = fastapi.APIRouter()


@router.get("/api/global/args", response_model=ArgumentSetting)
def get_global_argument():
    res = mongo.argument.get_setting("_global")
    return res


class ModelSetting(BaseModel):
    default_model: str = pydantic.Field(alias="defaultModel")
    models: List[str] = []


@router.get(
    "/api/global/models", response_model=ModelSetting, response_model_by_alias=True
)
def get_global_argument():
    res = ModelSetting(
        defaultModel=SystemConfigModel.singleton().default_model,
        models=SystemConfigModel.singleton().list_models(),
    )
    return res
