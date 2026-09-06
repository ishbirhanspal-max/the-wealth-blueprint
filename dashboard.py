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

POSTS_DIR = os.path.join(BASE_DIR, "posts_15_days")
POSTS_VIDEOS_DIR = os.path.join(POSTS_DIR, "ready_videos")
os.makedirs(POSTS_VIDEOS_DIR, exist_ok=True)

app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
app.mount("/ready_videos", StaticFiles(directory=POSTS_VIDEOS_DIR), name="ready_videos")
app.mount("/posts_images", StaticFiles(directory=POSTS_DIR), name="posts_images")

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

@app.get("/api/posts_library")
def get_posts_library():
    items = []
    for day in range(1, 16):
        mp4_name = f"day{day:02d}_The_Wealth_Blueprint.mp4"
        mp4_path = os.path.join(POSTS_VIDEOS_DIR, mp4_name)
        img_name = f"day{day:02d}_render_day{day:02d}.png"
        seo_path = os.path.join(POSTS_VIDEOS_DIR, f"day{day:02d}_seo.json")
        seo_info = {}
        if os.path.exists(seo_path):
            with open(seo_path, "r", encoding="utf-8") as f:
                seo_info = json.load(f)
        items.append({
            "day": day,
            "ready": os.path.exists(mp4_path),
            "video_url": f"/ready_videos/{mp4_name}" if os.path.exists(mp4_path) else None,
            "image_url": f"/posts_images/{img_name}",
            "title": seo_info.get("title", f"Day {day:02d} Video"),
            "category": seo_info.get("category", "Finance"),
            "script": seo_info.get("script", ""),
            "youtube_description": seo_info.get("youtube_description", ""),
            "instagram_caption": seo_info.get("instagram_caption", "")
        })
    return items

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
