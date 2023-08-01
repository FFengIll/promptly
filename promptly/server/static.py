from collections import defaultdict
from typing import Dict, List

import loguru
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from promptly.model.event import ActionEvent, UpdateEvent
from promptly.model.graph import Graph
from promptly.server.app import app

log = loguru.logger

templates = Jinja2Templates(directory="./promptly-vue/dist")


@app.get("/view/{path:path}")
def view(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    # return RedirectResponse(url=app.url_path_for("/index.html"))


# put this after all
app.mount("/", StaticFiles(directory="./promptly-vue/dist"), name="static")
