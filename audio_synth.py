import os
import numpy as np
from scipy.io import wavfile

def generate_ambient_background_music(output_path: str, duration: float = 45.0, sample_rate: int = 44100):
    """
    Generates a dark, sleek ambient synth track with deep sub-bass and 
    tape-warmth chords, ideal for high-retention wealth/tech shorts.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # Chord frequencies: Dm (D3, F3, A3, C4) -> Bb (Bb2, D3, F3, A3)
    chords = [
        [146.83, 174.61, 220.00, 261.63], # Dm7
        [116.54, 146.83, 174.61, 220.00], # Bbmaj7
        [130.81, 164.81, 196.00, 246.94], # C7
        [110.00, 130.81, 164.81, 196.00]  # Am7
    ]
    chord_len = 4.0 # 4 seconds per chord
    
    music = np.zeros_like(t)
    
    for i, chord in enumerate(chords * int(duration / (chord_len * len(chords)) + 1)):
        start_idx = int(i * chord_len * sample_rate)
        end_idx = min(int((i + 1) * chord_len * sample_rate), len(t))
        if start_idx >= len(t):
            break
            
        t_chord = t[start_idx:end_idx] - (i * chord_len)
        envelope = np.sin(np.pi * (t_chord / chord_len)) ** 0.5 # Smooth swelling envelope
        
        chord_wave = np.zeros(len(t_chord))
        for freq in chord:
            # Warm saw/sine hybrid
            chord_wave += 0.5 * np.sin(2 * np.pi * freq * t_chord)
            chord_wave += 0.25 * np.sin(2 * np.pi * freq * 2 * t_chord)
            chord_wave += 0.1 * np.sin(2 * np.pi * (freq * 1.002) * t_chord) # Chorus detune
            
        # Add deep subtle sub-bass
        sub_freq = chord[0] / 2.0
        sub_wave = 0.6 * np.sin(2 * np.pi * sub_freq * t_chord)
        
        music[start_idx:end_idx] += (chord_wave * 0.4 + sub_wave * 0.6) * envelope

    # Normalize and lower volume to -22 dB for clean background ducking
    max_val = np.max(np.abs(music))
    if max_val > 0:
        music = (music / max_val) * 0.22
        
    int_music = (music * 32767).astype(np.int16)
    wavfile.write(output_path, sample_rate, int_music)
    return output_path

if __name__ == "__main__":
    generate_ambient_background_music("assets/ambient_beat.wav", 30.0)
    print("Background music synthesized successfully.")
