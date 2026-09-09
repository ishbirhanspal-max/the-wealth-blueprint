import os
import sys
import json
import glob
import re
import time
from datetime import datetime
from pathlib import Path
from instagrapi import Client
from story_generator import render_story_background

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

def publish_reel(item: dict, post_story: bool = True):
    r_id = item["id"]
    print(f"\n========================================================")
    print(f">> PUBLISHING REEL #{r_id:02d} TO INSTAGRAM: {item['name']}")
    print(f"========================================================")

    caption = ""
    title_line = item['name'].replace(".mp4", "").replace("_", " ")
    if item["caption_file"] and os.path.exists(item["caption_file"]):
        with open(item["caption_file"], "r", encoding="utf-8") as f:
            caption = f.read().strip()
            first_line = caption.split("\n")[0].strip()
            if first_line:
                title_line = first_line

    if not caption:
        caption = f"The Wealth Blueprint - Reel #{r_id:02d}\n\nFollow @thewealthblueprint10 for daily wealth loopholes!"

    cl = Client()
    if not os.path.exists(SESSION_FILE):
        raise RuntimeError("ig_session.json not found! Please ensure your session is active.")
    
    cl.load_settings(SESSION_FILE)
    u = cl.account_info()
    print(f">> Authenticated as @{u.username} (ID: {cl.user_id})")
    print(f">> Uploading video ({os.path.getsize(item['mp4']) / (1024*1024):.2f} MB)...")

    media = cl.clip_upload(
        path=item["mp4"],
        caption=caption,
        thumbnail=item["thumb_file"]
    )

    reel_url = f"https://www.instagram.com/reel/{media.code}/"
    print(f"\n[SUCCESS] Reel #{r_id:02d} is LIVE on Instagram!")
    print(f">> Reel Code: {media.code}")
    print(f">> Reel PK: {media.pk}")
    print(f">> Live URL: {reel_url}")

    story_id = None
    if post_story:
        print(f"\n>> Generating luxury 9:16 Instagram Story Card...")
        story_bg = os.path.join(PACKAGE_DIR, f"temp_story_bg_{r_id:02d}.jpg")
        try:
            render_story_background(title_line, "Wealth System", story_bg)
            print(f">> Sharing Reel #{r_id:02d} to Instagram Stories with interactive sticker...")
            time.sleep(3) # allow CDN replication
            story = cl.media_share_to_story(
                media_id=str(media.pk),
                background=Path(story_bg)
            )
            story_id = story.id if hasattr(story, 'id') else str(story)
            print(f"[SUCCESS] Story is LIVE on @{u.username}'s profile!")
            print(f">> Story ID: {story_id}")
        except Exception as se:
            print(f"[!] Warning: Story share encountered an issue: {se}")
        finally:
            if os.path.exists(story_bg):
                try:
                    os.remove(story_bg)
                except Exception:
                    pass

    # Update history
    history = load_history()
    found = False
    for h in history:
        if h.get("id") == r_id:
            h["instagram_url"] = reel_url
            h["instagram_status"] = "PUBLISHED"
            h["instagram_published_at"] = datetime.now().isoformat()
            if story_id:
                h["instagram_story_id"] = story_id
            found = True
            break
    if not found:
        entry = {
            "id": r_id,
            "title": title_line,
            "timestamp": datetime.now().isoformat(),
            "instagram_url": reel_url,
            "instagram_status": "PUBLISHED",
            "instagram_published_at": datetime.now().isoformat()
        }
        if story_id:
            entry["instagram_story_id"] = story_id
        history.append(entry)
    save_history(history)
    return reel_url, story_id

if __name__ == "__main__":
    next_reel = get_next_unpublished_package_reel()
    if not next_reel:
        print(">> All 15 package reels have been published to Instagram!")
    else:
        print(f">> Next reel in queue: #{next_reel['id']:02d} ({next_reel['name']})")
        if "--publish" in sys.argv:
            publish_reel(next_reel, post_story=True)
        else:
            print(">> Run with '--publish' flag to upload Reel + Story live immediately:")
            print("   python publish_next_reel.py --publish")
