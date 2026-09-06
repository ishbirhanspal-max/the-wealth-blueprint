import os
import re
import asyncio
from datetime import timedelta
import edge_tts

DEFAULT_VOICE = "en-US-ChristopherNeural"  # Deep, confident, authoritative

def clean_text_for_speech(text: str) -> str:
    """Removes emojis and special characters that could trip up TTS."""
    clean = re.sub(r"[^\w\s.,!?'$%-]", "", text)
    return clean.strip()

def format_ass_time(td: timedelta) -> str:
    """Formats timedelta to ASS time format: H:MM:SS.cs"""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    centiseconds = td.microseconds // 10000
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

async def generate_speech_and_subtitles(
    text: str,
    output_audio_path: str,
    output_ass_path: str,
    voice: str = DEFAULT_VOICE
) -> float:
    """
    Generates realistic neural voiceover and styled ASS subtitles.
    Returns audio duration in seconds.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(output_ass_path)), exist_ok=True)
    
    clean_text = clean_text_for_speech(text)
    communicate = edge_tts.Communicate(clean_text, voice)
    
    sub = edge_tts.SubMaker()
    audio_data = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] in ("SentenceBoundary", "WordBoundary"):
            sub.feed(chunk)
            
    with open(output_audio_path, "wb") as f:
        f.write(audio_data)
        
    # Build styled ASS subtitle file (Hormozi / Viral Shorts Style)
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralStyle,Arial,58,&H002EFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_lines = []
    for cue in sub.cues:
        start_str = format_ass_time(cue.start)
        end_str = format_ass_time(cue.end)
        
        # Break longer sentences into punchy chunks of max 4 words
        words = cue.content.strip().split()
        if not words:
            continue
            
        chunk_size = 4
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        total_duration = (cue.end - cue.start).total_seconds()
        chunk_duration = total_duration / len(chunks) if chunks else total_duration
        
        for idx, ch in enumerate(chunks):
            ch_start = cue.start + timedelta(seconds=idx * chunk_duration)
            ch_end = cue.start + timedelta(seconds=(idx + 1) * chunk_duration)
            phrase = " ".join(ch).upper()
            
            # Highlight first word or key word in bright yellow
            styled_phrase = f"\\c&H002EFFFF\\{phrase}"
            line = f"Dialogue: 0,{format_ass_time(ch_start)},{format_ass_time(ch_end)},ViralStyle,,0,0,0,,{{\\b1}}{styled_phrase}"
            ass_lines.append(line)
            
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(ass_lines) + "\n")
        
    # Calculate duration
    duration = sub.cues[-1].end.total_seconds() if sub.cues else 15.0
    return duration

def create_voice(text: str, audio_path: str, ass_path: str, voice: str = DEFAULT_VOICE) -> float:
    """Synchronous wrapper for generate_speech_and_subtitles."""
    return asyncio.run(generate_speech_and_subtitles(text, audio_path, ass_path, voice))

if __name__ == "__main__":
    dur = create_voice(
        "If you pay your credit card bill on the due date, you are quietly hurting your credit score.",
        "assets/test.mp3",
        "assets/test.ass"
    )
    print(f"Generated {dur:.2f}s audio and subtitles successfully.")
