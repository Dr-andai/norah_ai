import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.llm_document_summary import extract_text_from_pdf, extract_text_from_docx, query_llm

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, "../uploads"))
templates = Jinja2Templates(directory="app/templates")

@router.get("/summarize/protocol/{filename}", response_class=HTMLResponse)
def summarize_protocol(request: Request, filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Extract content based on file extension
    if filename.endswith(".pdf"):
        content = extract_text_from_pdf(filepath)
    elif filename.endswith(".docx") or filename.endswith(".doc"):
        content = extract_text_from_docx(filepath)
    else:
        return HTMLResponse(f"<div>❌ Unsupported file type for summarization: {filename}</div>")

    # Query the LLM with extracted content
    try:
        summary = query_llm(content)
    except Exception as e:
        summary = f"❌ LLM Error: {str(e)}"

    # Render the partial summary block
    return templates.TemplateResponse("partials/summary_block.html", {
        "request": request,
        "summary": summary
    })
