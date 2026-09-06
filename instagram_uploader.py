import os
import sys
import json
import time
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def upload_reel_graph_api(video_url: str, caption: str, access_token: str, ig_user_id: str) -> str:
    """
    Uploads a Reel using Meta's Official Instagram Graph API.
    Requirements: Instagram Professional/Creator account linked to a Facebook Page.
    """
    print(f">> [Instagram] Creating Reel media container...")
    
    # Step 1: Create media container
    container_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": True,
        "access_token": access_token
    }
    
    res = requests.post(container_url, data=payload)
    data = res.json()
    if "id" not in data:
        raise RuntimeError(f"Failed to create Instagram container: {data}")
        
    container_id = data["id"]
    print(f"   Container created: {container_id}. Waiting for video processing...")
    
    # Step 2: Poll status until READY
    status_url = f"https://graph.facebook.com/v19.0/{container_id}?fields=status_code&access_token={access_token}"
    for _ in range(30):
        time.sleep(5)
        status_res = requests.get(status_url).json()
        status_code = status_res.get("status_code")
        print(f"   Status: {status_code}...")
        if status_code == "FINISHED":
            break
        elif status_code == "ERROR":
            raise RuntimeError(f"Instagram video processing error: {status_res}")
            
    # Step 3: Publish container
    publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
    pub_res = requests.post(publish_url, data={"creation_id": container_id, "access_token": access_token})
    pub_data = pub_res.json()
    
    if "id" in pub_data:
        post_id = pub_data["id"]
        print(f">> [Instagram] Reel published successfully! Post ID: {post_id}")
        return f"https://instagram.com/p/{post_id}"
    else:
        raise RuntimeError(f"Failed to publish Instagram Reel: {pub_data}")

def upload_reel_direct(video_path: str, caption: str, username: str, password: str) -> str:
    """
    Direct upload using instagrapi (does not require a Meta developer app).
    """
    try:
        from instagrapi import Client
        cl = Client()
        session_file = os.path.join(os.path.dirname(__file__), "ig_session.json")
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            
        print(f">> [Instagram] Logging in as @{username}...")
        cl.login(username, password)
        cl.dump_settings(session_file)
        
        print(f">> [Instagram] Uploading Reel: {os.path.basename(video_path)}...")
        media = cl.clip_upload(video_path, caption=caption)
        reel_url = f"https://www.instagram.com/reel/{media.code}/"
        print(f">> [Instagram] Published successfully! URL: {reel_url}")
        return reel_url
    except ImportError:
        print("[Notice] 'instagrapi' not installed. Run: pip install instagrapi")
        return None
    except Exception as e:
        print(f"[Warning] Direct Instagram upload failed: {e}")
        return None

def publish_to_instagram(video_path: str, caption: str, hashtags: str = "") -> str:
    """
    Universal Instagram publisher: checks for Graph API tokens or direct credentials.
    """
    full_caption = f"{caption}\n\n.\n.\n.\n{hashtags}"
    
    # 1. Check Official Graph API
    ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    ig_user_id = os.environ.get("INSTAGRAM_USER_ID")
    public_video_url = os.environ.get("PUBLIC_VIDEO_URL")
    
    if ig_token and ig_user_id and public_video_url:
        return upload_reel_graph_api(public_video_url, full_caption, ig_token, ig_user_id)
        
    # 2. Check Direct Credentials
    ig_user = os.environ.get("INSTAGRAM_USERNAME")
    ig_pass = os.environ.get("INSTAGRAM_PASSWORD")
    if ig_user and ig_pass:
        return upload_reel_direct(video_path, full_caption, ig_user, ig_pass)
        
    print("[Notice] Instagram credentials not configured. Skipping Instagram upload.")
    print("         (Saved complete Instagram caption and hashtags in processed_videos/ JSON!)")
    return None

if __name__ == "__main__":
    print("Instagram Uploader module ready. Configure credentials in environment or .env file.")
