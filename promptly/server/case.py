import fastapi
import loguru

from promptly.manager.memory import CaseManager
from promptly.manager.mongo import MongoCaseManager
from promptly.model.case import Case
from promptly.server.app import app, mongo

log = loguru.logger
manager: MongoCaseManager = mongo.case


@app.get("/api/case")
def list_case(reload: bool):
    if reload:
        manager.reload()
    return manager.keys()


@app.get("/api/case/{key}")
async def get_case(key: str):
    c: Case = manager.get(key)
    log.info(c)
    if not c:
        raise fastapi.HTTPException(404)
    return c.dict()
