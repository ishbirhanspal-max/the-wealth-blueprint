import os
import sys
import json
import argparse

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from generator import generate_script
from voice import create_voice
from audio_synth import generate_ambient_background_music
from media import get_broll_clips
from composer import compose_video

def run_pipeline(
    niche: str = "finance",
    voice: str = "en-US-ChristopherNeural",
    upload_youtube: bool = False,
    output_path: str = None
) -> dict:
    """Executes the complete 100% automated Short/Reel creation lifecycle."""
    print("=" * 60)
    print(">> [1/5] STARTING AUTOMATED SHORT GENERATION PIPELINE")
    print("=" * 60)
    
    # 1. Generate Script
    gemini_key = os.environ.get("GEMINI_API_KEY")
    script = generate_script(niche=niche, api_key=gemini_key)
    print(f">> Title: {script['title']}")
    print(f">> Narration: {script['voiceover_text'][:80]}...")
    
    # Set paths
    work_dir = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.join(work_dir, "assets")
    output_dir = os.path.join(work_dir, "output")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    audio_path = os.path.join(assets_dir, "current_voice.mp3")
    sub_path = os.path.join(assets_dir, "current_sub.ass")
    bg_music_path = os.path.join(assets_dir, "current_bg.wav")
    clips_dir = os.path.join(assets_dir, "video_clips")
    
    if not output_path:
        output_path = os.path.join(output_dir, "latest_short.mp4")
        
    # 2. Generate Voiceover & Timed Dynamic Subtitles
    print("\n>> [2/5] Synthesizing Neural Human Speech & Styled Subtitles...")
    duration = create_voice(script["voiceover_text"], audio_path, sub_path, voice=voice)
    print(f"[OK] Voiceover generated: {duration:.2f} seconds")
    
    # 3. Generate Ambient Background Music
    print("\n>> [3/5] Generating Ambient Background Music...")
    generate_ambient_background_music(bg_music_path, duration + 4.0)
    print("[OK] Background music ready.")
    
    # 4. Fetch / Render 9:16 Visual B-Roll Clips
    print("\n>> [4/5] Preparing 9:16 Vertical Visual B-Roll...")
    pexels_key = os.environ.get("PEXELS_API_KEY")
    clips = get_broll_clips(script.get("search_keywords", ["finance", "tech"]), duration, clips_dir, pexels_key=pexels_key)
    print(f"[OK] {len(clips)} dynamic b-roll scenes ready.")
    
    # 5. Composite Final Video & Burn Subtitles
    print("\n>> [5/5] Compositing 1080x1920 Video & Burning Kinetic Captions...")
    compose_video(clips, audio_path, bg_music_path, sub_path, output_path, duration)
    print(f"[SUCCESS] FINAL VIDEO READY: {output_path}")
    
    # Save video metadata for publishing
    meta_path = os.path.join(output_dir, "latest_metadata.json")
    meta_data = {
        "video_path": output_path,
        "title": script["title"],
        "description": script["description"],
        "pinned_comment": script["pinned_comment"],
        "duration": duration,
        "niche": niche
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2)
        
    # 6. Auto-upload if requested
    if upload_youtube:
        try:
            from youtube_uploader import upload_short_to_youtube
            url = upload_short_to_youtube(
                video_path=output_path,
                title=script["title"],
                description=script["description"],
                pinned_comment=script["pinned_comment"]
            )
            meta_data["youtube_url"] = url
        except Exception as e:
            print(f"[Warning] Auto-upload skipped: {e}")
            
    return meta_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Faceless Video Generator")
    parser.add_argument("--niche", default="finance", choices=["finance", "tech_ai"], help="Content niche")
    parser.add_argument("--voice", default="en-US-ChristopherNeural", help="Edge-TTS voice")
    parser.add_argument("--upload", action="store_true", help="Auto-upload to YouTube")
    parser.add_argument("--output", default=None, help="Custom output MP4 path")
    args = parser.parse_args()
    
    result = run_pipeline(niche=args.niche, voice=args.voice, upload_youtube=args.upload, output_path=args.output)
    print("\nDone! Video metadata:", json.dumps(result, indent=2))
