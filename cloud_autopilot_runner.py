import os
import sys
import json
import time
import argparse
import asyncio
import subprocess
import shutil
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

try:
    from infinite_content_engine import load_dynamic_catalog, generate_and_append_new_post
    CATALOG_100 = load_dynamic_catalog()
except Exception:
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

def render_progressive_frames(item: dict, out_dir: str, scale: int = 2):
    """Renders 3 progressive visual states in 4K Ultra HD (2160x3840) for extreme clarity and retention."""
    os.makedirs(out_dir, exist_ok=True)
    frames = []

    width = 1080 * scale
    height = 1920 * scale
    cx_left = 90 * scale
    cw = 840 * scale
    pill_font = get_font(20 * scale, bold=True)
    h2_font = get_font(27 * scale, bold=True)
    body_font = get_font(22 * scale, bold=False)
    stat_font = get_font(25 * scale, bold=True)

    for stage in [1, 2, 3]:
        img = Image.new("RGB", (width, height), color=BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Tech grid background
        for gy in range(150 * scale, 1850 * scale, 110 * scale):
            draw.line([(50 * scale, gy), (1030 * scale, gy)], fill=GRID_COLOR, width=1 * scale)
        for gx in range(50 * scale, 1050 * scale, 120 * scale):
            draw.line([(gx, 150 * scale), (gx, 1850 * scale)], fill=GRID_COLOR, width=1 * scale)

        # 1. Category and Brand Top Badges
        brand_text = "THE WEALTH BLUEPRINT"
        b_w = 320 * scale
        b_h = 44 * scale
        b_y = 215 * scale
        draw_card(draw, cx_left, b_y, b_w, b_h, border_color=GREEN, bg_color=(10, 28, 22), radius=22 * scale, border_width=2 * scale)
        b_bbox = pill_font.getbbox(brand_text)
        draw.text((cx_left + (b_w - (b_bbox[2] - b_bbox[0])) // 2, b_y + (b_h - (b_bbox[3] - b_bbox[1])) // 2), brand_text, fill=GREEN, font=pill_font)

        cat_prefix = "[INDIA] " if item.get("region") == "INDIA" else ""
        cat_text = f"{cat_prefix}{strip_emojis(item['category']).upper()}"
        cat_w = 400 * scale
        cat_x = cx_left + cw - cat_w
        draw_card(draw, cat_x, b_y, cat_w, b_h, border_color=GOLD, bg_color=(28, 24, 10), radius=22 * scale, border_width=2 * scale)
        c_bbox = pill_font.getbbox(cat_text)
        draw.text((cat_x + (cat_w - (c_bbox[2] - c_bbox[0])) // 2, b_y + (b_h - (c_bbox[3] - c_bbox[1])) // 2), cat_text, fill=GOLD, font=pill_font)

        # 2. Main Hook Headline
        title = strip_emojis(item["title"].split("#")[0]).strip()
        title_size = 40 * scale
        title_font = get_font(title_size, bold=True)
        t_bbox = title_font.getbbox(title)
        while (t_bbox[2] - t_bbox[0]) > (cw - 20 * scale) and title_size > (24 * scale):
            title_size -= (2 * scale)
            title_font = get_font(title_size, bold=True)
            t_bbox = title_font.getbbox(title)
        draw.text((cx_left, 275 * scale), title, fill=WHITE, font=title_font)

        sub_font = get_font(21 * scale, bold=False)
        draw.text((cx_left, 335 * scale), item.get("sub", ""), fill=MUTED, font=sub_font)

        # 3. Card 1: Mistake / Trap
        c1_y, c1_h = 385 * scale, 260 * scale
        draw_card(draw, cx_left, c1_y, cw, c1_h, border_color=RED, bg_color=(28, 12, 16), border_width=3 * scale if stage == 1 else 2 * scale, radius=24 * scale)
        draw.text((cx_left + 35 * scale, c1_y + 22 * scale), f"[!]  {item['c1_t']}", fill=RED, font=h2_font)
        
        if stage == 1:
            draw_card(draw, cx_left + cw - 170 * scale, c1_y + 18 * scale, 140 * scale, 34 * scale, border_color=RED, bg_color=(50, 15, 22), radius=17 * scale, border_width=2 * scale)
            h_f = get_font(16 * scale, bold=True)
            draw.text((cx_left + cw - 155 * scale, c1_y + 25 * scale), "THE TRAP", fill=RED, font=h_f)

        lines1 = wrap_text(item["c1_d"], body_font, cw - 120 * scale)
        ty = c1_y + 75 * scale
        for l in lines1[:4]:
            draw.text((cx_left + 35 * scale, ty), l, fill=WHITE, font=body_font)
            ty += 38 * scale

        # Arrow 1
        arrow_x = 540 * scale
        draw.line([(arrow_x, 655 * scale), (arrow_x, 688 * scale)], fill=CYAN if stage >= 2 else (30, 45, 60), width=5 * scale)
        draw.polygon([(arrow_x - 12 * scale, 680 * scale), (arrow_x + 12 * scale, 680 * scale), (arrow_x, 693 * scale)], fill=CYAN if stage >= 2 else (30, 45, 60))

        # 4. Card 2: Strategy / Blueprint
        c2_y, c2_h = 700 * scale, 330 * scale
        if stage >= 2:
            draw_card(draw, cx_left, c2_y, cw, c2_h, border_color=GREEN, bg_color=(12, 28, 22), border_width=3 * scale if stage == 2 else 2 * scale, radius=24 * scale)
            draw.text((cx_left + 35 * scale, c2_y + 22 * scale), f"[>]  {item['c2_t']}", fill=GREEN, font=h2_font)
            if stage == 2:
                draw_card(draw, cx_left + cw - 190 * scale, c2_y + 18 * scale, 160 * scale, 34 * scale, border_color=GREEN, bg_color=(15, 45, 25), radius=17 * scale, border_width=2 * scale)
                h_f = get_font(16 * scale, bold=True)
                draw.text((cx_left + cw - 178 * scale, c2_y + 25 * scale), "THE BLUEPRINT", fill=GREEN, font=h_f)

            ty = c2_y + 75 * scale
            for block in item["c2_d"].split("\n"):
                w_lines = wrap_text(block, body_font, cw - 120 * scale)
                for l in w_lines:
                    draw.text((cx_left + 35 * scale, ty), l, fill=WHITE, font=body_font)
                    ty += 38 * scale
                ty += 6 * scale
        else:
            draw_card(draw, cx_left, c2_y, cw, c2_h, border_color=(35, 42, 60), bg_color=(12, 14, 20), border_width=2 * scale, radius=24 * scale)
            lock_f = get_font(24 * scale, bold=True)
            draw.text((cx_left + 40 * scale, c2_y + 140 * scale), "STEP 2: REVEALING THE WEALTH BLUEPRINT...", fill=(80, 95, 125), font=lock_f)

        # Arrow 2
        draw.line([(arrow_x, 1040 * scale), (arrow_x, 1073 * scale)], fill=CYAN if stage == 3 else (30, 45, 60), width=5 * scale)
        draw.polygon([(arrow_x - 12 * scale, 1065 * scale), (arrow_x + 12 * scale, 1065 * scale), (arrow_x, 1078 * scale)], fill=CYAN if stage == 3 else (30, 45, 60))

        # 5. Card 3: Payoff / Result
        c3_y, c3_h = 1085 * scale, 240 * scale
        if stage == 3:
            draw_card(draw, cx_left, c3_y, cw, c3_h, border_color=GOLD, bg_color=(32, 28, 12), border_width=3 * scale, radius=24 * scale)
            draw.text((cx_left + 35 * scale, c3_y + 22 * scale), f"[$]  {item['c3_t']}", fill=GOLD, font=h2_font)
            draw_card(draw, cx_left + cw - 180 * scale, c3_y + 18 * scale, 150 * scale, 34 * scale, border_color=GOLD, bg_color=(50, 40, 15), radius=17 * scale, border_width=2 * scale)
            h_f = get_font(16 * scale, bold=True)
            draw.text((cx_left + cw - 168 * scale, c3_y + 25 * scale), "THE ROI PAYOFF", fill=GOLD, font=h_f)

            ty = c3_y + 75 * scale
            for block in item["c3_d"].split("\n"):
                w_lines = wrap_text(block, stat_font, cw - 120 * scale)
                for l in w_lines:
                    is_accent = any(s in l for s in ["PAYOFF", "$", "₹", "APR", "Jump", "+", "Saves", "0%", "100%"])
                    draw.text((cx_left + 35 * scale, ty), l, fill=GREEN if is_accent else WHITE, font=stat_font)
                    ty += 42 * scale
                ty += 6 * scale
        else:
            draw_card(draw, cx_left, c3_y, cw, c3_h, border_color=(35, 42, 60), bg_color=(12, 14, 20), border_width=2 * scale, radius=24 * scale)
            lock_f = get_font(24 * scale, bold=True)
            draw.text((cx_left + 40 * scale, c3_y + 105 * scale), "STEP 3: CALCULATING YOUR FINANCIAL PAYOFF...", fill=(80, 95, 125), font=lock_f)

        # 6. Bottom Brand Callout
        foot_font = get_font(23 * scale, bold=True)
        foot_text = "SAVE THIS REEL   •   FOLLOW FOR ZERO-BS WEALTH"
        draw_card(draw, cx_left, 1345 * scale, cw, 58 * scale, border_color=GREEN if stage == 3 else CARD_BORDER, bg_color=(12, 26, 22) if stage == 3 else CARD_BG, radius=16 * scale, border_width=2 * scale)
        f_bbox = foot_font.getbbox(foot_text)
        draw.text((cx_left + (cw - (f_bbox[2] - f_bbox[0])) // 2, 1345 * scale + (58 * scale - (f_bbox[3] - f_bbox[1])) // 2), foot_text, fill=GREEN if stage == 3 else MUTED, font=foot_font)

        frame_path = os.path.join(out_dir, f"frame_{stage}.png")
        img.save(frame_path, "PNG")
        frames.append(frame_path)

    return frames

async def generate_speech_async(script: str, out_mp3: str, voice: str):
    clean = script.replace("\n", " ").strip()
    communicate = edge_tts.Communicate(clean, voice, rate="+12%")
    await communicate.save(out_mp3)
    return out_mp3

def assemble_dynamic_video(frames: list, voice_path: str, out_mp4: str):
    """Combines 3 progressive visual frames with multi-stage reveals, 44.1kHz Stereo, and FastStart."""
    if not os.path.exists(BGM_PATH):
        generate_ambient_background_music(BGM_PATH, 75.0)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    # Get voice duration via ffprobe
    cmd_probe = [ffmpeg, "-i", voice_path]
    probe_res = subprocess.run(cmd_probe, capture_output=True, text=True)
    import re
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", probe_res.stderr)
    total_sec = 24.0
    if dur_match:
        h, m, s = map(float, dur_match.groups())
        total_sec = h * 3600 + m * 60 + s

    # Progressive timing cuts: Stage 1 = 30%, Stage 2 = 40%, Stage 3 = 30%
    d1 = round(total_sec * 0.30, 2)
    d2 = round(total_sec * 0.40, 2)
    d3 = round(total_sec - d1 - d2, 2)

    concat_file = os.path.join(os.path.dirname(out_mp4), "concat_list.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write(f"file '{frames[0]}'\nduration {d1}\n")
        f.write(f"file '{frames[1]}'\nduration {d2}\n")
        f.write(f"file '{frames[2]}'\nduration {d3}\n")
        f.write(f"file '{frames[2]}'\n")

    cmd = [
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", voice_path,
        "-stream_loop", "-1", "-i", BGM_PATH,
        "-filter_complex",
        "[1:a]volume=1.20[a1];"
        "[2:a]volume=0.38[a2];"
        "[a1][a2]amix=inputs=2:duration=first[amixed];"
        "[amixed]aformat=sample_rates=44100:channel_layouts=stereo[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-r", "25",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        out_mp4
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(concat_file):
        os.remove(concat_file)

    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg dynamic assembly error: {res.stderr}")
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
    published_ids = set()
    for entry in history:
        if entry.get("instagram_url") or entry.get("instagram_status") in ["PUBLISHED", "Published Live as Reel"]:
            if entry.get("id"):
                published_ids.add(entry["id"])

    try:
        from infinite_content_engine import load_dynamic_catalog
        catalog = load_dynamic_catalog()
    except Exception:
        catalog = CATALOG_100

    for item in catalog:
        if item["id"] not in published_ids:
            return item
    return None

def publish_entry(item: dict, dry_run: bool = False):
    item = clean_str(item)
    p_id = item["id"]
    day = item.get("day") or ((p_id + 2) // 3)
    slot = item.get("slot") or (((p_id - 1) % 3) + 1)
    region = item.get("region", "GLOBAL")
    voice = item.get("voice", "en-US-ChristopherNeural")
    print(f"\n========================================================")
    print(f">> CLOUD AUTOPILOT: PROCESSING POST #{p_id:03d} (Day {day:02d} / Slot {slot})")
    print(f">> Title: {item.get('title', '')}")
    print(f">> Region: {region} | Voice: {voice}")
    print(f"========================================================")

    # 1. Render progressive frames for dynamic multi-stage reveal
    frames_dir = os.path.join(TEMP_DIR, f"post_{p_id:03d}_frames")
    print(">> Rendering 3-stage progressive dynamic frames (Trap -> Blueprint -> ROI Payoff)...")
    frames = render_progressive_frames(item, frames_dir)
    img_path = frames[-1]  # Final complete frame used for thumbnail / previews

    # 2. Generate neural voiceover (+12% rate for rapid mobile retention)
    voice_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}_voice.mp3")
    print(f">> Synthesizing high-retention rapid voiceover ({item['voice']})...")
    asyncio.run(generate_speech_async(item["script"], voice_path, item["voice"]))

    # 3. Assemble dynamic MP4 (3-stage visual reveals, 44.1kHz Stereo, FastStart)
    mp4_path = os.path.join(TEMP_DIR, f"post_{p_id:03d}.mp4")
    print(">> Compositing high-retention dynamic video...")
    assemble_dynamic_video(frames, voice_path, mp4_path)
    sz_mb = os.path.getsize(mp4_path) / (1024 * 1024)
    print(f"[OK] Dynamic Video ready: {os.path.basename(mp4_path)} ({sz_mb:.2f} MB)")

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
        "day": day,
        "slot": slot,
        "region": region,
        "title": item.get("title", ""),
        "timestamp": datetime.now().isoformat()
    }

    # YouTube upload check
    cal_file = os.path.join(BASE_DIR, "SCHEDULE_CALENDAR.json")
    already_scheduled_url = None
    if os.path.exists(cal_file):
        try:
            with open(cal_file, "r", encoding="utf-8") as f:
                cal_data = json.load(f)
            cal_match = next((c for c in cal_data if c["id"] == p_id), None)
            if cal_match and cal_match.get("youtube_url"):
                already_scheduled_url = cal_match["youtube_url"]
        except Exception:
            pass

    if already_scheduled_url:
        results["youtube_url"] = already_scheduled_url
        print(f"   [OK] YouTube Shorts: Pre-scheduled in YouTube Studio at {already_scheduled_url}")
    else:
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

    # 6. Infinite Replenishment Loop: synthesize a brand-new viral post and append to catalog queue!
    if not dry_run:
        try:
            from infinite_content_engine import generate_and_append_new_post
            replenished = generate_and_append_new_post()
            print(f">> [INFINITE AUTOPILOT] Queue replenished with Post #{replenished['id']}: '{replenished['title']}'")
        except Exception as e:
            print(f"[!] Warning: Could not replenish queue: {e}")

    # Clean up temporary heavy video files to keep runner clean
    for p in [voice_path, mp4_path]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass
    if os.path.exists(frames_dir):
        try:
            shutil.rmtree(frames_dir, ignore_errors=True)
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
