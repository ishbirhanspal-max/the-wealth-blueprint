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
from infinite_content_engine import load_dynamic_catalog
from PIL import Image
from instagrapi import Client

TEMP_DIR = os.path.join(BASE_DIR, "output", "temp_ig_sync")
os.makedirs(TEMP_DIR, exist_ok=True)

def sync_instagram(post_ids=[5, 6, 7]):
    session_file = os.path.join(BASE_DIR, "ig_session.json")
    if not os.path.exists(session_file):
        print("[!] Error: ig_session.json not found.")
        return

    cl = Client()
    cl.load_settings(session_file)
    print(f">> Connected to Instagram as: {cl.username}")

    catalog = load_dynamic_catalog()
    catalog_by_id = {item["id"]: item for item in catalog}
    history = load_history()

    for p_id in post_ids:
        item = catalog_by_id.get(p_id)
        if not item:
            print(f"[!] Post #{p_id} not found in catalog.")
            continue

        print(f"\n>> Publishing Post #{p_id:02d} to Instagram Reels: {item['title']}")
        img_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.png")
        thumb_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_thumb.jpg")
        voice_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_voice.mp3")
        mp4_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.mp4")

        # 1. Render Safe Zone Poster
        render_poster(item, img_path)
        Image.open(img_path).convert("RGB").save(thumb_path, "JPEG", quality=95)

        # 2. Voiceover & Video Composite
        asyncio.run(generate_speech_async(item["script"], voice_path, item["voice"]))
        assemble_mp4(img_path, voice_path, mp4_path)

        # 3. Instagram Caption
        ig_caption = f"""{item['title']}\n\n{item['sub']}\n\nTHE TRAP:\n{item['c1_t']}\n{item['c1_d']}\n\nTHE BLUEPRINT:\n{item['c2_t']}\n{item['c2_d']}\n\nTHE PAYOFF:\n{item['c3_t']}\n{item['c3_d']}\n\nFollow @thewealthblueprint10 for daily wealth loopholes.\nSave this reel so you don't lose it!\n\n.\n.\n.\n#wealth #personalfinance #moneytips #bankinghacks #creditcard #investing #financialfreedom #smartmoney"""

        try:
            print(f"   Uploading video and safe-zone thumbnail to Instagram...")
            media = cl.clip_upload(mp4_path, caption=ig_caption, thumbnail=thumb_path)
            ig_url = f"https://www.instagram.com/reel/{media.code}/"
            print(f"   [SUCCESS] Published Reel: {ig_url}")

            # Update history
            for entry in history:
                if entry.get("id") == p_id:
                    entry["instagram_url"] = ig_url
                    entry["instagram_status"] = "Published Live as Reel"
                    break
            else:
                history.append({
                    "id": p_id,
                    "title": item["title"],
                    "timestamp": datetime.now().isoformat(),
                    "instagram_url": ig_url,
                    "instagram_status": "Published Live as Reel"
                })
            save_history(history)

        except Exception as e:
            print(f"   [!] Instagram upload failed for Post #{p_id}: {e}")

        # Clean up temp
        for p in [img_path, thumb_path, voice_path, mp4_path]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    print("\n>> Instagram sync complete!")

if __name__ == "__main__":
    sync_instagram([5, 6, 7])
