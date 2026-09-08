import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

OUT_BANNER = os.path.join(ASSETS_DIR, "youtube_channel_banner.jpg")
LOGO_PATH = os.path.join(ASSETS_DIR, "the_wealth_blueprint_logo.jpg")

# Dimensions for official YouTube Channel Banner
W, H = 2560, 1440

# Colors
BG_DARK = (9, 11, 16)
CARD_BG = (16, 20, 30)
GOLD = (255, 184, 0)
GREEN = (0, 242, 152)
CYAN = (0, 212, 255)
WHITE = (248, 250, 252)
MUTED = (160, 168, 185)
GRID_COLOR = (18, 24, 36)

def get_font(size: int, bold: bool = False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "seguiemj.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def create_banner():
    print(f">> Generating YouTube Channel Banner ({W}x{H})...")
    img = Image.new("RGB", (W, H), color=BG_DARK)
    draw = ImageDraw.Draw(img)

    # 1. Subtle luxury geometric grid
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=GRID_COLOR, width=1)
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=GRID_COLOR, width=1)

    # 2. Subtle ambient gradient / glow in safe zone
    # Safe zone on 2560x1440 is X: 507 to 2053, Y: 508 to 931 (Center box 1546 x 423)
    safe_x1, safe_y1 = 507, 508
    safe_x2, safe_y2 = 2053, 931

    # Ambient glow box behind text
    draw.rounded_rectangle([safe_x1 - 20, safe_y1 - 10, safe_x2 + 20, safe_y2 + 10], radius=30, fill=(14, 18, 28), outline=(32, 40, 60), width=2)

    # Gold accent line top & bottom of safe box
    draw.line([(safe_x1 + 40, safe_y1 - 10), (safe_x2 - 40, safe_y1 - 10)], fill=GOLD, width=3)
    draw.line([(safe_x1 + 40, safe_y2 + 10), (safe_x2 - 40, safe_y2 + 10)], fill=GREEN, width=3)

    # 3. Insert Gold Bull Logo on Left side of safe zone
    logo_size = 320
    logo_x = safe_x1 + 60
    logo_y = safe_y1 + (423 - logo_size) // 2

    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image.open(LOGO_PATH).convert("RGBA").resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            # Create rounded mask
            mask = Image.new("L", (logo_size, logo_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle([0, 0, logo_size, logo_size], radius=36, fill=255)
            img.paste(logo_img, (logo_x, logo_y), mask)
            # Border around logo
            draw.rounded_rectangle([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], radius=36, outline=GOLD, width=3)
        except Exception as e:
            print(f"[!] Logo paste note: {e}")

    # 4. Text Content in Safe Zone
    text_start_x = logo_x + logo_size + 60

    # Top Brand Pill
    pill_f = get_font(24, bold=True)
    pill_text = "OFFICIAL FINANCIAL INTELLIGENCE"
    draw.rounded_rectangle([text_start_x, safe_y1 + 35, text_start_x + 460, safe_y1 + 75], radius=20, fill=(12, 32, 24), outline=GREEN, width=2)
    draw.text((text_start_x + 30, safe_y1 + 43), pill_text, fill=GREEN, font=pill_f)

    # Main Channel Name
    title_f = get_font(72, bold=True)
    title_text = "THE WEALTH BLUEPRINT"
    draw.text((text_start_x, safe_y1 + 95), title_text, fill=WHITE, font=title_f)
    # Metallic gold shadow/accent
    draw.text((text_start_x + 2, safe_y1 + 97), title_text, fill=GOLD, font=title_f)
    draw.text((text_start_x, safe_y1 + 95), title_text, fill=WHITE, font=title_f)

    # Subtitle Hooks
    sub_f = get_font(28, bold=True)
    sub_text = "CONTRARIAN WEALTH LOOPHOLES  •  BANKING SECRETS  •  TAX ARBITRAGE"
    draw.text((text_start_x, safe_y1 + 195), sub_text, fill=CYAN, font=sub_f)

    # Cadence & Schedule Badge
    cad_f = get_font(24, bold=True)
    cad_text = "NEW BLUEPRINTS 3X DAILY: 9:00 AM  •  1:30 PM  •  8:30 PM IST"
    draw.rounded_rectangle([text_start_x, safe_y1 + 250, text_start_x + 840, safe_y1 + 295], radius=15, fill=(35, 28, 12), outline=GOLD, width=2)
    draw.text((text_start_x + 25, safe_y1 + 259), cad_text, fill=GOLD, font=cad_f)

    # Bottom Social Link & Call To Action
    foot_f = get_font(22, bold=False)
    foot_text = "INSTAGRAM: @thewealthblueprint10   |   SUBSCRIBE FOR ZERO-BS WEALTH STRATEGIES"
    draw.text((text_start_x + 5, safe_y1 + 325), foot_text, fill=MUTED, font=foot_f)

    img.save(OUT_BANNER, "JPEG", quality=95)
    print(f"[✓] Successfully generated YouTube Channel Banner: {OUT_BANNER}")
    return OUT_BANNER

if __name__ == "__main__":
    create_banner()
