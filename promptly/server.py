import fastapi
import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from promptly.api import action, case, config, embed, prompt, static
from promptly.dao.mongo import MongoManager

__all__ = ["app"]

log = loguru.logger

mongo = MongoManager.default()

api_router = fastapi.APIRouter()
api_router.include_router(case.router)
api_router.include_router(action.router)
api_router.include_router(prompt.router)
api_router.include_router(embed.router)
api_router.include_router(static.router)
api_router.include_router(config.router)

app = FastAPI()
app.include_router(api_router)


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


# put this after all
app.mount("/", StaticFiles(directory="./frontend/v2/dist"), name="static")
