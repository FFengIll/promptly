from typing import Optional

# One line of FastAPI imports here later 👈
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class ProfileDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int
    key: int = Field(index=True)
    role: str
    content: str
    history: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Code below omitted 👇
