import os
import sys
import json
import asyncio
import subprocess
import imageio_ffmpeg
import edge_tts
from audio_synth import generate_ambient_background_music

# Fix console encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BASE_DIR, "posts_15_days")
OUTPUT_VIDEOS_DIR = os.path.join(POSTS_DIR, "ready_videos")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BGM_PATH = os.path.join(ASSETS_DIR, "ambient_beat.wav")

os.makedirs(OUTPUT_VIDEOS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# 15 Days SEO Metadata Configurations
SEO_DATA = {
    1: {
        "title": "The 15/3 Credit Score Glitch Banks Keep Secret 💳📈 #Shorts #CreditHack",
        "category": "Credit & Banking",
        "hook": "Banks don't report your credit score on your due date...",
        "tags": ["credit score hack", "15 3 credit rule", "credit card glitch", "boost credit score fast", "personal finance", "wealth blueprint"]
    },
    2: {
        "title": "The Rule of 72: When Will Your Money Double? ⏳💰 #Investing #WealthShorts",
        "category": "Investing & Wealth",
        "hook": "The simple mental math formula billionaires use to double money...",
        "tags": ["rule of 72", "compound interest", "how to double money", "investing for beginners", "index funds", "sp500"]
    },
    3: {
        "title": "Buy, Borrow, Die: How Billionaires Pay 0% Tax 🛩️🏛️ #TaxLoopholes #Shorts",
        "category": "Tax Strategies",
        "hook": "Here is how the ultra-wealthy legally pay zero income tax...",
        "tags": ["buy borrow die", "tax loopholes", "how billionaires avoid tax", "wealth building", "asset protection", "tax strategies"]
    },
    4: {
        "title": "The 3-Bank-Account System That Builds Wealth on Autopilot 🏦💵 #Budgeting",
        "category": "Money Management",
        "hook": "Stop budgeting with willpower — let banking architecture do it for you...",
        "tags": ["3 account system", "automated savings", "checking vs savings", "financial freedom", "budgeting hacks", "money habits"]
    },
    5: {
        "title": "High-Yield Savings vs. Commercial Banks (Stop Losing Money) 🏦❌ #Banking",
        "category": "Banking",
        "hook": "Your regular bank is quietly paying you 0.01% while inflation steals 3%...",
        "tags": ["high yield savings account", "hysa explained", "bank hidden fees", "earn passive income", "smart money", "savings tips"]
    },
    6: {
        "title": "The Retention Script to Waive ANY Credit Card Annual Fee 📞💳 #CreditTips",
        "category": "Credit Hack",
        "hook": "Never pay a credit card annual fee again with this simple phone call...",
        "tags": ["credit card annual fee", "retention call script", "waive annual fee", "credit card rewards", "personal finance hacks"]
    },
    7: {
        "title": "The $700/Month Car Payment Trap Destroying Your Wealth 🚗📉 #DebtFree",
        "category": "Wealth Destroyer",
        "hook": "Financing a depreciating car is the number one middle-class wealth killer...",
        "tags": ["car payment trap", "depreciating assets", "investing vs car loan", "debt free community", "build wealth early"]
    },
    8: {
        "title": "The Roth IRA: The 100% Tax-Free Retirement Hack 🛡️📈 #Retirement #Investing",
        "category": "Tax Shield",
        "hook": "The government allows you to grow hundreds of thousands completely tax-free...",
        "tags": ["roth ira explained", "tax free investing", "compound growth", "retirement accounts", "investing in your 20s"]
    },
    9: {
        "title": "Stop Using Google: Perplexity AI Is The Future 🔍🤖 #Productivity #AI",
        "category": "AI Shortcut",
        "hook": "Google gives you 10 sponsored blue links, Perplexity gives you direct answers...",
        "tags": ["perplexity ai", "ai search engine", "google alternative", "ai productivity tools", "best ai apps 2026"]
    },
    10: {
        "title": "The Credit Card Chargeback Superpower (Forces Instant Refunds) 💳⚡ #ConsumerLaw",
        "category": "Consumer Protection",
        "hook": "The secret federal law that forces scam merchants to refund your money...",
        "tags": ["credit card chargeback", "fair credit billing act", "how to get refund", "consumer rights", "banking secrets"]
    },
    11: {
        "title": "Gamma AI: Create 15-Slide Decks in 15 Seconds 📊⚡ #PowerPointKiller #AI",
        "category": "AI Productivity",
        "hook": "Never spend hours aligning slide boxes in PowerPoint again...",
        "tags": ["gamma app", "ai presentation maker", "powerpoint alternatives", "ai tools for work", "productivity hacks"]
    },
    12: {
        "title": "Google NotebookLM: Turn Any 100-Page PDF Into a Podcast 🎙️📄 #AIHacks",
        "category": "AI Shortcut",
        "hook": "Upload any dense textbook or report and listen to it as a 2-person podcast...",
        "tags": ["notebooklm google", "pdf to podcast", "ai audio overview", "study hacks", "productivity tips"]
    },
    13: {
        "title": "The 5-Minute Debit Card Reset That Kills Zombie Subscriptions 💳❌ #MoneyHacks",
        "category": "Money Defense",
        "hook": "The easiest way to cancel all forgotten $10/mo subscriptions with zero phone calls...",
        "tags": ["cancel subscriptions", "stop wasting money", "bank card reset", "save 1000 a year", "smart money moves"]
    },
    14: {
        "title": "$10 a Day Compounds Into $680,000 (The Snowball Formula) ☕➡️💰 #Compounding",
        "category": "Investing Math",
        "hook": "Skipping two fancy coffees a day can build generational wealth over time...",
        "tags": ["10 dollars a day", "compound interest example", "start investing with little money", "index funds", "sp500 returns"]
    },
    15: {
        "title": "Assets vs. Liabilities: The Golden Rule of The Ultra-Wealthy ⚖️🏰 #RichDad",
        "category": "Core Foundation",
        "hook": "The fundamental difference separating the top 1% from the working class...",
        "tags": ["assets vs liabilities", "rich dad poor dad", "financial literacy", "cash flow assets", "wealth blueprint"]
    }
}

async def generate_voice(script_text: str, output_path: str, voice: str = "en-US-ChristopherNeural"):
    """Generates natural neural narration via Edge-TTS."""
    clean = script_text.replace("\n", " ").strip()
    communicate = edge_tts.Communicate(clean, voice)
    await communicate.save(output_path)
    return output_path

def build_single_video(day_num: int):
    """Assembles 1080x1920 video with voiceover, ambient ducked music, and metadata."""
    img_path = os.path.join(POSTS_DIR, f"day{day_num:02d}_render_day{day_num:02d}.png")
    txt_path = os.path.join(POSTS_DIR, f"day{day_num:02d}_script.txt")

    if not os.path.exists(img_path) or not os.path.exists(txt_path):
        print(f"   [!] Missing assets for Day {day_num:02d}")
        return None

    with open(txt_path, "r", encoding="utf-8") as f:
        script_text = f.read().strip()

    # 1. Voiceover
    voice_path = os.path.join(OUTPUT_VIDEOS_DIR, f"day{day_num:02d}_voice.mp3")
    asyncio.run(generate_voice(script_text, voice_path))

    # 2. FFmpeg Video Compositing
    output_mp4 = os.path.join(OUTPUT_VIDEOS_DIR, f"day{day_num:02d}_The_Wealth_Blueprint.mp4")
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
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"   [!] FFmpeg error on Day {day_num:02d}: {res.stderr}")
        return None

    # 3. SEO & Captions Package
    meta = SEO_DATA.get(day_num, {})
    title = meta.get("title", f"Day {day_num:02d} Financial Blueprint")
    tags = meta.get("tags", ["finance", "wealth", "money"])
    category = meta.get("category", "Personal Finance")

    yt_desc = f"""{title}

⚡ SCRIPT BREAKDOWN:
{script_text}

👇 GET OUR FREE 0% INTEREST CREDIT MASTERLIST & GUIDES:
Check the official link in our channel bio: @TheWealthBlueprint

📌 PINNED COMMENT TO ENGAGE AUDIENCE:
"Which step in this blueprint surprised you most? Comment below and we'll send you our 0% Interest Card Masterlist!"

#Shorts #{category.replace(' ', '')} #TheWealthBlueprint #PassiveIncome #FinancialFreedom"""

    ig_caption = f"""{title}

💡 THE BLUEPRINT BREAKDOWN:
{script_text}

📌 SAVE this post to refer back to when managing your money.
👉 Follow @TheWealthBlueprint for daily financial loopholes & wealth-building systems!

{" ".join(["#" + t.replace(" ", "") for t in tags])} #financialfreedom #personalfinance #wealthmindset #passiveincome #moneymoves"""

    seo_json_path = os.path.join(OUTPUT_VIDEOS_DIR, f"day{day_num:02d}_seo.json")
    with open(seo_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "day": day_num,
            "title": title,
            "category": category,
            "script": script_text,
            "tags": tags,
            "youtube_description": yt_desc,
            "instagram_caption": ig_caption,
            "video_path": output_mp4
        }, f, indent=2)

    caption_txt_path = os.path.join(OUTPUT_VIDEOS_DIR, f"day{day_num:02d}_caption.txt")
    with open(caption_txt_path, "w", encoding="utf-8") as f:
        f.write(f"=== YOUTUBE TITLE ===\n{title}\n\n=== YOUTUBE DESCRIPTION ===\n{yt_desc}\n\n=== INSTAGRAM CAPTION ===\n{ig_caption}\n")

    return output_mp4

def main():
    print(">> ========================================================")
    print(">> AUTOMATED 15-DAY VIDEO GENERATION ENGINE (FULL AUTOPILOT)")
    print(">> Generating Neural Voiceover + Ambient Music + 1080x1920 MP4s + SEO")
    print(">> ========================================================")

    if not os.path.exists(BGM_PATH):
        print(">> Synthesizing ambient background synth audio...")
        generate_ambient_background_music(BGM_PATH, 75.0)

    for day in range(1, 16):
        print(f">> Processing Day {day:02d}/15...")
        v_path = build_single_video(day)
        if v_path:
            sz_mb = os.path.getsize(v_path) / (1024 * 1024)
            print(f"   [OK] Generated: {os.path.basename(v_path)} ({sz_mb:.2f} MB)")

    print(">> ========================================================")
    print(f">> All 15 videos, neural voiceovers & SEO packages successfully generated in:")
    print(f">> {OUTPUT_VIDEOS_DIR}")
    print(">> ========================================================")

if __name__ == "__main__":
    main()
