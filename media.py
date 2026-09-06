import os
import math
import random
import requests
import cv2
import numpy as np

WIDTH = 1080
HEIGHT = 1920
FPS = 30

def create_candlestick_clip(output_path: str, duration: float = 4.0):
    """Renders a dynamic 1080x1920 climbing candlestick financial chart."""
    total_frames = int(duration * FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))
    
    prices = [900, 920, 910, 940, 930, 970, 960, 1010, 990, 1050, 1040, 1100, 1080, 1150]
    
    for frame_idx in range(total_frames):
        progress = frame_idx / total_frames
        # Dark modern background with subtle gradient
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        img[:, :] = (14, 18, 22) # Deep charcoal blue
        
        # Draw background grid
        for y in range(200, HEIGHT - 200, 160):
            cv2.line(img, (80, y), (WIDTH - 80, y), (28, 35, 45), 1)
        for x in range(120, WIDTH, 160):
            cv2.line(img, (x, 200), (x, HEIGHT - 200), (28, 35, 45), 1)
            
        # Draw animated ascending candles
        num_candles = min(len(prices), int(progress * len(prices)) + 2)
        candle_width = 42
        spacing = 65
        start_x = 120
        
        points = []
        for i in range(num_candles):
            cx = start_x + (i * spacing)
            base_price = prices[i]
            # Map price to Y coordinate
            cy = int(HEIGHT - 400 - (base_price - 850) * 2.8)
            points.append((cx, cy))
            
            # Wick
            cv2.line(img, (cx, cy - 40), (cx, cy + 40), (0, 230, 118), 2)
            # Body
            top_y = cy - 25
            bot_y = cy + 25
            cv2.rectangle(img, (cx - candle_width//2, top_y), (cx + candle_width//2, bot_y), (0, 230, 118), -1)
            
        # Glowing trend line connecting candles
        if len(points) > 1:
            for p_idx in range(len(points) - 1):
                cv2.line(img, points[p_idx], points[p_idx + 1], (0, 255, 180), 3)
                
        # Header text
        cv2.putText(img, "FINANCIAL ASSET INDEX // +34.8%", (100, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 180), 2)
        
        out.write(img)
        
    out.release()
    return output_path

def create_particles_clip(output_path: str, duration: float = 4.0):
    """Renders sleek rising golden wealth particles."""
    total_frames = int(duration * FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))
    
    # 50 particles
    np.random.seed(42)
    particles = []
    for _ in range(60):
        particles.append({
            "x": random.randint(100, WIDTH - 100),
            "y": random.randint(200, HEIGHT - 200),
            "speed": random.uniform(1.5, 4.0),
            "radius": random.randint(3, 10),
            "color": (random.randint(180, 255), random.randint(215, 255), random.randint(30, 100)) # Gold/Cyan BGR
        })
        
    for frame_idx in range(total_frames):
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        img[:, :] = (10, 12, 16) # Deep black
        
        for p in particles:
            p["y"] -= p["speed"]
            if p["y"] < 100:
                p["y"] = HEIGHT - 100
                p["x"] = random.randint(100, WIDTH - 100)
                
            # Draw glowing particle
            cx, cy = int(p["x"]), int(p["y"])
            rad = p["radius"]
            # Outer halo
            cv2.circle(img, (cx, cy), rad * 2, (p["color"][0]//4, p["color"][1]//4, p["color"][2]//4), -1)
            # Inner core
            cv2.circle(img, (cx, cy), rad, p["color"], -1)
            
        cv2.putText(img, "WEALTH ACCELERATOR PROTOCOL", (100, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 215, 0), 2)
        out.write(img)
        
    out.release()
    return output_path

def create_cyber_clip(output_path: str, duration: float = 4.0):
    """Renders high-tech futuristic digital scanner grid."""
    total_frames = int(duration * FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))
    
    for frame_idx in range(total_frames):
        progress = frame_idx / total_frames
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        img[:, :] = (8, 10, 15)
        
        # Center rotating radar circle
        center = (WIDTH // 2, HEIGHT // 2)
        angle = frame_idx * 0.05
        cv2.circle(img, center, 320, (35, 60, 80), 2)
        cv2.circle(img, center, 200, (45, 90, 120), 2)
        cv2.circle(img, center, 80, (0, 200, 255), 2)
        
        # Radar sweep line
        end_x = int(center[0] + 320 * math.cos(angle))
        end_y = int(center[1] + 320 * math.sin(angle))
        cv2.line(img, center, (end_x, end_y), (0, 220, 255), 3)
        
        # Digital code strings
        cv2.putText(img, "AI ENGINE STATUS: ACTIVE // 99.8%", (100, 280), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 220, 255), 2)
        cv2.putText(img, "DATA STREAM LATENCY: 0.12ms", (100, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 150, 180), 1)
        
        out.write(img)
        
    out.release()
    return output_path

def download_pexels_video(query: str, api_key: str, output_path: str) -> bool:
    """Downloads a vertical 9:16 stock video from Pexels."""
    try:
        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=1"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            videos = data.get("videos", [])
            if videos:
                video_files = videos[0].get("video_files", [])
                # Pick portrait HD file
                portrait_files = [f for f in video_files if f.get("width", 0) <= f.get("height", 0)]
                target = portrait_files[0] if portrait_files else video_files[0]
                dl_url = target.get("link")
                if dl_url:
                    r = requests.get(dl_url, stream=True, timeout=20)
                    with open(output_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            f.write(chunk)
                    return True
    except Exception as e:
        print(f"[Warning] Pexels download failed for '{query}': {e}")
    return False

def get_broll_clips(keywords: list, total_duration: float, output_dir: str, pexels_key: str = None) -> list:
    """
    Returns a sequence of vertical video clip paths to cover total_duration.
    Downloads from Pexels if API key is provided, or procedurally renders.
    """
    os.makedirs(output_dir, exist_ok=True)
    clips = []
    clip_dur = 3.5 # Fast cuts every 3.5s
    num_needed = int(math.ceil(total_duration / clip_dur))
    
    generators = [create_candlestick_clip, create_particles_clip, create_cyber_clip]
    
    for i in range(num_needed):
        clip_path = os.path.join(output_dir, f"broll_{i}.mp4")
        
        downloaded = False
        if pexels_key and i < len(keywords):
            downloaded = download_pexels_video(keywords[i], pexels_key, clip_path)
            
        if not downloaded:
            gen_func = generators[i % len(generators)]
            gen_func(clip_path, clip_dur)
            
        clips.append(clip_path)
        
    return clips

if __name__ == "__main__":
    clips = get_broll_clips(["finance", "luxury", "tech"], 10.0, "assets/video_clips")
    print(f"Prepared {len(clips)} b-roll clips.")
