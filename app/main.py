import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import upload, dashboard, home, summarize
from app.db.uploads_db import init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(home.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(summarize.router)

init_db()