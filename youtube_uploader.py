import os
import sys
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def get_authenticated_service(client_secrets_file="client_secret.json", token_file="token.json"):
    """Handles YouTube Data API v3 OAuth authentication."""
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists(client_secrets_file):
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_file, "w") as token:
                token.write(creds.to_json())
        else:
            raise FileNotFoundError(f"Missing {client_secrets_file}. Download OAuth client credentials from Google Cloud Console.")
            
    return build("youtube", "v3", credentials=creds)

def upload_short_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    pinned_comment: str = None,
    privacy_status: str = "public",
    publish_at: str = None
):
    """
    Uploads 9:16 video to YouTube as a #Shorts and auto-pins affiliate comment.
    If publish_at is provided (ISO 8601 string, e.g. 2026-09-07T06:30:00Z), 
    the video is uploaded as Scheduled.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    youtube = get_authenticated_service()
    
    # Ensure #Shorts tag is in title for algorithmic categorization
    if "#Shorts" not in title and "#shorts" not in title:
        title = f"{title} #Shorts"
        
    status_dict = {
        "privacyStatus": "private" if publish_at else privacy_status,
        "selfDeclaredMadeForKids": False
    }
    if publish_at:
        status_dict["publishAt"] = publish_at
        
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags or ["shorts", "finance", "money", "sidehustle"],
            "categoryId": "27" # Education
        },
        "status": status_dict
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    print(f"[YouTube] Uploading '{title}'...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")
            
    video_id = response.get("id")
    video_url = f"https://youtube.com/shorts/{video_id}"
    print(f"[YouTube] Successfully published! URL: {video_url}")
    
    # Auto-pin first comment with affiliate links
    if pinned_comment and video_id:
        try:
            comment_body = {
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": pinned_comment
                        }
                    }
                }
            }
            comment_res = youtube.commentThreads().insert(part="snippet", body=comment_body).execute()
            print("[YouTube] Pinned comment posted successfully.")
        except Exception as e:
            print(f"[YouTube] Note: Could not pin comment: {e}")
            
    return video_url

if __name__ == "__main__":
    print("YouTube Uploader module loaded. Set up client_secret.json to authenticate.")
