import os
import sys
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from cloud_autopilot_runner import render_poster, assemble_mp4, generate_speech_async, load_history, save_history
from infinite_content_engine import load_dynamic_catalog, generate_and_append_new_post
from youtube_uploader import upload_short_to_youtube
from PIL import Image

TEMP_DIR = os.path.join(BASE_DIR, "output", "temp_batch")
os.makedirs(TEMP_DIR, exist_ok=True)

# Schedule slots starting after Day 06 (which is Sep 09 8 PM IST):
# Slots: 12:00 PM IST (06:30 UTC) and 08:00 PM IST (14:30 UTC)
SCHEDULE_SLOTS = [
    {"post_id": 8,  "time_iso": "2026-09-10T06:30:00.000Z", "human": "Thursday Sep 10, 12:00 PM IST"},
    {"post_id": 9,  "time_iso": "2026-09-10T14:30:00.000Z", "human": "Thursday Sep 10, 08:00 PM IST"},
    {"post_id": 10, "time_iso": "2026-09-11T06:30:00.000Z", "human": "Friday Sep 11, 12:00 PM IST"},
    {"post_id": 11, "time_iso": "2026-09-11T14:30:00.000Z", "human": "Friday Sep 11, 08:00 PM IST"},
    {"post_id": 12, "time_iso": "2026-09-12T06:30:00.000Z", "human": "Saturday Sep 12, 12:00 PM IST"},
    {"post_id": 13, "time_iso": "2026-09-12T14:30:00.000Z", "human": "Saturday Sep 12, 08:00 PM IST"},
    {"post_id": 14, "time_iso": "2026-09-13T06:30:00.000Z", "human": "Sunday Sep 13, 12:00 PM IST"},
    {"post_id": 15, "time_iso": "2026-09-13T14:30:00.000Z", "human": "Sunday Sep 13, 08:00 PM IST"}
]

def replenish_queue():
    print("========================================================")
    print("  THE WEALTH BLUEPRINT: REPLENISHING YOUTUBE QUEUE")
    print("  Safe Zone: Enabled (100% Mobile Safe Zone Y:215-1405)")
    print("  Self-Replenishment: Active (Synthesizes new posts)")
    print("========================================================\n")

    catalog = load_dynamic_catalog()
    catalog_by_id = {item["id"]: item for item in catalog}
    history = load_history()

    scheduled_count = 0

    for slot in SCHEDULE_SLOTS:
        p_id = slot["post_id"]
        item = catalog_by_id.get(p_id)
        if not item:
            print(f"[!] Post #{p_id} not found in catalog, skipping.")
            continue

        print(f"\n>> Processing Post #{p_id:02d}: {item['title']}")
        print(f"   Target Schedule Time: {slot['human']} ({slot['time_iso']})")

        img_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.png")
        thumb_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_thumb.jpg")
        voice_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_voice.mp3")
        mp4_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.mp4")

        # 1. Render Safe-Zone Poster
        print("   [1/4] Rendering 1080x1920 Mobile Safe-Zone Poster...")
        render_poster(item, img_path)
        Image.open(img_path).convert("RGB").save(thumb_path, "JPEG", quality=95)

        # 2. Neural Voiceover
        print(f"   [2/4] Synthesizing Neural Voiceover ({item['voice']})...")
        asyncio.run(generate_speech_async(item["script"], voice_path, item["voice"]))

        # 3. Assemble Video
        print("   [3/4] Compositing video with ducked ambient phonk beat...")
        assemble_mp4(img_path, voice_path, mp4_path)

        # 4. Schedule on YouTube Shorts
        print(f"   [4/4] Uploading to YouTube Shorts as Scheduled for {slot['time_iso']}...")
        yt_desc = f"""{item['title']}\n\n{item['sub']}\n\nTHE BREAKDOWN:\n{item['c1_t']}\n{item['c1_d']}\n\nTHE BLUEPRINT:\n{item['c2_t']}\n{item['c2_d']}\n\nTHE PAYOFF:\n{item['c3_t']}\n{item['c3_d']}\n\nSubscribe to The Wealth Blueprint for daily wealth loopholes!"""

        try:
            yt_url = upload_short_to_youtube(
                video_path=mp4_path,
                title=item["title"],
                description=yt_desc,
                tags=item.get("tags", ["shorts", "wealth", "finance"]),
                pinned_comment=item.get("pinned_comment", "Subscribe for daily wealth rules & banking loopholes!"),
                publish_at=slot["time_iso"]
            )
            print(f"   [SUCCESS] Scheduled on YouTube: {yt_url}")

            # Log to history
            record = {
                "id": p_id,
                "day": item["day"],
                "slot": item["slot"],
                "title": item["title"],
                "timestamp": datetime.now().isoformat(),
                "youtube_url": yt_url,
                "youtube_scheduled_for": f"{slot['time_iso']} ({slot['human']})",
                "instagram_status": "Ready in queue"
            }
            history.append(record)
            save_history(history)
            scheduled_count += 1

            # 5. Infinite Replenishment: Synthesize brand new post and append to dynamic catalog!
            try:
                new_post = generate_and_append_new_post()
                print(f"   >> [INFINITE ENGINE] Added Post #{new_post['id']} to catalog: '{new_post['title']}'")
            except Exception as re_err:
                print(f"   [!] Replenishment notice: {re_err}")

        except Exception as e:
            print(f"   [!] YouTube Upload Error: {e}")
            if "quotaExceeded" in str(e):
                print("\n   >> [QUOTA LIMIT REACHED] Reached daily YouTube API upload quota limit.")
                print("   >> All scheduled videos so far are securely active in YouTube Studio.")
                break

        # Clean up heavy temp video file
        for p in [img_path, thumb_path, voice_path, mp4_path]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    print(f"\n========================================================")
    print(f">> BATCH COMPLETE: {scheduled_count} videos newly scheduled into YouTube Studio!")
    print("========================================================\n")

if __name__ == "__main__":
    replenish_queue()
