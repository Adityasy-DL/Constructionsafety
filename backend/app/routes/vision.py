from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from computer_vision.video_analyzer import analyze_video


router = APIRouter(
    prefix="/api/vision",
    tags=["Computer Vision"]
)

UPLOAD_DIR = Path("uploads/videos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/analyze-video")
async def analyze_video_endpoint(video: UploadFile = File(...)):

    file_path = UPLOAD_DIR / video.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    results = analyze_video(str(file_path))

    return {
        "filename": video.filename,
        "results": results
    }