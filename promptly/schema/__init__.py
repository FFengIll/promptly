from pydantic import BaseModel, Field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import dataclass
else:

    def dataclass(model):
        return model


autocomplete = dataclass
