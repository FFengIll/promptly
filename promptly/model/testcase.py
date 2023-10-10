from typing import List

import loguru
from pydantic import BaseModel, Field

log = loguru.logger


class TestCase(BaseModel):
    id: int = Field(default=0)
    name: str
    data: List[str] = Field(default_factory=list)
    description: str = Field(default="")

    def __hash__(self):
        return self.name.__hash__()


class TestResult(BaseModel):
    id: int
    source: str
    target: str
