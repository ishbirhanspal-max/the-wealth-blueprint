import os
import sys
import json
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Console encoding fix for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

POSTS_DIR = os.path.join(BASE_DIR, "posts_15_days", "ready_videos")
PUBLISHED_DIR = os.path.join(BASE_DIR, "published_videos")
HISTORY_FILE = os.path.join(PUBLISHED_DIR, "published_history.json")
os.makedirs(PUBLISHED_DIR, exist_ok=True)

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
        json.dump(history, f, indent=2)

def check_credentials():
    yt_ready = os.path.exists(os.path.join(BASE_DIR, "token.json")) or os.path.exists(os.path.join(BASE_DIR, "client_secret.json"))
    ig_user = os.getenv("INSTAGRAM_USERNAME")
    ig_pass = os.getenv("INSTAGRAM_PASSWORD")
    ig_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_ready = bool((ig_user and ig_pass) or ig_token)
    return yt_ready, ig_ready

def publish_video(day_num: int, dry_run: bool = False):
    """Publishes a specific day's video to YouTube and Instagram."""
    video_file = os.path.join(POSTS_DIR, f"day{day_num:02d}_The_Wealth_Blueprint.mp4")
    seo_file = os.path.join(POSTS_DIR, f"day{day_num:02d}_seo.json")

    if not os.path.exists(video_file) or not os.path.exists(seo_file):
        print(f"[!] Error: Assets for Day {day_num:02d} not found in {POSTS_DIR}")
        return False

    with open(seo_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    title = meta.get("title", f"Day {day_num:02d} - The Wealth Blueprint")
    desc = meta.get("youtube_description", "")
    caption = meta.get("instagram_caption", "")
    tags = meta.get("tags", ["finance", "shorts", "wealth"])
    
    pinned_comment = "Which step in this blueprint surprised you most? Comment below and we'll send you our 0% Interest Card Masterlist!"

    print(f"\n========================================================")
    print(f">> PUBLISHING DAY {day_num:02d}: {title}")
    print(f">> Video: {os.path.basename(video_file)}")
    print(f"========================================================")

    if dry_run:
        print("[DRY-RUN] Verification mode active - no API calls made.")
        print(f"[DRY-RUN] Title: {title}")
        print(f"[DRY-RUN] Tags: {', '.join(tags)}")
        print(f"[DRY-RUN] Pinned Comment: {pinned_comment}")
        return True

    yt_ready, ig_ready = check_credentials()
    results = {"day": day_num, "timestamp": datetime.now().isoformat(), "title": title}

    # 1. YouTube Upload
    if yt_ready:
        try:
            from youtube_uploader import upload_short_to_youtube
            yt_url = upload_short_to_youtube(
                video_path=video_file,
                title=title,
                description=desc,
                tags=tags,
                pinned_comment=pinned_comment,
                privacy_status="public"
            )
            results["youtube_url"] = yt_url
            print(f"   [OK] YouTube Shorts: Published at {yt_url}")
        except Exception as e:
            print(f"   [!] YouTube Upload Error: {e}")
            results["youtube_error"] = str(e)
    else:
        print("   [SKIP] YouTube: client_secret.json / token.json not configured.")

    # 2. Instagram Upload
    if ig_ready:
        try:
            from instagram_uploader import publish_to_instagram
            ig_url = publish_to_instagram(
                video_path=video_file,
                caption=caption
            )
            results["instagram_url"] = ig_url
            print(f"   [OK] Instagram Reels: Published at {ig_url}")
        except Exception as e:
            print(f"   [!] Instagram Upload Error: {e}")
            results["instagram_error"] = str(e)
    else:
        print("   [SKIP] Instagram: INSTAGRAM_USERNAME or Meta tokens not set in .env")

    # Record history
    history = load_history()
    history.append(results)
    save_history(history)
    print(f">> Day {day_num:02d} logged to published_history.json")
    return True

def get_next_unpublished_day():
    history = load_history()
    published_days = {entry.get("day") for entry in history}
    for day in range(1, 16):
        if day not in published_days:
            return day
    return None

def show_status():
    history = load_history()
    published_days = {entry.get("day"): entry for entry in history}
    yt_ready, ig_ready = check_credentials()

    print("\n========================================================")
    print(">> THE WEALTH BLUEPRINT: 15-DAY AUTOPILOT STATUS")
    print("========================================================")
    print(f"Credentials Status:")
    print(f"  - YouTube:   {'[CONNECTED]' if yt_ready else '[MISSING client_secret.json or token.json]'}")
    print(f"  - Instagram: {'[CONNECTED]' if ig_ready else '[MISSING credentials in .env]'}")
    print("--------------------------------------------------------")
    print("Day-by-Day Schedule:")
    for day in range(1, 16):
        video_exists = os.path.exists(os.path.join(POSTS_DIR, f"day{day:02d}_The_Wealth_Blueprint.mp4"))
        status_tag = "[PUBLISHED]" if day in published_days else ("[READY TO POST]" if video_exists else "[NOT BUILT]")
        print(f"  Day {day:02d}: {status_tag}")
    print("========================================================\n")

def run_daemon(interval_hours: float = 24.0):
    print(f">> Starting background autopilot daemon (posting every {interval_hours} hours)...")
    while True:
        next_day = get_next_unpublished_day()
        if next_day is None:
            print(">> All 15 days have been published! Autopilot campaign complete.")
            break
        print(f"\n>> [Autopilot] Triggering scheduled post for Day {next_day:02d}...")
        publish_video(next_day)
        print(f">> Sleeping for {interval_hours} hours until next post...")
        time.sleep(interval_hours * 3600)

def main():
    parser = argparse.ArgumentParser(description="The Wealth Blueprint - Automated Video Publisher")
    parser.add_argument("--status", action="store_true", help="Show publishing campaign status")
    parser.add_argument("--publish-next", action="store_true", help="Publish the next unposted video")
    parser.add_argument("--publish-day", type=int, help="Publish a specific day number (1-15)")
    parser.add_argument("--daemon", action="store_true", help="Run in background daemon mode posting every 24h")
    parser.add_argument("--dry-run", action="store_true", help="Test execution without live API upload")
    args = parser.parse_args()

    if args.status or (not any(vars(args).values())):
        show_status()
        return

    if args.publish_day:
        publish_video(args.publish_day, dry_run=args.dry_run)
    elif args.publish_next:
        next_day = get_next_unpublished_day()
        if next_day:
            publish_video(next_day, dry_run=args.dry_run)
        else:
            print(">> All 15 videos are already published!")
    elif args.daemon:
        run_daemon()

if __name__ == "__main__":
    main()
