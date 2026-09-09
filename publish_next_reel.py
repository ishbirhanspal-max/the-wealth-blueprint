import os
import sys
import json
import glob
import re
from datetime import datetime
from instagrapi import Client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(BASE_DIR, "meta_bulk_upload_package")
HISTORY_FILE = os.path.join(BASE_DIR, "published_videos", "published_history.json")
SESSION_FILE = os.path.join(BASE_DIR, "ig_session.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_next_unpublished_package_reel():
    history = load_history()
    published_ig_ids = {
        h.get("id") for h in history 
        if h.get("instagram_status") == "PUBLISHED" or h.get("instagram_url")
    }

    mp4_files = sorted(glob.glob(os.path.join(PACKAGE_DIR, "Reel_*_*.mp4")))
    for mp4 in mp4_files:
        fname = os.path.basename(mp4)
        m = re.match(r"Reel_(\d+)_", fname)
        if m:
            r_id = int(m.group(1))
            if r_id not in published_ig_ids:
                base_name = os.path.splitext(fname)[0]
                caption_file = os.path.join(PACKAGE_DIR, f"{base_name}_caption.txt")
                thumb_file = os.path.join(PACKAGE_DIR, f"{base_name}_thumb.jpg")
                return {
                    "id": r_id,
                    "mp4": mp4,
                    "caption_file": caption_file if os.path.exists(caption_file) else None,
                    "thumb_file": thumb_file if os.path.exists(thumb_file) else None,
                    "name": fname
                }
    return None

def publish_reel(item: dict):
    r_id = item["id"]
    print(f"\n========================================================")
    print(f">> PUBLISHING REEL #{r_id:02d} TO INSTAGRAM: {item['name']}")
    print(f"========================================================")

    caption = ""
    if item["caption_file"] and os.path.exists(item["caption_file"]):
        with open(item["caption_file"], "r", encoding="utf-8") as f:
            caption = f.read().strip()

    if not caption:
        caption = f"The Wealth Blueprint - Reel #{r_id:02d}\n\nFollow @thewealthblueprint10 for daily wealth loopholes!"

    cl = Client()
    if not os.path.exists(SESSION_FILE):
        raise RuntimeError("ig_session.json not found! Please ensure your session is active.")
    
    cl.load_settings(SESSION_FILE)
    u = cl.account_info()
    print(f">> Authenticated as @{u.username}")
    print(f">> Uploading video ({os.path.getsize(item['mp4']) / (1024*1024):.2f} MB)...")

    media = cl.clip_upload(
        path=item["mp4"],
        caption=caption,
        thumbnail=item["thumb_file"]
    )

    reel_url = f"https://www.instagram.com/reel/{media.code}/"
    print(f">> [SUCCESS] Reel #{r_id:02d} is LIVE on Instagram!")
    print(f">> URL: {reel_url}")

    # Update history
    history = load_history()
    found = False
    for h in history:
        if h.get("id") == r_id:
            h["instagram_url"] = reel_url
            h["instagram_status"] = "PUBLISHED"
            h["instagram_published_at"] = datetime.now().isoformat()
            found = True
            break
    if not found:
        history.append({
            "id": r_id,
            "title": item["name"],
            "timestamp": datetime.now().isoformat(),
            "instagram_url": reel_url,
            "instagram_status": "PUBLISHED",
            "instagram_published_at": datetime.now().isoformat()
        })
    save_history(history)
    return reel_url

if __name__ == "__main__":
    next_reel = get_next_unpublished_package_reel()
    if not next_reel:
        print(">> All 15 package reels have been published to Instagram!")
    else:
        print(f">> Next reel in queue: #{next_reel['id']:02d} ({next_reel['name']})")
        if "--publish" in sys.argv:
            publish_reel(next_reel)
        else:
            print(">> Run with '--publish' flag to upload and publish live immediately:")
            print("   python publish_next_reel.py --publish")
