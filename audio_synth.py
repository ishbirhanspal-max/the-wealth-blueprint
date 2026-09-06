import os
import numpy as np
from scipy.io import wavfile

def generate_ambient_background_music(output_path: str, duration: float = 60.0, sample_rate: int = 44100):
    """
    Synthesizes a punchy, high-retention dark wealth beat:
    - Deep punchy 808 bass glides
    - Sleek minor-key luxury chord swells (Dm9 -> Bbmaj7 -> Gm7 -> A7)
    - Rhythmic trap/phonk percussion (kick, snare, and rolling hi-hats)
    - Mastered with high dynamic energy for YouTube Shorts and Instagram Reels.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    bpm = 124.0 # High-energy viral tempo
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * 4.0
    
    # 1. Harmonic Chords (Dark Wealth & Finance Progression)
    chord_prog = [
        [146.83, 174.61, 220.00, 261.63, 329.63], # Dm9
        [116.54, 146.83, 174.61, 220.00, 261.63], # Bbmaj7
        [98.00,  116.54, 146.83, 174.61, 220.00], # Gm7
        [110.00, 138.59, 164.81, 220.00, 277.18]  # A7
    ]
    
    music = np.zeros(num_samples)
    bass = np.zeros(num_samples)
    
    # Generate Chord Swells & Sub-Bass
    num_bars = int(np.ceil(duration / bar_sec))
    for bar_i in range(num_bars):
        chord = chord_prog[bar_i % len(chord_prog)]
        bar_start = int(bar_i * bar_sec * sample_rate)
        bar_end = min(int((bar_i + 1) * bar_sec * sample_rate), num_samples)
        if bar_start >= num_samples:
            break
            
        tb = t[bar_start:bar_end] - (bar_i * bar_sec)
        # Rhythmic pulsing sidechain envelope (pumps on every beat)
        beat_phase = (tb % beat_sec) / beat_sec
        pulse_env = 0.5 + 0.5 * np.sin(np.pi * beat_phase)
        
        # Chord voices
        chord_wave = np.zeros(len(tb))
        for freq in chord:
            chord_wave += 0.25 * np.sin(2 * np.pi * freq * tb)
            chord_wave += 0.12 * np.sin(2 * np.pi * (freq * 2.003) * tb) # Shimmer octave
            chord_wave += 0.08 * np.sin(2 * np.pi * (freq * 0.997) * tb) # Chorus detune
            
        music[bar_start:bar_end] += chord_wave * pulse_env * 0.6
        
        # 808 Sub-Bass Note
        root_freq = chord[0] / 2.0 # 808 register (49Hz - 73Hz)
        bass_wave = np.sin(2 * np.pi * root_freq * tb)
        # Add subtle saturation / harmonic warmth
        bass_wave = np.tanh(bass_wave * 1.6)
        bass[bar_start:bar_end] += bass_wave * 0.75
        
    # 2. Rhythmic Percussion (Punchy Kick, Snare & Hi-Hats)
    drums = np.zeros(num_samples)
    total_beats = int(np.ceil(duration / beat_sec))
    
    for beat_i in range(total_beats):
        beat_time = beat_i * beat_sec
        beat_sample = int(beat_time * sample_rate)
        beat_in_bar = beat_i % 4
        
        # --- A. Punchy 808 Kick on Beat 1 and Beat 2.5 ---
        if beat_in_bar in [0, 2]:
            kick_dur = 0.32
            k_len = min(int(kick_dur * sample_rate), num_samples - beat_sample)
            if k_len > 0:
                tk = np.linspace(0, kick_dur, k_len)
                # Rapid pitch drop: 160Hz -> 48Hz
                k_freq = 48.0 + 112.0 * np.exp(-tk * 28.0)
                phase = 2 * np.pi * np.cumsum(k_freq) / sample_rate
                k_env = np.exp(-tk * 9.0)
                kick = np.sin(phase) * k_env * 0.9
                drums[beat_sample:beat_sample + k_len] += kick
                
        # --- B. Snare / Trap Clap on Beat 2 and Beat 4 ---
        if beat_in_bar in [1, 3]:
            snare_dur = 0.22
            s_len = min(int(snare_dur * sample_rate), num_samples - beat_sample)
            if s_len > 0:
                ts = np.linspace(0, snare_dur, s_len)
                # Noise burst + tone body
                noise = np.random.uniform(-1, 1, s_len) * np.exp(-ts * 22.0)
                body = np.sin(2 * np.pi * 210.0 * ts) * np.exp(-ts * 30.0)
                snare = (noise * 0.75 + body * 0.4) * 0.7
                drums[beat_sample:beat_sample + s_len] += snare
                
        # --- C. Rolling 8th/16th Hi-Hats ---
        hat_steps = 4 # 16th notes
        sub_sec = beat_sec / hat_steps
        for h in range(hat_steps):
            h_time = beat_time + (h * sub_sec)
            h_sample = int(h_time * sample_rate)
            if h_sample < num_samples:
                hat_dur = 0.05
                h_len = min(int(hat_dur * sample_rate), num_samples - h_sample)
                if h_len > 0:
                    th = np.linspace(0, hat_dur, h_len)
                    # High-frequency bandpass noise
                    hat = np.random.uniform(-1, 1, h_len) * np.exp(-th * 85.0)
                    hat_vol = 0.35 if (h % 2 == 0) else 0.20 # Velocity groove
                    drums[h_sample:h_sample + h_len] += hat * hat_vol

    # Mix Full Stems
    full_track = (music * 0.45) + (bass * 0.65) + (drums * 0.70)
    
    # High-impact master normalization to 0.85
    peak = np.max(np.abs(full_track))
    if peak > 0:
        full_track = (full_track / peak) * 0.85
        
    int_audio = (full_track * 32767).astype(np.int16)
    wavfile.write(output_path, sample_rate, int_audio)
    print(f">> [Audio Engine] Synthesized punchy wealth beat ({duration:.1f}s) -> {output_path}")
    return output_path

if __name__ == "__main__":
    out = generate_ambient_background_music("assets/ambient_beat.wav", 60.0)
    print("Synthesized new punchy wealth beat successfully.")
