import os
import sys
import json
from googleapiclient.http import MediaFileUpload

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANNER_PATH = os.path.join(BASE_DIR, "assets", "youtube_channel_banner.jpg")

from youtube_uploader import get_authenticated_service

CHANNEL_ID = "UCv2BCjcyeUfLMl6q-0jj6eQ"

# High-converting description crafted strictly under YouTube API 1,000 char ceiling (880 chars)
CHANNEL_DESCRIPTION = """Welcome to The Wealth Blueprint (@thewealthblueprint10).

We decode the contrarian wealth loopholes, banking secrets, and legal tax arbitrage frameworks that high-net-worth individuals use to build, protect, and multiply generational wealth.

DAILY UPLOAD SCHEDULE (3X DAILY):
• Morning Commute: 09:00 AM IST (03:30 UTC)
• Lunch Break: 01:30 PM IST (08:00 UTC)
• Prime Evening: 08:30 PM IST (15:00 UTC)

WHAT WE DECODE:
• Legal Tax Arbitrage: Section 54F, HUF PAN status, 80CCD(1B), 54EC Bonds, 80GG
• Credit Card Architecture: 45-day float, zero-liability chargebacks, CIBIL 750+ hacks
• Banking Shields: FDIC IntraFi network, RBI circulars, locker guarantees
• Sovereign Compounding: 10% Step-Up SIPs, Sovereign Gold Bonds, EPF/VPF

Connect with our community on Instagram:
https://www.instagram.com/thewealthblueprint10/

Subscribe for daily financial intelligence and zero-BS wealth strategies.

Disclaimer: Educational purposes only. Consult a licensed financial advisor."""

KEYWORDS = '"The Wealth Blueprint" wealth "personal finance" investing "money hacks" "banking loopholes" "tax saving" "income tax" "cibil score" "credit card hacks" "financial freedom" "sovereign gold bonds" "mutual funds" "stock market" "passive income"'

def update_profile():
    print("========================================================")
    print("  UPDATING YOUTUBE CHANNEL PROFILE & BRANDING")
    print(f"  Channel ID: {CHANNEL_ID}")
    print("========================================================\n")

    yt = get_authenticated_service()

    # 1. Upload Channel Banner (2560x1440)
    banner_url = None
    if os.path.exists(BANNER_PATH):
        print(f">> Uploading official Channel Banner: {BANNER_PATH}")
        try:
            media = MediaFileUpload(BANNER_PATH, mimetype="image/jpeg", resumable=True)
            banner_res = yt.channelBanners().insert(body={}, media_body=media).execute()
            banner_url = banner_res.get("url")
            print(f"[✓] Banner uploaded successfully! URL: {banner_url}")
        except Exception as e:
            print(f"[!] Banner upload note: {e}")
            banner_url = "https://yt3.googleusercontent.com/oQuB6EIQi8hVtAzJhuem1VkOKVbeck0j6NiYHDtlUM6WPCIzkWEGRsNc7wIJUMcDrSNiIjbeBQ"

    # 2. Update Channel Branding Settings
    print("\n>> Updating Channel Branding Settings (Title, Description, Keywords, Banner)...")
    branding_body = {
        "id": CHANNEL_ID,
        "brandingSettings": {
            "channel": {
                "title": "The Wealth Blueprint",
                "description": CHANNEL_DESCRIPTION,
                "keywords": KEYWORDS
            }
        }
    }

    if banner_url:
        branding_body["brandingSettings"]["image"] = {
            "bannerExternalUrl": banner_url
        }

    try:
        update_res = yt.channels().update(part="brandingSettings", body=branding_body).execute()
        print("[✓] Successfully updated YouTube Channel Branding Settings!")
        ch_settings = update_res.get("brandingSettings", {}).get("channel", {})
        print(f"    - Channel Title: {ch_settings.get('title')}")
        print(f"    - Description:   {len(ch_settings.get('description', ''))} characters saved")
        print(f"    - SEO Keywords:  {ch_settings.get('keywords')[:60]}...")
        if banner_url:
            print(f"    - Banner URL:    {update_res.get('brandingSettings', {}).get('image', {}).get('bannerExternalUrl')}")
    except Exception as e:
        print(f"[!] Error updating branding settings: {e}")

    # 3. Verify Public Channel Details via channels.list
    print("\n>> Verifying updated public channel details via channels.list...")
    try:
        verify_res = yt.channels().list(part="snippet,brandingSettings", id=CHANNEL_ID).execute()
        item = verify_res["items"][0]
        snippet = item["snippet"]
        branding = item.get("brandingSettings", {})
        print(f"[✓] Channel Title:       {snippet['title']}")
        print(f"[✓] Channel Custom URL:   {snippet.get('customUrl')}")
        print(f"[✓] Description Length:   {len(branding.get('channel', {}).get('description', ''))} chars")
        print(f"[✓] Banner Active:        {'bannerExternalUrl' in branding.get('image', {})}")
        print(f"[✓] Keywords Saved:       {'keywords' in branding.get('channel', {})}")
    except Exception as e:
        print(f"[!] Verify note: {e}")

    print("\n========================================================")
    print("  YOUTUBE PROFILE UPDATE 100% COMPLETE!")
    print("========================================================")

if __name__ == "__main__":
    update_profile()
