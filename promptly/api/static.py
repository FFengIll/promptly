import fastapi
import loguru
from fastapi import Request
from fastapi.templating import Jinja2Templates

log = loguru.logger

templates = Jinja2Templates(directory="./frontend/v2/dist")

router = fastapi.APIRouter()


@router.get("/view/{path:path}")
def view(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    # return RedirectResponse(url=app.url_path_for("/index.html"))
