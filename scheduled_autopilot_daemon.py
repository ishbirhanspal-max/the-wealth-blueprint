import os
import sys
import json
import time
from datetime import datetime
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
        if item.get("status") == "SCHEDULED":
            sched_dt = datetime.fromisoformat(item["scheduled_datetime"].replace("+05:30", ""))
            if now_dt >= sched_dt:
                due_item = item
                break

    if not due_item:
        next_up = next((it for it in cal if it.get("status") == "SCHEDULED"), None)
        if next_up:
            print(f">> Autopilot Scheduler: No posts currently due.")
            print(f">> Next scheduled post: Reel #{next_up['reel_id']:02d} on {next_up.get('scheduled_time_str')}")
        else:
            print(">> All items on schedule calendar have already been published!")
        return None

    r_id = due_item["reel_id"]
    print(f"\n========================================================")
    print(f">> DUE POST DETECTED: Reel #{r_id:02d} ({due_item['title']})")
    print(f">> Scheduled For: {due_item.get('scheduled_time_str')}")
    print(f"========================================================")

    if dry_run:
        print("[DRY-RUN] Post is due and ready to publish.")
        return due_item

    # Publish reel + story
    item_payload = {
        "id": r_id,
        "name": os.path.basename(due_item["video_path"]),
        "mp4": due_item["video_path"],
        "caption_file": due_item["caption_path"],
        "thumb_file": due_item["thumb_path"]
    }
    reel_url, story_id = publish_reel(item_payload, post_story=True)

    due_item["status"] = "PUBLISHED"
    due_item["published_at"] = datetime.now().isoformat()
    due_item["instagram_url"] = reel_url
    if story_id:
        due_item["instagram_story_id"] = story_id
    save_calendar(cal)

    print(f">> Reel #{r_id:02d} + Story published and marked done in schedule calendar!")
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
