import os
import json
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from main import run_pipeline

app = FastAPI(title="Autopilot Shorts & Reels Creator")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
WEB_DIR = os.path.join(BASE_DIR, "web")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)

app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

class GenerateRequest(BaseModel):
    niche: str = "finance"
    voice: str = "en-US-ChristopherNeural"
    gemini_key: str = ""
    pexels_key: str = ""

@app.get("/")
def get_dashboard():
    index_file = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Web UI initializing. Please refresh in a moment."}

@app.get("/bio")
def get_bio_page():
    bio_file = os.path.join(WEB_DIR, "bio_landing_page.html")
    if os.path.exists(bio_file):
        return FileResponse(bio_file)
    return {"message": "Bio page initializing."}

@app.get("/api/latest")
def get_latest():
    meta_path = os.path.join(OUTPUT_DIR, "latest_metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["video_url"] = "/output/latest_short.mp4"
            return data
    sample_mp4 = os.path.join(OUTPUT_DIR, "sample_short.mp4")
    if os.path.exists(sample_mp4):
        return {
            "title": "The Rule of 72: How Billionaires Double Wealth #Shorts",
            "description": "Double your wealth with compound interest.\n#investing #finance",
            "pinned_comment": "📈 Grab the free investing sheet linked in my bio!",
            "video_url": "/output/sample_short.mp4",
            "duration": 15.0,
            "niche": "finance"
        }
    return {"message": "No video generated yet"}

@app.post("/api/generate")
def generate_video(req: GenerateRequest):
    if req.gemini_key:
        os.environ["GEMINI_API_KEY"] = req.gemini_key
    if req.pexels_key:
        os.environ["PEXELS_API_KEY"] = req.pexels_key
        
    out_file = os.path.join(OUTPUT_DIR, "latest_short.mp4")
    res = run_pipeline(niche=req.niche, voice=req.voice, output_path=out_file)
    res["video_url"] = "/output/latest_short.mp4"
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard:app", host="127.0.0.1", port=8000, reload=False)
