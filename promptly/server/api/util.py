import fastapi
from pymongo import results


def check_mongo_result(res: results.UpdateResult):
    if not res.acknowledged:
        raise fastapi.HTTPException(404)

    # if res.modified_count <= 0 and res.matched_count<=0:
    #     raise fastapi.HTTPException(404)

    return True
