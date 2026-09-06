import os
import sys
import json
import time
import shutil
import subprocess
import imageio_ffmpeg

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from generator import generate_script
from composer import compose_video

# Directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input_videos")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed_videos")
PUBLISHED_DIR = os.path.join(BASE_DIR, "published_videos")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(PUBLISHED_DIR, exist_ok=True)

def generate_video_seo(video_name: str, transcript_summary: str = "", gemini_key: str = None) -> dict:
    """
    Generates high-ranking, algorithm-optimized SEO metadata for YouTube & Instagram.
    """
    clean_name = os.path.splitext(video_name)[0].replace("_", " ").replace("-", " ")
    
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            You are a world-class YouTube Shorts and Instagram Reels SEO growth strategist.
            Generate viral SEO metadata for a video titled/about: "{clean_name}".
            Context / Transcript: "{transcript_summary}"

            Respond strictly in valid JSON format with:
            - "youtube_title": Ultra-clickable hook title under 65 chars with 1 emoji and #Shorts.
            - "youtube_description": High-SEO description with keywords, bullet points, and CTA for link in bio.
            - "youtube_tags": Array of 15 high-volume search tags.
            - "youtube_pinned_comment": High-converting pinned comment directing to bio link.
            - "instagram_caption": Engaging 3-line Instagram caption with spacing.
            - "instagram_hashtags": 15 high-ranking niche hashtags.
            """
            response = model.generate_content(prompt)
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:-3].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:-3].strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"[Warning] AI SEO fallback triggered: {e}")
            
    # Pro Template SEO fallback based on filename keywords
    is_finance = any(w in clean_name.lower() for w in ["money", "credit", "bank", "wealth", "invest", "rich", "cash", "finance"])
    if is_finance:
        return {
            "youtube_title": f"{clean_name.title()} 💳 (Don't Ignore This) #Shorts",
            "youtube_description": f"Here is what the banking system doesn't teach you about {clean_name}.\n\n📌 Free Wealth-Building Checklist in Bio!\n\n#personalfinance #moneytips #financialfreedom #wealthhabits #investing",
            "youtube_tags": ["shorts", "personal finance", "money hacks", "investing", "wealth habits", "credit score", "passive income"],
            "youtube_pinned_comment": "💳 Grab the free wealth acceleration guide linked in my bio!",
            "instagram_caption": f"The financial system isn't designed to teach you this. 🏦\n\nSave this reel before you forget!\n\nCheck the link in bio for the complete roadmap 📊",
            "instagram_hashtags": "#personalfinance #moneyhacks #wealthmindset #financialeducation #investing101 #richhabits #sidehustle"
        }
    else:
        return {
            "youtube_title": f"Stop Doing This Manually 🛑 ({clean_name.title()}) #Shorts",
            "youtube_description": f"How to automate your workflow using this secret shortcut for {clean_name}.\n\n⚡ 40+ Secret Productivity Tools in Bio!\n\n#productivity #aitools #techhacks #lifehacks #shortcuts",
            "youtube_tags": ["shorts", "tech hacks", "ai tools", "productivity", "life hacks", "software", "student hacks"],
            "youtube_pinned_comment": "🤖 Grab the free 40+ AI & Productivity Tools cheat sheet in my bio!",
            "instagram_caption": f"If you're still doing this manually in 2026, you're losing hours. ⏳\n\nComment 'TOOL' below and I'll DM you the link directly! 🚀",
            "instagram_hashtags": "#aitools #productivityhacks #freewebsites #techtrends #lifehacks #studentlife #worksmart"
        }

def process_and_upload(video_path: str, upload_to_youtube: bool = True):
    """Processes a single video file, performs SEO, and uploads it."""
    filename = os.path.basename(video_path)
    print(f"\n============================================================")
    print(f">> PROCESSING NEW VIDEO: {filename}")
    print(f"============================================================")
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    # 1. Generate SEO
    print(">> [1/3] Generating High-Ranking SEO & Metadata...")
    seo_data = generate_video_seo(filename, gemini_key=gemini_key)
    print(f"   Title: {seo_data['youtube_title']}")
    print(f"   Tags: {', '.join(seo_data['youtube_tags'][:5])}...")
    
    # Save SEO package alongside video
    seo_output_path = os.path.join(PROCESSED_DIR, f"{os.path.splitext(filename)[0]}_seo.json")
    with open(seo_output_path, "w", encoding="utf-8") as f:
        json.dump(seo_data, f, indent=2)
    print(f"[OK] SEO package saved to: {seo_output_path}")
    
    # 2. Upload to YouTube Shorts
    if upload_to_youtube:
        print("\n>> [2/3] Uploading to YouTube Shorts...")
        try:
            from youtube_uploader import upload_short_to_youtube
            yt_url = upload_short_to_youtube(
                video_path=video_path,
                title=seo_data["youtube_title"],
                description=seo_data["youtube_description"],
                tags=seo_data["youtube_tags"],
                pinned_comment=seo_data["youtube_pinned_comment"]
            )
            print(f"[SUCCESS] Uploaded to YouTube: {yt_url}")
            seo_data["youtube_url"] = yt_url
        except Exception as e:
            print(f"[Notice] YouTube upload pending API authorization: {e}")
            print("         (Video and SEO package are prepared and ready to publish!)")
            
    # 3. Move video to published archive
    dest_path = os.path.join(PUBLISHED_DIR, filename)
    shutil.move(video_path, dest_path)
    print(f"\n>> [3/3] Video moved to archive: {dest_path}")
    print("============================================================\n")

def watch_folder(poll_interval: int = 5):
    """Watches input_videos/ directory and processes any video dropped in."""
    print(f"👀 WATCHING FOLDER FOR NEW VIDEOS: {INPUT_DIR}")
    print("👉 Simply drop any .mp4 or .mov file into this folder!")
    print("   Press Ctrl+C to stop.\n")
    
    valid_exts = (".mp4", ".mov", ".mkv", ".webm")
    
    while True:
        try:
            files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_exts)]
            for f in files:
                full_path = os.path.join(INPUT_DIR, f)
                # Wait briefly to ensure file is completely written/copied
                initial_size = os.path.getsize(full_path)
                time.sleep(1.5)
                if os.path.exists(full_path) and os.path.getsize(full_path) == initial_size:
                    process_and_upload(full_path)
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\nStopped watching folder.")
            break
        except Exception as e:
            print(f"Error during folder scan: {e}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    watch_folder()
