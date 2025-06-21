from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os, shutil, json
from typing import Optional
from app.db.uploads_db import insert_upload_record, fetch_all_uploads, delete_upload_record
from app.services.llm_document_summary import extract_text_from_pdf, extract_text_from_docx, query_llm

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, "../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/files", response_class=HTMLResponse)
async def handle_upload(
    request: Request,
    notebook: Optional[UploadFile] = File(None),
    protocol: Optional[UploadFile] = File(None),
    sop: Optional[UploadFile] = File(None)
):
    uploaded_files = [(notebook, "notebook"), (protocol, "protocol"), (sop, "sop")]

    for file, label in uploaded_files:
        if file and file.filename:
            dest_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(dest_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            insert_upload_record(file.filename, label)

    return templates.TemplateResponse("partials/upload_success.html", {
        "request": request
    })

@router.get("/ds-dashboard", response_class=HTMLResponse)
def ds_dashboard(request: Request):
    try:
        project_data = json.load(open("data/mock_project_meta.json"))
    except Exception:
        project_data = []

    all_uploads = fetch_all_uploads()
    existing_uploads = []
    for file in all_uploads:
        filename = file[0]
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            existing_uploads.append(file)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects": project_data,
        "uploads": existing_uploads,
        "role": "ds"
    })

@router.get("/upload", response_class=HTMLResponse)
def upload_view(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/delete/file/{filename}", response_class=HTMLResponse)
async def delete_file(request: Request, filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Delete file from disk
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

    # Remove from DB
    delete_upload_record(filename)

    # Refresh dashboard
    project_data = json.load(open("data/mock_project_meta.json"))
    uploads = fetch_all_uploads()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects": project_data,
        "uploads": uploads,
        "role": "ds"
    })