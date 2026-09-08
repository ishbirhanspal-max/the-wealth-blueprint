import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

OUT_PFP = os.path.join(ASSETS_DIR, "youtube_profile_picture.jpg")
SRC_LOGO = os.path.join(ASSETS_DIR, "the_wealth_blueprint_logo.jpg")
SRC_AVATAR = os.path.join(ASSETS_DIR, "avatar.jpg")

SIZE = 800

def create_pfp():
    print(f">> Creating 800x800 YouTube Profile Picture with Circular Safe Margin...")
    img = Image.new("RGB", (SIZE, SIZE), color=(9, 11, 16))
    draw = ImageDraw.Draw(img)

    # 1. Outer subtle dark radial gradient/glow
    draw.ellipse([20, 20, SIZE - 20, SIZE - 20], fill=(16, 20, 30), outline=(255, 184, 0), width=6)
    draw.ellipse([28, 28, SIZE - 28, SIZE - 28], outline=(0, 242, 152), width=2)

    # 2. Load the source gold bull logo
    src_file = SRC_LOGO if os.path.exists(SRC_LOGO) else SRC_AVATAR
    if os.path.exists(src_file):
        try:
            logo = Image.open(src_file).convert("RGB")
            # Inner circle diameter = 680 to guarantee 100% circular crop safety
            inner_size = 680
            logo_resized = logo.resize((inner_size, inner_size), Image.Resampling.LANCZOS)

            # Circular mask for logo
            mask = Image.new("L", (inner_size, inner_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, inner_size, inner_size], fill=255)

            offset = (SIZE - inner_size) // 2
            img.paste(logo_resized, (offset, offset), mask)

            # Gold inner rim
            draw.ellipse([offset, offset, offset + inner_size, offset + inner_size], outline=(255, 184, 0), width=4)
        except Exception as e:
            print(f"[!] Logo processing note: {e}")

    img.save(OUT_PFP, "JPEG", quality=98)
    print(f">> Saved YouTube Profile Picture to: {OUT_PFP}")
    return OUT_PFP

if __name__ == "__main__":
    create_pfp()
