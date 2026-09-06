import os
import sys
import json
import time
import argparse
import asyncio
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import edge_tts
from dotenv import load_dotenv

# Fix encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def clean_str(val):
    if isinstance(val, str):
        try:
            return val.encode("utf-16", "surrogatepass").decode("utf-16")
        except Exception:
            return val
    elif isinstance(val, list):
        return [clean_str(x) for x in val]
    elif isinstance(val, dict):
        return {k: clean_str(v) for k, v in val.items()}
    return val

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from content_catalog_100 import CATALOG_100
from audio_synth import generate_ambient_background_music

# Directories
TEMP_DIR = os.path.join(BASE_DIR, "output", "temp_cloud")
PUBLISHED_DIR = os.path.join(BASE_DIR, "published_videos")
HISTORY_FILE = os.path.join(PUBLISHED_DIR, "published_history.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BGM_PATH = os.path.join(ASSETS_DIR, "ambient_beat.wav")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(PUBLISHED_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# Colors
BG_COLOR = (9, 11, 16)
CARD_BG = (17, 20, 30)
CARD_BORDER = (30, 35, 51)
WHITE = (245, 246, 248)
MUTED = (156, 163, 175)
GREEN = (0, 242, 152)
GOLD = (255, 184, 0)
RED = (255, 75, 75)
CYAN = (0, 212, 255)
GRID_COLOR = (18, 22, 34)

def get_font(size: int, bold: bool = False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "seguiemj.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def wrap_text(text: str, font, max_width: int):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        bbox = font.getbbox(test_line)
        if (bbox[2] - bbox[0]) <= max_width:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

def draw_card(draw, x, y, w, h, border_color=CARD_BORDER, bg_color=CARD_BG, radius=24, border_width=2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, outline=border_color, width=border_width)

def draw_warning_badge(draw, cx, cy, size=46):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(45, 15, 20), outline=RED, width=2)
    pts = [(cx, cy - r + 10), (cx - r + 10, cy + r - 10), (cx + r - 10, cy + r - 10)]
    draw.polygon(pts, outline=RED, fill=(70, 20, 25))
    draw.line([(cx, cy - 6), (cx, cy + 4)], fill=WHITE, width=3)
    draw.ellipse([cx - 2, cy + 8, cx + 2, cy + 12], fill=WHITE)

def draw_credit_card_badge(draw, cx, cy, size=46):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 30, 40), outline=CYAN, width=2)
    cw, ch = 28, 18
    draw.rounded_rectangle([cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], radius=3, outline=WHITE, width=2)
    draw.rounded_rectangle([cx - cw//2 + 3, cy - 3, cx - cw//2 + 9, cy + 3], radius=1, fill=GOLD)
    draw.line([(cx - 2, cy), (cx + cw//2 - 4, cy)], fill=CYAN, width=2)

def draw_bull_badge(draw, cx, cy, size=46):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 35, 25), outline=GREEN, width=2)
    head_pts = [(cx - 10, cy - 6), (cx + 10, cy - 6), (cx + 6, cy + 14), (cx - 6, cy + 14)]
    draw.polygon(head_pts, fill=GREEN)
    draw.line([(cx - 10, cy - 4), (cx - 18, cy - 14)], fill=CYAN, width=3)
    draw.line([(cx + 10, cy - 4), (cx + 18, cy - 14)], fill=CYAN, width=3)
    draw.ellipse([cx - 5, cy + 2, cx - 2, cy + 5], fill=BG_COLOR)
    draw.ellipse([cx + 2, cy + 2, cx + 5, cy + 5], fill=BG_COLOR)
    draw.line([(cx - 20, cy + 8), (cx + 20, cy - 12)], fill=GOLD, width=2)
    draw.polygon([(cx + 20, cy - 12), (cx + 12, cy - 12), (cx + 20, cy - 4)], fill=GOLD)

def draw_growth_chart_badge(draw, cx, cy, size=46):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 30, 25), outline=GREEN, width=2)
    for i, h in enumerate([8, 14, 22, 30]):
        bx = cx - 24 + (i * 12)
        draw.rounded_rectangle([bx, cy + 16 - h, bx + 8, cy + 16], radius=2, fill=GREEN)
    draw.line([(cx - 26, cy + 6), (cx + 26, cy - 20)], fill=GOLD, width=3)
    draw.polygon([(cx + 26, cy - 20), (cx + 15, cy - 20), (cx + 26, cy - 9)], fill=GOLD)

def draw_vault_badge(draw, cx, cy, size=46):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(35, 30, 10), outline=GOLD, width=2)
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=GOLD, width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    for ang in [0, 60, 120, 180, 240, 300]:
        import math
        rad = math.radians(ang)
        x1 = cx + int(6 * math.cos(rad))
        y1 = cy + int(6 * math.sin(rad))
        x2 = cx + int(14 * math.cos(rad))
        y2 = cy + int(14 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)

def draw_money_stack_badge(draw, cx, cy, size=46):
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(35, 30, 10), outline=GOLD, width=2)
    draw.ellipse([cx - 16, cy + 4, cx + 16, cy + 16], fill=(180, 130, 0), outline=GOLD, width=2)
    draw.ellipse([cx - 16, cy - 4, cx + 16, cy + 8], fill=(210, 150, 0), outline=GOLD, width=2)
    draw.ellipse([cx - 16, cy - 12, cx + 16, cy], fill=GOLD, outline=WHITE, width=2)
    mf = get_font(16, bold=True)
    draw.text((cx - 5, cy - 11), "$", fill=BG_COLOR, font=mf)

BADGE_MAP = {
    "warning": draw_warning_badge,
    "card": draw_credit_card_badge,
    "bull": draw_bull_badge,
    "growth": draw_growth_chart_badge,
    "vault": draw_vault_badge,
    "money": draw_money_stack_badge
}

def strip_emojis(text: str) -> str:
    """Removes unicode emojis for clean PIL text rendering while preserving currency symbols."""
    return "".join(c for c in text if ord(c) < 128 or c in "₹$€£%+-•./'\"()[]:").strip()

def render_poster(item: dict, out_png: str):
    """Renders pixel-perfect 1080x1920 infographic with auto-sized headlines and bounded text."""
    img = Image.new("RGB", (1080, 1920), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Grid background
    for gy in range(120, 1850, 130):
        draw.line([(50, gy), (1030, gy)], fill=GRID_COLOR, width=1)
    for gx in range(50, 1050, 140):
        draw.line([(gx, 120), (gx, 1850)], fill=GRID_COLOR, width=1)

    # Top Left: FOLLOW / SUBSCRIBE Pill
    pill_text = "FOLLOW / SUBSCRIBE"
    pill_font = get_font(24, bold=True)
    pill_w = 380
    draw_card(draw, 70, 75, pill_w, 52, border_color=GREEN, bg_color=(10, 28, 22), radius=26, border_width=2)
    p_bbox = pill_font.getbbox(pill_text)
    p_tx = 70 + (pill_w - (p_bbox[2] - p_bbox[0])) // 2
    p_ty = 75 + (52 - (p_bbox[3] - p_bbox[1])) // 2
    draw.text((p_tx, p_ty), pill_text, fill=GREEN, font=pill_font)

    # Top Right: CATEGORY Pill
    cat_prefix = "[INDIA] " if item.get("region") == "INDIA" else ""
    cat_text = f"CATEGORY: {cat_prefix}{strip_emojis(item['category']).upper()}"
    cat_font = get_font(22, bold=True)
    cat_w = 460
    draw_card(draw, 550, 75, cat_w, 52, border_color=GOLD, bg_color=(28, 24, 10), radius=26, border_width=2)
    c_bbox = cat_font.getbbox(cat_text)
    c_tx = 550 + (cat_w - (c_bbox[2] - c_bbox[0])) // 2
    c_ty = 75 + (52 - (c_bbox[3] - c_bbox[1])) // 2
    draw.text((c_tx, c_ty), cat_text, fill=GOLD, font=cat_font)

    # Main Headline (Auto-fit to 940px)
    title = strip_emojis(item["title"].split("#")[0]).strip()
    title_size = 50
    title_font = get_font(title_size, bold=True)
    t_bbox = title_font.getbbox(title)
    while (t_bbox[2] - t_bbox[0]) > 940 and title_size > 26:
        title_size -= 2
        title_font = get_font(title_size, bold=True)
        t_bbox = title_font.getbbox(title)
    draw.text((70, 150), title, fill=WHITE, font=title_font)

    # Subtitle Hook
    sub = item["sub"]
    sub_size = 25
    sub_font = get_font(sub_size, bold=False)
    s_bbox = sub_font.getbbox(sub)
    while (s_bbox[2] - s_bbox[0]) > 940 and sub_size > 18:
        sub_size -= 1
        sub_font = get_font(sub_size, bold=False)
        s_bbox = sub_font.getbbox(sub)
    draw.text((70, 218), sub, fill=MUTED, font=sub_font)

    h2_font = get_font(32, bold=True)
    body_font = get_font(26, bold=False)
    stat_font = get_font(30, bold=True)

    # --- Card 1: Mistake / Warning ---
    c1_y, c1_h = 270, 420
    draw_card(draw, 70, c1_y, 940, c1_h, border_color=RED, bg_color=(24, 12, 16))
    draw.text((110, c1_y + 30), f"[!]  {item['c1_t']}", fill=RED, font=h2_font)
    b1_fn = BADGE_MAP.get(item.get("b1", "warning"), draw_warning_badge)
    b1_fn(draw, 920, c1_y + 80, size=46)

    lines1 = wrap_text(item["c1_d"], body_font, 740)
    ty = c1_y + 110
    for l in lines1:
        draw.text((110, ty), l, fill=WHITE, font=body_font)
        ty += 44

    # Arrow 1
    draw.line([(540, 695), (540, 740)], fill=CYAN, width=6)
    draw.polygon([(525, 730), (555, 730), (540, 745)], fill=CYAN)

    # --- Card 2: Blueprint Strategy ---
    c2_y, c2_h = 750, 520
    draw_card(draw, 70, c2_y, 940, c2_h, border_color=GREEN, bg_color=(12, 28, 22))
    draw.text((110, c2_y + 30), f"[>]  {item['c2_t']}", fill=GREEN, font=h2_font)
    b2_fn = BADGE_MAP.get(item.get("b2", "card"), draw_credit_card_badge)
    b2_fn(draw, 920, c2_y + 80, size=46)

    ty = c2_y + 110
    for block in item["c2_d"].split("\n"):
        w_lines = wrap_text(block, body_font, 740)
        for l in w_lines:
            draw.text((110, ty), l, fill=WHITE, font=body_font)
            ty += 44
        ty += 8

    # Arrow 2
    draw.line([(540, 1275), (540, 1320)], fill=CYAN, width=6)
    draw.polygon([(525, 1310), (555, 1310), (540, 1325)], fill=CYAN)

    # --- Card 3: Financial Payoff ---
    c3_y, c3_h = 1330, 370
    draw_card(draw, 70, c3_y, 940, c3_h, border_color=GOLD, bg_color=(30, 26, 12))
    draw.text((110, c3_y + 30), f"[$]  {item['c3_t']}", fill=GOLD, font=h2_font)
    b3_fn = BADGE_MAP.get(item.get("b3", "bull"), draw_bull_badge)
    b3_fn(draw, 920, c3_y + 80, size=46)

    ty = c3_y + 110
    for block in item["c3_d"].split("\n"):
        w_lines = wrap_text(block, stat_font, 740)
        for l in w_lines:
            draw.text((110, ty), l, fill=GREEN if ("PAYOFF" in item["c3_t"] or "$" in l or "₹" in l) else WHITE, font=stat_font)
            ty += 50
        ty += 10

    # Bottom CTA Card
    foot_font = get_font(27, bold=True)
    foot_text = "SAVE THIS REEL   |   FOLLOW / SUBSCRIBE"
    draw_card(draw, 70, 1750, 940, 90, border_color=GREEN, bg_color=(12, 26, 22), radius=20, border_width=3)
    f_bbox = foot_font.getbbox(foot_text)
    f_tx = 70 + (940 - (f_bbox[2] - f_bbox[0])) // 2
    f_ty = 1750 + (90 - (f_bbox[3] - f_bbox[1])) // 2
    draw.text((f_tx, f_ty), foot_text, fill=GREEN, font=foot_font)

    img.save(out_png, "PNG")
    return out_png

async def generate_speech_async(script: str, out_mp3: str, voice: str):
    clean = script.replace("\n", " ").strip()
    communicate = edge_tts.Communicate(clean, voice)
    await communicate.save(out_mp3)
    return out_mp3

def assemble_mp4(img_path: str, voice_path: str, out_mp4: str):
    """Combines poster image, neural voice, and looped ducked ambient music with FFmpeg."""
    if not os.path.exists(BGM_PATH):
        generate_ambient_background_music(BGM_PATH, 75.0)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg, "-y",
        "-loop", "1", "-i", img_path,
        "-i", voice_path,
        "-stream_loop", "-1", "-i", BGM_PATH,
        "-filter_complex",
        "[1:a]volume=1.25[a1];"
        "[2:a]volume=0.20[a2];"
        "[a1][a2]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-preset", "ultrafast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render error: {res.stderr}")
    return out_mp4

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

def get_next_item():
    history = load_history()
    published_ids = {entry.get("id") for entry in history}
    for item in CATALOG_100:
        if item["id"] not in published_ids:
            return item
    return None

def publish_entry(item: dict, dry_run: bool = False):
    item = clean_str(item)
    p_id = item["id"]
    print(f"\n========================================================")
    print(f">> CLOUD AUTOPILOT: PROCESSING POST #{p_id:03d} (Day {item['day']:02d} / Slot {item['slot']})")
    print(f">> Title: {item['title']}")
    print(f">> Region: {item['region']} | Voice: {item['voice']}")
    print(f"========================================================")

    # 1. Render poster image
    img_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.png")
    print(">> Rendering 1080x1920 HD infographic poster...")
    render_poster(item, img_path)

    # 2. Generate neural voiceover
    voice_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_voice.mp3")
    print(f">> Synthesizing neural speech ({item['voice']})...")
    asyncio.run(generate_speech_async(item["script"], voice_path, item["voice"]))

    # 3. Assemble MP4
    mp4_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.mp4")
    print(">> Compositing video with lo-fi ambient audio ducking...")
    assemble_mp4(img_path, voice_path, mp4_path)
    sz_mb = os.path.getsize(mp4_path) / (1024 * 1024)
    print(f"[OK] Video ready: {os.path.basename(mp4_path)} ({sz_mb:.2f} MB)")

    # 4. Assemble SEO package
    yt_desc = f"""{item['title']}

⚡ SCRIPT BREAKDOWN:
{item['script']}

👇 FREE FINANCIAL RESOURCES & CREDIT MASTERLIST:
Check our channel bio: @TheWealthBlueprint

📌 PINNED COMMENT:
{item['pinned_comment']}

#Shorts #{item['category'].replace(' ', '')} #TheWealthBlueprint #FinancialFreedom"""

    ig_caption = f"""{item['title']}

💡 THE BLUEPRINT BREAKDOWN:
{item['script']}

📌 SAVE this post to refer back to when managing your money.
👉 Follow @TheWealthBlueprint for daily financial loopholes & wealth systems!

{" ".join(["#" + t.replace(" ", "") for t in item['tags']])} #financialfreedom #personalfinance #wealthmindset #passiveincome #moneymoves"""

    if dry_run:
        print("[DRY-RUN] Verification complete! Video rendered and verified.")
        print(f"[DRY-RUN] Script length: {len(item['script'])} chars")
        return True

    # 5. Live Uploads
    results = {
        "id": p_id,
        "day": item["day"],
        "slot": item["slot"],
        "region": item["region"],
        "title": item["title"],
        "timestamp": datetime.now().isoformat()
    }

    # YouTube upload check
    yt_token = os.environ.get("YOUTUBE_TOKEN_JSON")
    if yt_token or os.path.exists(os.path.join(BASE_DIR, "token.json")) or os.path.exists(os.path.join(BASE_DIR, "client_secret.json")):
        try:
            # If passed via GitHub secret string, write token.json
            if yt_token and not os.path.exists(os.path.join(BASE_DIR, "token.json")):
                with open(os.path.join(BASE_DIR, "token.json"), "w", encoding="utf-8") as f:
                    f.write(yt_token)

            from youtube_uploader import upload_short_to_youtube
            yt_url = upload_short_to_youtube(
                video_path=mp4_path,
                title=item["title"],
                description=yt_desc,
                tags=item["tags"],
                pinned_comment=item["pinned_comment"],
                privacy_status="public"
            )
            results["youtube_url"] = yt_url
            print(f"   [OK] YouTube Shorts: Published at {yt_url}")
        except Exception as e:
            print(f"   [!] YouTube Error: {e}")
            results["youtube_error"] = str(e)
    else:
        print("   [SKIP] YouTube: Credentials not found in environment.")

    # Instagram upload check
    ig_user = os.environ.get("INSTAGRAM_USERNAME")
    ig_pass = os.environ.get("INSTAGRAM_PASSWORD")
    ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")

    if (ig_user and ig_pass) or ig_token:
        try:
            from instagram_uploader import publish_to_instagram
            ig_url = publish_to_instagram(
                video_path=mp4_path,
                caption=ig_caption
            )
            results["instagram_url"] = ig_url
            print(f"   [OK] Instagram Reels: Published at {ig_url}")
        except Exception as e:
            print(f"   [!] Instagram Error: {e}")
            results["instagram_error"] = str(e)
    else:
        print("   [SKIP] Instagram: Credentials not found in environment.")

    # Save to history
    hist = load_history()
    hist.append(results)
    save_history(hist)

    # Clean up temporary heavy video files to keep runner clean
    for p in [img_path, voice_path, mp4_path]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    print(f">> Post #{p_id:03d} logged successfully to history!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Cloud Autopilot Video Runner")
    parser.add_argument("--post-id", type=int, help="Specific post ID (1-100) to render and publish")
    parser.add_argument("--dry-run", action="store_true", help="Render video and verify without live API upload")
    args = parser.parse_args()

    if args.post_id:
        target = next((item for item in CATALOG_100 if item["id"] == args.post_id), None)
        if not target:
            print(f"[!] Post ID {args.post_id} not found in catalog.")
            sys.exit(1)
        publish_entry(target, dry_run=args.dry_run)
    else:
        target = get_next_item()
        if not target:
            print(">> All 100 posts have been published! 50-day campaign complete.")
            sys.exit(0)
        publish_entry(target, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
