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

def render_story_background(title: str, category: str, out_path: str, scale: int = 2):
    """Renders a 4K Ultra HD (2160x3840) luxury Story background tailored for instagrapi media_share_to_story."""
    width = 1080 * scale
    height = 1920 * scale
    img = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Subtle background tech grid
    for gy in range(80 * scale, 1860 * scale, 120 * scale):
        draw.line([(40 * scale, gy), (1040 * scale, gy)], fill=GRID_COLOR, width=1 * scale)
    for gx in range(40 * scale, 1060 * scale, 120 * scale):
        draw.line([(gx, 80 * scale), (gx, 1860 * scale)], fill=GRID_COLOR, width=1 * scale)

    # Top Section (Y: 100 to 360)
    # 1. Brand Tag
    tag_font = get_font(22 * scale, bold=True)
    brand_text = "THE WEALTH BLUEPRINT"
    draw.rounded_rectangle([340 * scale, 110 * scale, 740 * scale, 155 * scale], radius=22 * scale, fill=(10, 28, 22), outline=GREEN, width=2 * scale)
    t_bbox = tag_font.getbbox(brand_text)
    tx = 340 * scale + (400 * scale - (t_bbox[2] - t_bbox[0])) // 2
    ty = 110 * scale + (45 * scale - (t_bbox[3] - t_bbox[1])) // 2
    draw.text((tx, ty), brand_text, fill=GREEN, font=tag_font)

    # 2. Main Story Alert Hook
    alert_font = get_font(42 * scale, bold=True)
    alert_text = "NEW BLUEPRINT DROPPED"
    a_bbox = alert_font.getbbox(alert_text)
    ax = (width - (a_bbox[2] - a_bbox[0])) // 2
    draw.text((ax, 180 * scale), alert_text, fill=WHITE, font=alert_font)

    # 3. Clean Topic Line
    clean_title = "".join(c for c in title.split("#")[0] if ord(c) < 128).strip()
    if len(clean_title) > 42:
        clean_title = clean_title[:40] + "..."
    title_font = get_font(26 * scale, bold=False)
    ti_bbox = title_font.getbbox(clean_title)
    tix = (width - (ti_bbox[2] - ti_bbox[0])) // 2
    draw.text((tix, 245 * scale), clean_title, fill=GOLD, font=title_font)

    # Decorative Arrow pointing down to Reel
    arrow_x = 540 * scale
    draw.line([(arrow_x, 310 * scale), (arrow_x, 350 * scale)], fill=CYAN, width=4 * scale)
    draw.polygon([(arrow_x - 14 * scale, 340 * scale), (arrow_x + 14 * scale, 340 * scale), (arrow_x, 358 * scale)], fill=CYAN)

    # Bottom Section (Y: 1560 to 1820)
    # 4. Animated-style CTA Box (Where Instagram Reel tap hint is shown)
    draw.line([(arrow_x, 1555 * scale), (arrow_x, 1585 * scale)], fill=CYAN, width=4 * scale)
    draw.polygon([(arrow_x - 14 * scale, 1565 * scale), (arrow_x + 14 * scale, 1565 * scale), (arrow_x, 1550 * scale)], fill=CYAN)

    cta_box_y = 1600 * scale
    draw.rounded_rectangle([140 * scale, cta_box_y, 940 * scale, cta_box_y + 90 * scale], radius=24 * scale, fill=(18, 32, 25), outline=GREEN, width=3 * scale)
    cta_font = get_font(32 * scale, bold=True)
    cta_text = "TAP TO WATCH FULL REEL"
    c_bbox = cta_font.getbbox(cta_text)
    cx = 140 * scale + (800 * scale - (c_bbox[2] - c_bbox[0])) // 2
    cy = cta_box_y + (90 * scale - (c_bbox[3] - c_bbox[1])) // 2
    draw.text((cx, cy), cta_text, fill=WHITE, font=cta_font)

    # Follow prompt
    sub_font = get_font(22 * scale, bold=False)
    sub_text = "FOLLOW @THEWEALTHBLUEPRINT10 FOR DAILY FINANCIAL WEAPONS"
    s_bbox = sub_font.getbbox(sub_text)
    sx = (width - (s_bbox[2] - s_bbox[0])) // 2
    draw.text((sx, 1720 * scale), sub_text, fill=MUTED, font=sub_font)

    img.save(out_path, "JPEG", quality=95)
    return out_path

if __name__ == "__main__":
    out = render_story_background("Perplexity AI: The Google Search Killer", "AI Wealth Engine", "test_story_bg.jpg")
    print(f"Test story background generated: {out}")
