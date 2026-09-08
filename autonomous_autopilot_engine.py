import os
import sys
import json
import time
import asyncio
import argparse
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from cloud_autopilot_runner import render_poster, assemble_mp4, generate_speech_async, load_history, save_history
from infinite_content_engine import load_dynamic_catalog, generate_and_append_new_post
from youtube_uploader import upload_short_to_youtube, get_authenticated_service
from PIL import Image

TEMP_DIR = os.path.join(BASE_DIR, "output", "temp_autopilot")
os.makedirs(TEMP_DIR, exist_ok=True)

def sync_git():
    """Commits and pushes updated history and dynamic catalog to GitHub."""
    try:
        subprocess.run(["git", "add", "published_videos/published_history.json", "dynamic_catalog.json"], cwd=BASE_DIR, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Auto-replenished queue and updated video schedule [skip ci]"], cwd=BASE_DIR, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True)
        print(">> [Git] Synced history and dynamic catalog to GitHub remote.")
    except Exception as e:
        print(f">> [Git Notice]: {e}")

def get_youtube_scheduled_videos():
    """Returns list of all currently scheduled videos in YouTube Studio."""
    try:
        yt = get_authenticated_service()
        ch = yt.channels().list(part='contentDetails', mine=True).execute()
        up_id = ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        items = yt.playlistItems().list(part='snippet,status', playlistId=up_id, maxResults=50).execute()
        
        scheduled = []
        for i in items.get('items', []):
            vid_id = i['snippet']['resourceId']['videoId']
            status = i.get('status', {}).get('privacyStatus')
            title = i['snippet']['title']
            
            # If private, fetch video details to check publishAt
            if status == "private":
                v_res = yt.videos().list(part='status,snippet', id=vid_id).execute()
                if v_res.get('items'):
                    v_stat = v_res['items'][0]['status']
                    pub_at = v_stat.get('publishAt')
                    if pub_at:
                        scheduled.append({
                            "id": vid_id,
                            "title": title,
                            "publish_at": pub_at
                        })
        return scheduled
    except Exception as e:
        print(f"[!] Error fetching YouTube scheduled videos: {e}")
        return []

def get_instagram_client():
    session_file = os.path.join(BASE_DIR, "ig_session.json")
    if not os.path.exists(session_file):
        return None
    try:
        from instagrapi import Client
        cl = Client()
        cl.load_settings(session_file)
        return cl
    except Exception:
        return None

def check_status():
    """Prints a complete executive status dashboard of YouTube and Instagram channels."""
    print("\n========================================================")
    print("  THE WEALTH BLUEPRINT: AUTOPILOT STATUS DASHBOARD")
    print("========================================================")
    
    catalog = load_dynamic_catalog()
    history = load_history()
    print(f"Content Catalog Reservoir: {len(catalog)} total topics ready")
    print(f"Published History Log:      {len(history)} entries logged")
    
    print("\n-- YouTube Studio Scheduled Queue --")
    scheduled_yt = get_youtube_scheduled_videos()
    print(f"Scheduled Videos in Studio: {len(scheduled_yt)}")
    for v in sorted(scheduled_yt, key=lambda x: x.get('publish_at', '')):
        print(f"  [SCHEDULED] {v['publish_at']} | {v['title']}")
        
    print("\n-- Instagram Reels Status --")
    cl = get_instagram_client()
    if cl:
        try:
            u_id = cl.user_id_from_username("thewealthblueprint10")
            medias = cl.user_medias(u_id, amount=10)
            print(f"Connected as: @thewealthblueprint10")
            print(f"Live Reels on Profile: {len(medias)}")
            for m in medias[:5]:
                print(f"  [LIVE REEL] https://www.instagram.com/reel/{m.code}/")
        except Exception as e:
            print(f"Instagram check note: {e}")
    else:
        print("Instagram session not active.")
    print("========================================================\n")

def replenish_youtube_queue(min_buffer=6, batch_size=8):
    """
    Checks the YouTube scheduled queue. If below min_buffer, automatically renders
    the next un-scheduled posts from dynamic_catalog.json in the safe zone,
    schedules them into YouTube Studio, and auto-replenishes the catalog!
    """
    scheduled_yt = get_youtube_scheduled_videos()
    print(f"\n>> YouTube Scheduled Queue currently has {len(scheduled_yt)} videos.")

    catalog = load_dynamic_catalog()
    history = load_history()
    
    # Identify already scheduled / uploaded post IDs and titles
    uploaded_titles = {v['title'].split('#')[0].strip().lower() for v in scheduled_yt}
    for h in history:
        if h.get('title'):
            uploaded_titles.add(h['title'].split('#')[0].strip().lower())

    # Find next un-uploaded items
    pending_items = []
    for item in catalog:
        clean_t = item['title'].split('#')[0].strip().lower()
        if not any(clean_t[:20] in ut for ut in uploaded_titles):
            pending_items.append(item)

    if not pending_items:
        print(">> No pending items found in catalog! Synthesizing new posts now...")
        for _ in range(batch_size):
            pending_items.append(generate_and_append_new_post())

    # Determine latest scheduled time to extend from
    latest_time = None
    for v in scheduled_yt:
        pub = v.get('publish_at')
        if pub:
            try:
                # Parse ISO timestamp
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                if latest_time is None or dt > latest_time:
                    latest_time = dt
            except Exception:
                pass

    if latest_time is None:
        # Default start from tomorrow 12:00 PM IST (06:30 UTC)
        now = datetime.utcnow()
        latest_time = datetime(now.year, now.month, now.day, 6, 30, 0) + timedelta(days=1)

    print(f">> Extending YouTube schedule after latest slot: {latest_time.isoformat()}")

    # Slots alternate between:
    # 03:30 UTC (09:00 AM IST) -> 08:00 UTC (01:30 PM IST) -> 15:00 UTC (08:30 PM IST)
    items_to_schedule = pending_items[:batch_size]
    curr_time = latest_time
    scheduled_count = 0

    for item in items_to_schedule:
        # Advance to next 3x slot
        if curr_time.hour < 6:
            # Move from 03:30 UTC to 08:00 UTC same day
            curr_time = curr_time.replace(hour=8, minute=0, second=0)
        elif curr_time.hour < 12:
            # Move from 08:00 UTC to 15:00 UTC same day
            curr_time = curr_time.replace(hour=15, minute=0, second=0)
        else:
            # Move to next day 03:30 UTC
            curr_time = (curr_time + timedelta(days=1)).replace(hour=3, minute=30, second=0)

        iso_time = curr_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        p_id = item["id"]

        print(f"\n>> Scheduling Post #{p_id:02d}: {item['title']}")
        print(f"   Slot Time: {iso_time}")

        img_path = os.path.join(TEMP_DIR, f"yt_{p_id:03d}.png")
        thumb_path = os.path.join(TEMP_DIR, f"yt_{p_id:03d}_thumb.jpg")
        voice_path = os.path.join(TEMP_DIR, f"yt_{p_id:03d}_voice.mp3")
        mp4_path = os.path.join(TEMP_DIR, f"yt_{p_id:03d}.mp4")

        # 1. Render Safe-Zone Poster (1080x1920, Y:215-1405)
        render_poster(item, img_path)
        Image.open(img_path).convert("RGB").save(thumb_path, "JPEG", quality=95)

        # 2. Neural Speech
        asyncio.run(generate_speech_async(item["script"], voice_path, item["voice"]))

        # 3. Composite Video
        assemble_mp4(img_path, voice_path, mp4_path)

        # 4. Upload to YouTube Shorts Scheduled
        yt_desc = f"""{item['title']}\n\n{item['sub']}\n\nTHE BREAKDOWN:\n{item['c1_t']}\n{item['c1_d']}\n\nTHE BLUEPRINT:\n{item['c2_t']}\n{item['c2_d']}\n\nTHE PAYOFF:\n{item['c3_t']}\n{item['c3_d']}\n\nSubscribe to The Wealth Blueprint for daily wealth loopholes!"""

        try:
            yt_url = upload_short_to_youtube(
                video_path=mp4_path,
                title=item["title"],
                description=yt_desc,
                tags=item.get("tags", ["shorts", "wealth", "finance"]),
                pinned_comment=item.get("pinned_comment", "Subscribe for daily wealth rules & banking loopholes!"),
                publish_at=iso_time
            )
            print(f"   [SUCCESS] Scheduled on YouTube: {yt_url}")

            record = {
                "id": p_id,
                "day": item["day"],
                "slot": item["slot"],
                "title": item["title"],
                "timestamp": datetime.now().isoformat(),
                "youtube_url": yt_url,
                "youtube_scheduled_for": iso_time,
                "instagram_status": "Ready in queue"
            }
            history.append(record)
            save_history(history)
            scheduled_count += 1

            # 5. Infinite Self-Replenishment: Create a brand new viral concept!
            new_post = generate_and_append_new_post()
            print(f"   >> [INFINITE AUTOPILOT] Queue replenished with Post #{new_post['id']}: '{new_post['title']}'")

        except Exception as e:
            print(f"   [!] YouTube Upload Error: {e}")
            if "quotaExceeded" in str(e):
                print("   >> Reached daily YouTube API quota limit. Will continue in next cycle.")
                break

        # Clean temp files
        for p in [img_path, thumb_path, voice_path, mp4_path]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    sync_git()
    print(f"\n>> Replenished YouTube Queue with {scheduled_count} newly scheduled videos.")

def publish_next_reel():
    """Publishes the next pending reel to Instagram, replenishes queue, and syncs history."""
    cl = get_instagram_client()
    if not cl:
        print("[!] Error: Instagram session not found.")
        return False

    catalog = load_dynamic_catalog()
    history = load_history()
    ig_published_ids = {h.get("id") for h in history if h.get("instagram_url")}

    next_item = None
    for item in catalog:
        if item["id"] not in ig_published_ids:
            next_item = item
            break

    if not next_item:
        next_item = generate_and_append_new_post()

    p_id = next_item["id"]
    print(f"\n>> Publishing Next Instagram Reel (Post #{p_id:02d}): {next_item['title']}")

    img_path = os.path.join(TEMP_DIR, f"ig_{p_id:03d}.png")
    thumb_path = os.path.join(TEMP_DIR, f"ig_{p_id:03d}_thumb.jpg")
    voice_path = os.path.join(TEMP_DIR, f"ig_{p_id:03d}_voice.mp3")
    mp4_path = os.path.join(TEMP_DIR, f"ig_{p_id:03d}.mp4")

    render_poster(next_item, img_path)
    Image.open(img_path).convert("RGB").save(thumb_path, "JPEG", quality=95)
    asyncio.run(generate_speech_async(next_item["script"], voice_path, next_item["voice"]))
    assemble_mp4(img_path, voice_path, mp4_path)

    ig_caption = f"""{next_item['title']}\n\n{next_item['sub']}\n\nTHE TRAP:\n{next_item['c1_t']}\n{next_item['c1_d']}\n\nTHE BLUEPRINT:\n{next_item['c2_t']}\n{next_item['c2_d']}\n\nTHE PAYOFF:\n{next_item['c3_t']}\n{next_item['c3_d']}\n\nFollow @thewealthblueprint10 for daily wealth loopholes.\nSave this reel so you don't lose it!\n\n.\n.\n.\n#wealth #personalfinance #moneytips #bankinghacks #creditcard #investing #financialfreedom #smartmoney"""

    try:
        media = cl.clip_upload(mp4_path, caption=ig_caption, thumbnail=thumb_path)
        ig_url = f"https://www.instagram.com/reel/{media.code}/"
        print(f"   [SUCCESS] Published Reel: {ig_url}")

        for h in history:
            if h.get("id") == p_id:
                h["instagram_url"] = ig_url
                h["instagram_status"] = "Published Live as Reel"
                break
        else:
            history.append({
                "id": p_id,
                "title": next_item["title"],
                "timestamp": datetime.now().isoformat(),
                "instagram_url": ig_url,
                "instagram_status": "Published Live as Reel"
            })
        save_history(history)

        # Infinite replenishment
        new_post = generate_and_append_new_post()
        print(f"   >> [INFINITE AUTOPILOT] Queue replenished with Post #{new_post['id']}: '{new_post['title']}'")
        sync_git()
        return True
    except Exception as e:
        print(f"   [!] Instagram upload error: {e}")
        return False
    finally:
        for p in [img_path, thumb_path, voice_path, mp4_path]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

def run_continuous_daemon():
    """Continuous background daemon ensuring queue buffer and scheduled reel posting."""
    print("========================================================")
    print("  THE WEALTH BLUEPRINT: AUTOPILOT DAEMON RUNNING")
    print("  - Daily Slots: 12:00 PM IST & 08:00 PM IST")
    print("  - YouTube Buffer: Auto-replenished (Target: 7+ days)")
    print("  - Infinite Content Engine: Active (Never depletes)")
    print("========================================================\n")

    # Initial check & buffer replenishment
    try:
        replenish_youtube_queue(min_buffer=6, batch_size=6)
    except Exception as e:
        print(f"[!] Startup replenishment notice: {e}")

    last_slot = None
    while True:
        now = datetime.now()
        h, m = now.hour, now.minute
        date_str = now.strftime("%Y-%m-%d")

        slot = None
        # 3x Daily Cadence: 09:00 AM, 01:30 PM, 08:30 PM IST
        if h == 9 and 0 <= m <= 15:
            slot = f"{date_str}_09AM"
        elif h == 13 and 25 <= m <= 40:
            slot = f"{date_str}_0130PM"
        elif h == 20 and 25 <= m <= 40:
            slot = f"{date_str}_0830PM"

        if slot and slot != last_slot:
            print(f"\n[TRIGGER] Reached prime posting slot: {slot}!")
            try:
                # 1. Publish next Reel to Instagram
                publish_next_reel()
                # 2. Check YouTube queue and replenish if buffer getting low
                replenish_youtube_queue(min_buffer=6, batch_size=4)
                last_slot = slot
            except Exception as e:
                print(f"[!] Autopilot slot error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Infinite Autopilot Engine")
    parser.add_argument("--status", action="store_true", help="Display full channel and queue status")
    parser.add_argument("--replenish-youtube", action="store_true", help="Replenish YouTube Studio scheduled queue")
    parser.add_argument("--publish-reel", action="store_true", help="Publish the next Instagram Reel immediately")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background daemon mode")
    args = parser.parse_args()

    if args.status:
        check_status()
    elif args.replenish_youtube:
        replenish_youtube_queue(min_buffer=6, batch_size=8)
    elif args.publish_reel:
        publish_next_reel()
    elif args.daemon:
        run_continuous_daemon()
    else:
        check_status()
