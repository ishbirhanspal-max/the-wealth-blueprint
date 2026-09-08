import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(BASE_DIR, "meta_bulk_upload_package")

from infinite_content_engine import load_dynamic_catalog

catalog = load_dynamic_catalog()
cat_by_id = {item["id"]: item for item in catalog}

REEL_IDS = list(range(8, 23)) # 8 to 22 (15 reels)

captions_sheet = []
js_captions_map = []

captions_sheet.append("=" * 70)
captions_sheet.append("THE WEALTH BLUEPRINT - ALL 15 REEL CAPTIONS (ONE SINGLE SHEET)")
captions_sheet.append("No need to open 15 separate files! Everything is in order below.")
captions_sheet.append("=" * 70 + "\n")

for p_id in REEL_IDS:
    item = cat_by_id.get(p_id)
    if not item:
        continue

    # Clean, high-converting, punchy caption
    title = item["title"]
    sub = item["sub"]
    c1 = item["c1_t"]
    c2 = item["c2_t"]
    c3 = item["c3_t"]

    clean_cap = f"""{title}

{sub}

THE TRAP: {c1}
THE BLUEPRINT: {c2}
THE PAYOFF: {c3}

Follow @thewealthblueprint10 for daily wealth loopholes!
Save this reel so you never lose it.

#wealth #personalfinance #moneyhacks #investing #smartmoney #financialfreedom #reelsindia"""

    captions_sheet.append(f"--- REEL {p_id:02d}: {title} ---")
    captions_sheet.append(clean_cap)
    captions_sheet.append("\n" + "=" * 70 + "\n")

    # Escaped for JS
    js_escaped = clean_cap.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    js_captions_map.append(f"  {json.dumps(title[:25])}: `{js_escaped}`")

# 1. Write 01_ALL_CAPTIONS_ONE_SHEET.txt
out_sheet = os.path.join(PACKAGE_DIR, "01_ALL_CAPTIONS_ONE_SHEET.txt")
with open(out_sheet, "w", encoding="utf-8") as f:
    f.write("\n".join(captions_sheet))

print(f"[OK] Generated: {out_sheet}")

# 2. Write 02_AUTO_FILL_SNIPPET.js
js_code = f"""// ============================================================
// META BUSINESS SUITE 1-CLICK CAPTION AUTO-FILLER
// 1. Open DevTools on Meta Business Suite (Press F12 -> Console)
// 2. Paste this entire snippet and press Enter!
// ============================================================
(function() {{
    const captions = [
{",\n".join([f"        `{item['title']}\\n\\n{item['sub']}\\n\\nFollow @thewealthblueprint10 for daily wealth loopholes!\\n\\n#wealth #finance #moneyhacks #investing #smartmoney`" for item in [cat_by_id[i] for i in REEL_IDS if i in cat_by_id]])}
    ];

    // Find all caption inputs or contenteditable containers in Meta Bulk Upload table
    const inputs = document.querySelectorAll('div[contenteditable="true"], textarea[placeholder*="caption" i], textarea[aria-label*="caption" i], textarea');
    let filled = 0;

    inputs.forEach((input, index) => {{
        if (index < captions.length) {{
            const cap = captions[index];
            if (input.tagName.toLowerCase() === 'textarea') {{
                input.value = cap;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else {{
                input.focus();
                input.innerText = cap;
                input.dispatchEvent(new InputEvent('input', {{ bubbles: true, inputType: 'insertText' }}));
            }}
            filled++;
        }}
    }});

    console.log(`[The Wealth Blueprint] Successfully auto-filled ${{filled}} reel captions!`);
    alert(`Successfully auto-filled ${{filled}} reel captions! Now select schedule times and click Schedule.`);
}})();
"""

out_js = os.path.join(PACKAGE_DIR, "02_AUTO_FILL_SNIPPET.js")
with open(out_js, "w", encoding="utf-8") as f:
    f.write(js_code)

print(f"[OK] Generated: {out_js}")
