from fastapi import APIRouter, UploadFile, File, Form
from pipeline import process_pipeline
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"status": "success", "file_path": file_path}

@router.post("/process")
async def process_media(file_path: str = Form(...)):
    """Runs full CNN → OCR → Transcription → Summary pipeline"""
    summary = process_pipeline(file_path)
    return {"status": "completed", "summary": summary}

@router.post("/youtube")
async def process_youtube(url: str = Form(...)):
    """(Optional) Process YouTube URL in future"""
    return {"message": f"YouTube URL {url} received. Will process soon."}
