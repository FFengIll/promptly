from typing import Optional

# One line of FastAPI imports here later 👈
from sqlmodel import Field, SQLModel, create_engine


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int
    content: str


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int
    role: str
    content: str
    enable: bool
    order: int


class Snapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Code below omitted 👇
