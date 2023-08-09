import json

import toml
import typer
from path import Path
from tinydb import Query

from promptly.manager import ProfileManager
from promptly.manager.memory import CaseManager
from promptly.model.profile import Profile


def migrate_0729(base: str):
    for file in Path(base).listdir("*.toml"):
        with open(file) as fd:
            item = toml.load(fd)
            profile: Profile = Profile.parse_obj(item)
            for m in profile.messages:
                profile.history.extend(m.history)
                m.history.clear()

        json_file = Path(base).joinpath(file.with_suffix(".json").basename())
        with open(json_file, "w") as fd:
            json.dump(profile.dict(), fd, indent=4, ensure_ascii=False)


def migrate_0803_09(input: str, output: str):
    from promptly.manager.tinydb import TinyDBProfileManager

    left = ProfileManager(input)
    right = TinyDBProfileManager(output)

    for p in left.profiles:
        q: Profile = Query()
        right.db.upsert(p.dict(), q.name == p.name)


def migrate_0803_12(input: str):
    left = ProfileManager(input)

    from promptly.orm.mongo import client

    db = client["promptly"]
    c_profile = db["profile"]
    for p in left.profiles:
        c_profile.insert_one(p.dict())


def migrate_case_0804_14(input: str):
    left = CaseManager(input)

    from promptly.orm.mongo import client

    db = client["promptly"]
    c_case = db["case"]
    for p in left.profiles:
        c_case.insert_one(p.dict())


if __name__ == "__main__":
    typer.run(migrate_case_0804_14)
