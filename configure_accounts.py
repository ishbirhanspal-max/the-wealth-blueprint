import os
import sys
import getpass

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

def read_env():
    env_dict = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_dict[k.strip()] = v.strip()
    return env_dict

def write_env(env_dict):
    lines = [
        "# The Wealth Blueprint Autopilot Credentials",
        f"INSTAGRAM_USERNAME={env_dict.get('INSTAGRAM_USERNAME', '')}",
        f"INSTAGRAM_PASSWORD={env_dict.get('INSTAGRAM_PASSWORD', '')}",
        f"INSTAGRAM_ACCESS_TOKEN={env_dict.get('INSTAGRAM_ACCESS_TOKEN', '')}",
        f"INSTAGRAM_USER_ID={env_dict.get('INSTAGRAM_USER_ID', '')}",
        f"GEMINI_API_KEY={env_dict.get('GEMINI_API_KEY', '')}",
        f"PEXELS_API_KEY={env_dict.get('PEXELS_API_KEY', '')}"
    ]
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def main():
    print("========================================================")
    print("  THE WEALTH BLUEPRINT: ACCOUNT CREDENTIALS SETUP")
    print("========================================================")
    print("Enter your social media account details below.")
    print("These are stored locally on your machine in .env only.\n")

    env_dict = read_env()

    # Instagram
    print("--- 1. INSTAGRAM REELS ---")
    current_ig_user = env_dict.get("INSTAGRAM_USERNAME", "")
    ig_user = input(f"Enter Instagram Username [{current_ig_user}]: ").strip()
    if ig_user:
        env_dict["INSTAGRAM_USERNAME"] = ig_user

    ig_pass = getpass.getpass("Enter Instagram Password (typing hidden): ").strip()
    if ig_pass:
        env_dict["INSTAGRAM_PASSWORD"] = ig_pass

    # YouTube
    print("\n--- 2. YOUTUBE SHORTS ---")
    client_sec = os.path.join(BASE_DIR, "client_secret.json")
    if os.path.exists(client_sec):
        print("[OK] Found client_secret.json in project folder.")
    else:
        print("[!] To publish to YouTube automatically:")
        print("    Download OAuth 2.0 Client ID JSON from Google Cloud Console")
        print(f"    and save it as: {client_sec}")

    write_env(env_dict)
    print("\n========================================================")
    print("[SUCCESS] Credentials saved locally to .env!")
    print("Now simply run: publish_next_video.bat to post automatically.")
    print("========================================================")

if __name__ == "__main__":
    main()
