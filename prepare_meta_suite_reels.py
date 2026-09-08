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

from cloud_autopilot_runner import render_poster, assemble_mp4, generate_speech_async
from infinite_content_engine import load_dynamic_catalog
from PIL import Image

PACKAGE_DIR = os.path.join(BASE_DIR, "meta_bulk_upload_package")
os.makedirs(PACKAGE_DIR, exist_ok=True)

# 3-Times Daily Cadence:
# Slot 1: 09:00 AM IST (Morning Commute)
# Slot 2: 01:30 PM IST (Lunch Break)
# Slot 3: 08:30 PM IST (Prime Evening)
SLOTS = [
    # Wednesday, Sep 09
    {"post_id": 8,  "slot_str": "Wed Sep 09, 09:00 AM IST"},
    {"post_id": 9,  "slot_str": "Wed Sep 09, 01:30 PM IST"},
    {"post_id": 10, "slot_str": "Wed Sep 09, 08:30 PM IST"},
    # Thursday, Sep 10
    {"post_id": 11, "slot_str": "Thu Sep 10, 09:00 AM IST"},
    {"post_id": 12, "slot_str": "Thu Sep 10, 01:30 PM IST"},
    {"post_id": 13, "slot_str": "Thu Sep 10, 08:30 PM IST"},
    # Friday, Sep 11
    {"post_id": 14, "slot_str": "Fri Sep 11, 09:00 AM IST"},
    {"post_id": 15, "slot_str": "Fri Sep 11, 01:30 PM IST"},
    {"post_id": 16, "slot_str": "Fri Sep 11, 08:30 PM IST"},
    # Saturday, Sep 12
    {"post_id": 17, "slot_str": "Sat Sep 12, 09:00 AM IST"},
    {"post_id": 18, "slot_str": "Sat Sep 12, 01:30 PM IST"},
    {"post_id": 19, "slot_str": "Sat Sep 12, 08:30 PM IST"},
    # Sunday, Sep 13
    {"post_id": 20, "slot_str": "Sun Sep 13, 09:00 AM IST"},
    {"post_id": 21, "slot_str": "Sun Sep 13, 01:30 PM IST"},
    {"post_id": 22, "slot_str": "Sun Sep 13, 08:30 PM IST"},
]

def build_package():
    catalog = load_dynamic_catalog()
    catalog_by_id = {item["id"]: item for item in catalog}

    print("========================================================")
    print("  PREPARING 3X DAILY BULK REELS FOR META BUSINESS SUITE")
    print(f"  Target Directory: {PACKAGE_DIR}")
    print(f"  Total Slots to Schedule: {len(SLOTS)} (5 Days on 3x Autopilot)")
    print("========================================================\n")

    manifest = []

    for slot in SLOTS:
        p_id = slot["post_id"]
        item = catalog_by_id.get(p_id)
        if not item:
            print(f"[!] Post #{p_id} not found in catalog, skipping.")
            continue

        clean_slug = "".join(c for c in item["title"][:25] if c.isalnum() or c in " _-").strip().replace(" ", "_")
        v_name = f"Reel_{p_id:02d}_{clean_slug}.mp4"
        thumb_name = f"Reel_{p_id:02d}_{clean_slug}_thumb.jpg"
        cap_name = f"Reel_{p_id:02d}_{clean_slug}_caption.txt"

        mp4_path = os.path.join(PACKAGE_DIR, v_name)
        thumb_path = os.path.join(PACKAGE_DIR, thumb_name)
        cap_path = os.path.join(PACKAGE_DIR, cap_name)
        temp_png = os.path.join(PACKAGE_DIR, f"temp_{p_id:02d}.png")
        temp_voice = os.path.join(PACKAGE_DIR, f"temp_{p_id:02d}.mp3")

        # Check if already rendered
        if os.path.exists(mp4_path) and os.path.getsize(mp4_path) > 100000 and os.path.exists(thumb_path):
            print(f"[✓] Reel #{p_id:02d} already rendered: {v_name}")
        else:
            print(f">> Rendering Post #{p_id:02d}: {item['title']}")
            print(f"   Scheduled Slot: {slot['slot_str']}")

            # 1. Poster in Safe Zone
            render_poster(item, temp_png)
            Image.open(temp_png).convert("RGB").save(thumb_path, "JPEG", quality=95)

            # 2. Voiceover & Composite
            asyncio.run(generate_speech_async(item["script"], temp_voice, item["voice"]))
            assemble_mp4(temp_png, temp_voice, mp4_path)

            # Clean temp
            for p in [temp_png, temp_voice]:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass

        # 3. Caption text file
        caption_text = f"""{item['title']}

{item['sub']}

THE TRAP:
{item['c1_t']}
{item['c1_d']}

THE BLUEPRINT:
{item['c2_t']}
{item['c2_d']}

THE PAYOFF:
{item['c3_t']}
{item['c3_d']}

Follow @thewealthblueprint10 for daily wealth loopholes.
Save this reel so you don't lose it!

.
.
#wealth #personalfinance #moneyhacks #financialfreedom #smartmoney #reelsindia #shorts #investing"""

        with open(cap_path, "w", encoding="utf-8") as cf:
            cf.write(caption_text)

        manifest.append({
            "post_id": p_id,
            "title": item["title"],
            "video_file": v_name,
            "thumb_file": thumb_name,
            "caption_file": cap_name,
            "scheduled_time": slot["slot_str"]
        })

    # Write Master Guide
    guide_path = os.path.join(PACKAGE_DIR, "00_SCHEDULE_GUIDE.txt")
    with open(guide_path, "w", encoding="utf-8") as gf:
        gf.write("META BUSINESS SUITE - 3X DAILY BULK UPLOAD SCHEDULE GUIDE\n")
        gf.write("============================================================\n")
        gf.write("Cadence: 3x Daily (09:00 AM, 01:30 PM, 08:30 PM IST)\n")
        gf.write("Target Account: @thewealthblueprint10\n")
        gf.write("Server-Side Cloud Scheduling: Videos publish on autopilot even with laptop powered off!\n\n")

        for m in manifest:
            gf.write(f"Post #{m['post_id']:02d}: {m['title']}\n")
            gf.write(f"  -> File:      {m['video_file']}\n")
            gf.write(f"  -> Thumbnail: {m['thumb_file']}\n")
            gf.write(f"  -> Schedule:  {m['scheduled_time']}\n\n")

    print("\n[✓] Package creation complete!")
    print(f"[✓] Schedule guide generated at: {guide_path}")

if __name__ == "__main__":
    build_package()
