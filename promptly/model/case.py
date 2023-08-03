from typing import List

import loguru
from pydantic import BaseModel, Field

log = loguru.logger


class Case(BaseModel):
    id: int = Field(default=0)
    name: str
    data: List[str]
    description: str = Field(default="")
