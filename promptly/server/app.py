import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from promptly.dao.mongo import client,MongoManager

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


@app.get("/api/ping")
def ping():
    return "pong"
