import os
from PIL import Image, ImageDraw, ImageFont

BG_COLOR = (9, 11, 16)
CARD_BG = (17, 20, 30)
CARD_BORDER = (30, 35, 51)
WHITE = (245, 246, 248)
MUTED = (156, 163, 175)
GREEN = (0, 242, 152)
GOLD = (255, 184, 0)
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

def render_story_background(title: str, category: str, out_path: str):
    """Renders a 1080x1920 luxury Story background tailored for instagrapi media_share_to_story."""
    img = Image.new("RGB", (1080, 1920), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Subtle background tech grid
    for gy in range(80, 1860, 120):
        draw.line([(40, gy), (1040, gy)], fill=GRID_COLOR, width=1)
    for gx in range(40, 1060, 120):
        draw.line([(gx, 80), (gx, 1860)], fill=GRID_COLOR, width=1)

    # Top Section (Y: 100 to 360)
    # 1. Brand Tag
    tag_font = get_font(22, bold=True)
    brand_text = "THE WEALTH BLUEPRINT"
    draw.rounded_rectangle([340, 110, 740, 155], radius=22, fill=(10, 28, 22), outline=GREEN, width=2)
    t_bbox = tag_font.getbbox(brand_text)
    tx = 340 + (400 - (t_bbox[2] - t_bbox[0])) // 2
    ty = 110 + (45 - (t_bbox[3] - t_bbox[1])) // 2
    draw.text((tx, ty), brand_text, fill=GREEN, font=tag_font)

    # 2. Main Story Alert Hook
    alert_font = get_font(42, bold=True)
    alert_text = "NEW BLUEPRINT DROPPED"
    a_bbox = alert_font.getbbox(alert_text)
    ax = (1080 - (a_bbox[2] - a_bbox[0])) // 2
    draw.text((ax, 180), alert_text, fill=WHITE, font=alert_font)

    # 3. Clean Topic Line
    clean_title = "".join(c for c in title.split("#")[0] if ord(c) < 128).strip()
    if len(clean_title) > 42:
        clean_title = clean_title[:40] + "..."
    title_font = get_font(26, bold=False)
    ti_bbox = title_font.getbbox(clean_title)
    tix = (1080 - (ti_bbox[2] - ti_bbox[0])) // 2
    draw.text((tix, 245), clean_title, fill=GOLD, font=title_font)

    # Decorative Arrow pointing down to Reel
    draw.line([(540, 310), (540, 350)], fill=CYAN, width=4)
    draw.polygon([(526, 340), (554, 340), (540, 358)], fill=CYAN)

    # Bottom Section (Y: 1560 to 1820)
    # 4. Animated-style CTA Box (Where Instagram Reel tap hint is shown)
    draw.line([(540, 1555), (540, 1585)], fill=CYAN, width=4)
    draw.polygon([(526, 1565), (554, 1565), (540, 1550)], fill=CYAN)

    cta_box_y = 1600
    draw.rounded_rectangle([140, cta_box_y, 940, cta_box_y + 90], radius=24, fill=(18, 32, 25), outline=GREEN, width=3)
    cta_font = get_font(32, bold=True)
    cta_text = "TAP TO WATCH FULL REEL"
    c_bbox = cta_font.getbbox(cta_text)
    cx = 140 + (800 - (c_bbox[2] - c_bbox[0])) // 2
    cy = cta_box_y + (90 - (c_bbox[3] - c_bbox[1])) // 2
    draw.text((cx, cy), cta_text, fill=WHITE, font=cta_font)

    # Follow prompt
    sub_font = get_font(22, bold=False)
    sub_text = "FOLLOW @THEWEALTHBLUEPRINT10 FOR DAILY FINANCIAL WEAPONS"
    s_bbox = sub_font.getbbox(sub_text)
    sx = (1080 - (s_bbox[2] - s_bbox[0])) // 2
    draw.text((sx, 1720), sub_text, fill=MUTED, font=sub_font)

    img.save(out_path, "JPEG", quality=95)
    return out_path

if __name__ == "__main__":
    out = render_story_background("Perplexity AI: The Google Search Killer", "AI Wealth Engine", "test_story_bg.jpg")
    print(f"Test story background generated: {out}")
