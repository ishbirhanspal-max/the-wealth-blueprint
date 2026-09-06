import os
import subprocess
import imageio_ffmpeg

def compose_video(
    clip_paths: list,
    voice_audio_path: str,
    bg_music_path: str,
    ass_subtitle_path: str,
    output_mp4_path: str,
    duration: float
) -> str:
    """
    Concatenates visual b-roll clips, loops ambient background music,
    mixes ducked voiceover, burns dynamic kinetic ASS subtitles, and
    exports a polished 1080x1920 MP4 for YouTube Shorts / Reels.
    """
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(os.path.dirname(os.path.abspath(output_mp4_path)), exist_ok=True)
    
    # 1. Create concat list for video clips
    concat_file = os.path.abspath(os.path.join(os.path.dirname(output_mp4_path), "concat_list.txt"))
    with open(concat_file, "w", encoding="utf-8") as f:
        for p in clip_paths:
            # Use forward slashes for FFmpeg compatibility
            norm_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{norm_p}'\n")
            
    # Format paths with forward slashes
    norm_ass = os.path.abspath(ass_subtitle_path).replace("\\", "/")
    # If drive letter colon exists (e.g. C:/...), escape as C\\:/ for subtitles filter
    if ":" in norm_ass:
        drive, rest = norm_ass.split(":", 1)
        escaped_ass = f"{drive}\\:{rest}"
    else:
        escaped_ass = norm_ass

    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file.replace("\\", "/"),
        "-i", os.path.abspath(voice_audio_path).replace("\\", "/"),
        "-stream_loop", "-1", "-i", os.path.abspath(bg_music_path).replace("\\", "/"),
        "-filter_complex",
        f"[0:v]subtitles='{escaped_ass}'[v_sub];"
        f"[1:a]volume=1.1[v_voice];"
        f"[2:a]volume=0.18[v_bgm];"
        f"[v_voice][v_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_out]",
        "-map", "[v_sub]",
        "-map", "[a_out]",
        "-t", f"{duration:.2f}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg compositing failed:\n{res.stderr}")
        
    if os.path.exists(concat_file):
        os.remove(concat_file)
        
    return output_mp4_path

if __name__ == "__main__":
    from audio_synth import generate_ambient_background_music
    from voice import create_voice
    from media import get_broll_clips
    
    sample_text = "Most people have no idea how long it takes to double their money. Billionaires use one simple mental math rule called the Rule of 72."
    dur = create_voice(sample_text, "assets/sample_voice.mp3", "assets/sample_sub.ass")
    bg = generate_ambient_background_music("assets/sample_bg.wav", dur + 5.0)
    clips = get_broll_clips(["finance", "luxury"], dur, "assets/sample_clips")
    
    out = compose_video(clips, "assets/sample_voice.mp3", bg, "assets/sample_sub.ass", "output/sample_short.mp4", dur)
    print("Video rendered successfully:", out)
