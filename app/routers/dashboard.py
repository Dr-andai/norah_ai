from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/pm-dashboard", response_class=HTMLResponse)
def pm_dashboard(request: Request):
    try:
        project_data = json.load(open("data/mock_project_meta.json"))
    except Exception:
        project_data = []

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects": project_data,
        "role": "pm"
    })