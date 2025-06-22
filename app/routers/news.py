from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/api/news", response_class=HTMLResponse)
async def get_latest_news(request: Request):
    snippets = [
        "🧠 <strong>WHO (June 2024):</strong> Mental health services must integrate more digital-first tools for early detection.",
        "🧒 <strong>UNICEF (April 2024):</strong> Youth-focused mental health programs show 30% increase in service uptake.",
        "🌍 <strong>Dementia Update:</strong> Dementia cases expected to triple by 2050 — researchers urge for scalable community care strategies."
    ]
    return templates.TemplateResponse("partials/news_snippets.html", {
        "request": request,
        "snippets": snippets
    })
