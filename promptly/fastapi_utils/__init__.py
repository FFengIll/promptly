import re
from functools import partial
from typing import ClassVar

import pydantic
from pydantic import BaseConfig, BaseModel


def snake2camel(snake: str, start_lower: bool = False) -> str:
    """
    Converts a snake_case string to camelCase.

    The `start_lower` argument determines whether the first letter in the generated camelcase should
    be lowercase (if `start_lower` is True), or capitalized (if `start_lower` is False).
    """
    camel = snake.title()
    camel = re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)
    if start_lower:
        camel = re.sub("(^_*[A-Z])", lambda m: m.group(1).lower(), camel)
    return camel


def camel2snake(camel: str) -> str:
    """
    Converts a camelCase string to snake_case.
    """
    snake = re.sub(r"([a-zA-Z])([0-9])", lambda m: f"{m.group(1)}_{m.group(2)}", camel)
    snake = re.sub(r"([a-z0-9])([A-Z])", lambda m: f"{m.group(1)}_{m.group(2)}", snake)
    return snake.lower()


class APIModel(BaseModel):
    """
    Intended for use as a base class for externally-facing models.

    Any models that inherit from this class will:
    * accept fields using snake_case or camelCase keys
    * use camelCase keys in the generated OpenAPI spec
    * have orm_mode on by default
        * Because of this, FastAPI will automatically attempt to parse returned orm instances into the model
    """

    config: ClassVar = pydantic.ConfigDict(
        populate_by_name=True,
        alias_generator=partial(snake2camel, start_lower=True),
    )


class APIMessage(APIModel):
    """
    A lightweight utility class intended for use with simple message-returning endpoints.
    """

    detail: str
