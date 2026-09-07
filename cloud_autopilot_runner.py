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
    """Renders pixel-perfect 1080x1920 infographic with strict mobile Reels/Shorts safe zone (no cutoff)."""
    img = Image.new("RGB", (1080, 1920), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Background subtle grid lines
    for gy in range(150, 1850, 110):
        draw.line([(50, gy), (1030, gy)], fill=GRID_COLOR, width=1)
    for gx in range(50, 1050, 120):
        draw.line([(gx, 150), (gx, 1850)], fill=GRID_COLOR, width=1)

    # SAFE ZONE COORDINATES:
    # Left margin = 90, Card width = 840 (Right edge = 930 -> leaves 150px for like/comment buttons!)
    # Top safe start = Y 215, Bottom safe limit = Y 1405 (leaves 515px for IG caption/audio overlay!)
    cx_left = 90
    cw = 840

    # 1. Category and Brand Top Badges (Y = 215 to 260)
    pill_font = get_font(20, bold=True)
    
    # Left: THE WEALTH BLUEPRINT
    brand_text = "THE WEALTH BLUEPRINT"
    b_w = 320
    draw_card(draw, cx_left, 215, b_w, 44, border_color=GREEN, bg_color=(10, 28, 22), radius=22, border_width=2)
    b_bbox = pill_font.getbbox(brand_text)
    b_tx = cx_left + (b_w - (b_bbox[2] - b_bbox[0])) // 2
    b_ty = 215 + (44 - (b_bbox[3] - b_bbox[1])) // 2
    draw.text((b_tx, b_ty), brand_text, fill=GREEN, font=pill_font)

    # Right: Category
    cat_prefix = "[INDIA] " if item.get("region") == "INDIA" else ""
    cat_text = f"{cat_prefix}{strip_emojis(item['category']).upper()}"
    cat_w = 400
    cat_x = cx_left + cw - cat_w
    draw_card(draw, cat_x, 215, cat_w, 44, border_color=GOLD, bg_color=(28, 24, 10), radius=22, border_width=2)
    c_bbox = pill_font.getbbox(cat_text)
    c_tx = cat_x + (cat_w - (c_bbox[2] - c_bbox[0])) // 2
    c_ty = 215 + (44 - (c_bbox[3] - c_bbox[1])) // 2
    draw.text((c_tx, c_ty), cat_text, fill=GOLD, font=pill_font)

    # 2. Main Hook Headline (Y = 275 to 335)
    title = strip_emojis(item["title"].split("#")[0]).strip()
    title_size = 40
    title_font = get_font(title_size, bold=True)
    t_bbox = title_font.getbbox(title)
    while (t_bbox[2] - t_bbox[0]) > (cw - 20) and title_size > 24:
        title_size -= 2
        title_font = get_font(title_size, bold=True)
        t_bbox = title_font.getbbox(title)
    draw.text((cx_left, 275), title, fill=WHITE, font=title_font)

    # Subtitle Hook (Y = 335 to 365)
    sub = item["sub"]
    sub_font = get_font(21, bold=False)
    draw.text((cx_left, 335), sub, fill=MUTED, font=sub_font)

    h2_font = get_font(27, bold=True)
    body_font = get_font(22, bold=False)
    stat_font = get_font(25, bold=True)

    # 3. Card 1: Mistake / Trap (Y = 385 to 645, H = 260)
    c1_y, c1_h = 385, 260
    draw_card(draw, cx_left, c1_y, cw, c1_h, border_color=RED, bg_color=(24, 12, 16))
    draw.text((cx_left + 35, c1_y + 22), f"[!]  {item['c1_t']}", fill=RED, font=h2_font)
    b1_fn = BADGE_MAP.get(item.get("b1", "warning"), draw_warning_badge)
    b1_fn(draw, cx_left + cw - 55, c1_y + 36, size=38)

    lines1 = wrap_text(item["c1_d"], body_font, cw - 120)
    ty = c1_y + 75
    for l in lines1[:4]:
        draw.text((cx_left + 35, ty), l, fill=WHITE, font=body_font)
        ty += 38

    # Arrow 1 (Y = 655 to 690)
    draw.line([(540, 655), (540, 688)], fill=CYAN, width=5)
    draw.polygon([(528, 680), (552, 680), (540, 693)], fill=CYAN)

    # 4. Card 2: Strategy / Blueprint (Y = 700 to 1030, H = 330)
    c2_y, c2_h = 700, 330
    draw_card(draw, cx_left, c2_y, cw, c2_h, border_color=GREEN, bg_color=(12, 28, 22))
    draw.text((cx_left + 35, c2_y + 22), f"[>]  {item['c2_t']}", fill=GREEN, font=h2_font)
    b2_fn = BADGE_MAP.get(item.get("b2", "card"), draw_credit_card_badge)
    b2_fn(draw, cx_left + cw - 55, c2_y + 36, size=38)

    ty = c2_y + 75
    for block in item["c2_d"].split("\n"):
        w_lines = wrap_text(block, body_font, cw - 120)
        for l in w_lines:
            draw.text((cx_left + 35, ty), l, fill=WHITE, font=body_font)
            ty += 38
        ty += 6

    # Arrow 2 (Y = 1040 to 1075)
    draw.line([(540, 1040), (540, 1073)], fill=CYAN, width=5)
    draw.polygon([(528, 1065), (552, 1065), (540, 1078)], fill=CYAN)

    # 5. Card 3: Payoff / Result (Y = 1085 to 1325, H = 240)
    c3_y, c3_h = 1085, 240
    draw_card(draw, cx_left, c3_y, cw, c3_h, border_color=GOLD, bg_color=(30, 26, 12))
    draw.text((cx_left + 35, c3_y + 22), f"[$]  {item['c3_t']}", fill=GOLD, font=h2_font)
    b3_fn = BADGE_MAP.get(item.get("b3", "bull"), draw_bull_badge)
    b3_fn(draw, cx_left + cw - 55, c3_y + 36, size=38)

    ty = c3_y + 75
    for block in item["c3_d"].split("\n"):
        w_lines = wrap_text(block, stat_font, cw - 120)
        for l in w_lines:
            is_accent = any(s in l for s in ["PAYOFF", "$", "₹", "APR", "Jump", "+"])
            draw.text((cx_left + 35, ty), l, fill=GREEN if is_accent else WHITE, font=stat_font)
            ty += 42
        ty += 6

    # 6. Bottom Brand Callout (Y = 1345 to 1405, H = 60)
    foot_font = get_font(23, bold=True)
    foot_text = "SAVE THIS REEL   •   FOLLOW FOR ZERO-BS WEALTH"
    draw_card(draw, cx_left, 1345, cw, 58, border_color=GREEN, bg_color=(12, 26, 22), radius=16, border_width=2)
    f_bbox = foot_font.getbbox(foot_text)
    f_tx = cx_left + (cw - (f_bbox[2] - f_bbox[0])) // 2
    f_ty = 1345 + (58 - (f_bbox[3] - f_bbox[1])) // 2
    draw.text((f_tx, f_ty), foot_text, fill=GREEN, font=foot_font)

    # 7. Safe Zone Guarantee: Y = 1405 to 1920 is strictly preserved for Instagram/Shorts native overlay
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
        "[1:a]volume=1.20[a1];"
        "[2:a]volume=0.45[a2];"
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
    ig_session_env = os.environ.get("INSTAGRAM_SESSION_JSON")
    session_file = os.path.join(BASE_DIR, "ig_session.json")

    if ig_session_env and not os.path.exists(session_file):
        with open(session_file, "w", encoding="utf-8") as f:
            f.write(ig_session_env)

    if (ig_user and ig_pass) or ig_token or ig_session_env or os.path.exists(session_file):
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
