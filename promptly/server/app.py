import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from promptly.manager import MongoManager
from promptly.manager.memory import CaseManager
from promptly.orm.mongo import client

log = loguru.logger

mongo = MongoManager(client)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
