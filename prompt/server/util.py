from typing import List

from prompt.model.profile import Message


def to_message(ms: List[Message]):
    res = []
    for i in ms:
        if i.enable:
            res.append(dict(role=i.role, content=i.content))
    return res
