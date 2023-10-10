import fastapi
import loguru

from promptly.dao.mongo import MongoCaseManager, MongoManager
from promptly.model.testcase import TestCase

log = loguru.logger
mongo = MongoManager.default()
manager: MongoCaseManager = mongo.case
router = fastapi.APIRouter()


@router.get("/api/case")
def list_case(reload: bool):
    if reload:
        manager.reload()
    return manager.keys()


@router.get("/api/case/{key}", response_model=TestCase)
async def get_case(key: str):
    c: TestCase = manager.get(key)
    log.info(c)
    if not c:
        raise fastapi.HTTPException(404)
    return c
