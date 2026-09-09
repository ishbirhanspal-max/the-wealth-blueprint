import os
import sys
import json
import time
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

from publish_next_reel import publish_reel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_FILE = os.path.join(BASE_DIR, "SCHEDULE_CALENDAR.json")
HISTORY_FILE = os.path.join(BASE_DIR, "published_videos", "published_history.json")

def load_calendar():
    if not os.path.exists(CALENDAR_FILE):
        return []
    with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_calendar(cal):
    with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
        json.dump(cal, f, indent=2, ensure_ascii=False)

def check_and_publish_due(dry_run: bool = False):
    cal = load_calendar()
    now_iso = datetime.now().isoformat()
    now_dt = datetime.now()

    due_item = None
    for item in cal:
        if item.get("status") == "SCHEDULED" or item.get("reel_status") == "SCHEDULED":
            sched_dt = datetime.fromisoformat(item["scheduled_datetime"].replace("+05:30", ""))
            if now_dt >= sched_dt:
                due_item = item
                break

    if not due_item:
        next_up = next((it for it in cal if it.get("status") == "SCHEDULED" or it.get("reel_status") == "SCHEDULED"), None)
        if next_up:
            n_id = next_up.get("reel_id") or next_up.get("id")
            print(f">> Autopilot Scheduler: No posts currently due.")
            print(f">> Next scheduled post: Reel #{n_id:02d} on {next_up.get('scheduled_time_str')}")
        else:
            print(">> All items on schedule calendar have already been published!")
        return None

    r_id = due_item.get("reel_id") or due_item.get("id")
    print(f"\n========================================================")
    print(f">> DUE POST DETECTED: Reel #{r_id:02d} ({due_item['title']})")
    print(f">> Scheduled For: {due_item.get('scheduled_time_str')}")
    print(f"========================================================")

    if dry_run:
        print("[DRY-RUN] Post is due and ready to publish.")
        return due_item

    # 1. Publish to Instagram (Reel + Story)
    reel_url = None
    story_id = None
    yt_url = due_item.get("youtube_url")

    # Fetch full item metadata from catalog
    catalog_path = os.path.join(BASE_DIR, "dynamic_catalog.json")
    with open(catalog_path, "r", encoding="utf-8") as f:
        cat = json.load(f)
    target = next((c for c in cat if c["id"] == r_id), None)

    if due_item.get("video_path") and os.path.exists(due_item["video_path"]):
        item_payload = {
            "id": r_id,
            "name": os.path.basename(due_item["video_path"]),
            "mp4": due_item["video_path"],
            "caption_file": due_item.get("caption_path") or (os.path.splitext(due_item["video_path"])[0] + "_caption.txt" if os.path.exists(os.path.splitext(due_item["video_path"])[0] + "_caption.txt") else None),
            "thumb_file": due_item.get("thumb_path") or (os.path.splitext(due_item["video_path"])[0] + "_thumb.jpg" if os.path.exists(os.path.splitext(due_item["video_path"])[0] + "_thumb.jpg") else None)
        }
        reel_url, story_id = publish_reel(item_payload, post_story=True)

        # 2. Check and Publish to YouTube Shorts if not already pre-scheduled in Studio
        if not due_item.get("youtube_url") and due_item.get("youtube_status") != "SCHEDULED IN STUDIO" and target:
            try:
                from youtube_uploader import upload_short_to_youtube
                yt_desc = f"""{target['title']}\n\n⚡ SCRIPT BREAKDOWN:\n{target['script']}\n\n👇 FREE WEALTH MASTERLIST: Check bio @TheWealthBlueprint\n\n#Shorts #{target['category'].replace(' ', '')} #TheWealthBlueprint"""
                print(f">> Uploading Post #{r_id:02d} to YouTube Shorts...")
                yt_url = upload_short_to_youtube(
                    video_path=due_item["video_path"],
                    title=target["title"],
                    description=yt_desc,
                    tags=target.get("tags", ["shorts", "finance"]),
                    pinned_comment=target.get("pinned_comment"),
                    privacy_status="public"
                )
                due_item["youtube_url"] = yt_url
                print(f"   [OK] YouTube Shorts LIVE: {yt_url}")
            except Exception as ye:
                print(f"   [!] YouTube upload notice: {ye}")
    else:
        print(f">> Pre-rendered file not found for Post #{r_id:02d}. Rendering on-the-fly with cloud runner...")
        from cloud_autopilot_runner import publish_entry
        if target:
            publish_entry(target)
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as hf:
                    h_data = json.load(hf)
                    last_entry = next((x for x in reversed(h_data) if x.get("id") == r_id), {})
                    reel_url = last_entry.get("instagram_url")
                    story_id = last_entry.get("instagram_story_id")
                    yt_url = last_entry.get("youtube_url")

    due_item["status"] = "PUBLISHED"
    due_item["published_at"] = datetime.now().isoformat()
    due_item["instagram_url"] = reel_url
    if yt_url:
        due_item["youtube_url"] = yt_url
        due_item["youtube_status"] = "LIVE"
    if story_id:
        due_item["instagram_story_id"] = story_id
    save_calendar(cal)

    print(f">> Post #{r_id:02d} (YouTube + Instagram Reel + Story) published and marked done in schedule calendar!")
    return due_item

def run_daemon():
    print(">> Starting Scheduled Autopilot Daemon in background...")
    print(">> Checking calendar every 60 seconds for due posting slots...")
    while True:
        try:
            check_and_publish_due()
        except Exception as e:
            print(f"[!] Scheduler exception: {e}")
        time.sleep(60)

if __name__ == "__main__":
    if "--daemon" in sys.argv:
        run_daemon()
    else:
        check_and_publish_due(dry_run=("--dry-run" in sys.argv))
