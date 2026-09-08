import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Console encoding fix for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from infinite_content_engine import load_dynamic_catalog, generate_and_append_new_post
from cloud_autopilot_runner import render_poster, assemble_mp4, generate_speech_async, load_history, save_history
from PIL import Image
import asyncio

TEMP_DIR = os.path.join(BASE_DIR, "output", "temp_cloud")
os.makedirs(TEMP_DIR, exist_ok=True)

def publish_next_cycle():
    """Renders and publishes the next video, then auto-replenishes the catalog."""
    catalog = load_dynamic_catalog()
    history = load_history()
    published_ids = {entry.get("id") for entry in history}

    next_item = None
    for item in catalog:
        if item["id"] not in published_ids:
            next_item = item
            break

    if not next_item:
        print(">> No pending posts in catalog. Generating a new one now...")
        next_item = generate_and_append_new_post()

    p_id = next_item["id"]
    print("\n========================================================")
    print(f">> LOCAL AUTOPILOT: PROCESSING POST #{p_id:03d} (Day {next_item['day']:02d} / Slot {next_item['slot']})")
    print(f">> Title: {next_item['title']}")
    print(f">> Region: {next_item['region']} | Voice: {next_item['voice']}")
    print("========================================================")

    img_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.png")
    thumb_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_thumb.jpg")
    voice_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_voice.mp3")
    mp4_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.mp4")

    # 1. Render Safe-Zone Poster
    print("1. Rendering 1080x1920 Mobile Safe-Zone Poster...")
    render_poster(next_item, img_path)

    # 2. Convert to JPEG Thumbnail
    print("2. Generating high-quality JPEG thumbnail...")
    Image.open(img_path).convert("RGB").save(thumb_path, "JPEG", quality=95)

    # 3. Neural Speech
    print(f"3. Synthesizing voiceover ({next_item['voice']})...")
    asyncio.run(generate_speech_async(next_item["script"], voice_path, next_item["voice"]))

    # 4. Assemble Video
    print("4. Compositing video with 124 BPM phonk/sub-bass beat...")
    assemble_mp4(img_path, voice_path, mp4_path)
    sz_mb = os.path.getsize(mp4_path) / (1024 * 1024)
    print(f"[OK] Video ready: {os.path.basename(mp4_path)} ({sz_mb:.2f} MB)")

    results = {
        "id": p_id,
        "day": next_item["day"],
        "slot": next_item["slot"],
        "region": next_item["region"],
        "title": next_item["title"],
        "timestamp": datetime.now().isoformat(),
        "youtube_url": None,
        "instagram_url": None
    }

    # 5. YouTube Shorts Upload
    yt_token_exists = os.path.exists(os.path.join(BASE_DIR, "token.json"))
    if yt_token_exists:
        try:
            from youtube_uploader import upload_short_to_youtube
            yt_desc = f"""{next_item['title']}\n\n{next_item['sub']}\n\nTHE BREAKDOWN:\n{next_item['c1_t']}\n{next_item['c1_d']}\n\nTHE BLUEPRINT:\n{next_item['c2_t']}\n{next_item['c2_d']}\n\nTHE PAYOFF:\n{next_item['c3_t']}\n{next_item['c3_d']}\n\nSubscribe to The Wealth Blueprint for 2 wealth loopholes daily!"""
            yt_url = upload_short_to_youtube(
                video_path=mp4_path,
                title=next_item["title"],
                description=yt_desc,
                tags=next_item["tags"],
                pinned_comment=next_item["pinned_comment"],
                privacy_status="public"
            )
            results["youtube_url"] = yt_url
            print(f">> [YouTube Shorts] Published successfully! URL: {yt_url}")
        except Exception as e:
            print(f">> [YouTube Error]: {e}")
            results["youtube_error"] = str(e)
    else:
        print(">> [YouTube] token.json not found, skipping YouTube.")

    # 6. Instagram Reels Upload
    session_file = os.path.join(BASE_DIR, "ig_session.json")
    if os.path.exists(session_file):
        try:
            from instagrapi import Client
            cl = Client()
            cl.load_settings(session_file)

            ig_caption = f"""{next_item['title']}\n\n{next_item['sub']}\n\nTHE TRAP:\n{next_item['c1_t']}\n{next_item['c1_d']}\n\nTHE BLUEPRINT:\n{next_item['c2_t']}\n{next_item['c2_d']}\n\nTHE PAYOFF:\n{next_item['c3_t']}\n{next_item['c3_d']}\n\nFollow @thewealthblueprint10 for daily wealth loopholes.\nSave this reel so you don't lose it!\n\n.\n.\n.\n#wealth #personalfinance #moneytips #bankinghacks #creditcard #investing #financialfreedom #smartmoney"""
            print(f">> [Instagram Reels] Uploading Reel with thumbnail...")
            media = cl.clip_upload(mp4_path, caption=ig_caption, thumbnail=thumb_path)
            ig_url = f"https://www.instagram.com/reel/{media.code}/"
            results["instagram_url"] = ig_url
            print(f">> [Instagram Reels] Published successfully! URL: {ig_url}")
        except Exception as e:
            print(f">> [Instagram Error]: {e}")
            results["instagram_error"] = str(e)
    else:
        print(">> [Instagram] ig_session.json not found, skipping Instagram.")

    # 7. Save History
    history.append(results)
    save_history(history)

    # 8. Infinite Replenishment: Create a brand new viral video concept and append to catalog
    try:
        new_post = generate_and_append_new_post()
        print(f">> [INFINITE AUTOPILOT] Queue replenished with Post #{new_post['id']}: '{new_post['title']}'")
    except Exception as e:
        print(f"[!] Warning: Could not replenish queue: {e}")

    # 9. Sync with Git Remote
    try:
        subprocess.run(["git", "add", "published_videos/published_history.json", "dynamic_catalog.json"], cwd=BASE_DIR, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Auto-published Post #{p_id:03d} and replenished catalog [skip ci]"], cwd=BASE_DIR, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True)
        print(">> [Git] Synced history and dynamic catalog to GitHub.")
    except Exception as e:
        print(f">> [Git Notice]: {e}")

    return results

def run_scheduler_loop():
    """Runs continuously in the background, triggering at 12:00 PM and 08:00 PM IST."""
    print("========================================================")
    print("  THE WEALTH BLUEPRINT: INFINITE AUTOPILOT DAEMON")
    print("  Slots: 12:00 PM IST & 08:00 PM IST (Daily)")
    print("  Platforms: YouTube Shorts & Instagram Reels")
    print("  Safe Zone: Enabled (100% Un-eaten layout)")
    print("========================================================\n")
    
    last_triggered_slot = None

    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # Slot 1: 12:00 PM IST (12:00 - 12:05)
        # Slot 2: 08:00 PM IST (20:00 - 20:05)
        current_date_str = now.strftime("%Y-%m-%d")
        slot_key = None

        if hour == 12 and 0 <= minute <= 10:
            slot_key = f"{current_date_str}_12PM"
        elif hour == 20 and 0 <= minute <= 10:
            slot_key = f"{current_date_str}_8PM"

        if slot_key and slot_key != last_triggered_slot:
            print(f"\n[TRIGGER] Scheduled slot activated: {slot_key}!")
            try:
                publish_next_cycle()
                last_triggered_slot = slot_key
            except Exception as e:
                print(f"[!] Cycle error: {e}")
        
        time.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local Autopilot Daemon")
    parser.add_argument("--publish-now", action="store_true", help="Immediately publish the next video, replenish queue, and exit")
    args = parser.parse_args()

    if args.publish_now:
        publish_next_cycle()
    else:
        run_scheduler_loop()
