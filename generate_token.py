import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(BASE_DIR, "client_secret.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

print("========================================================")
print("  THE WEALTH BLUEPRINT: YOUTUBE AUTHORIZATION")
print("========================================================")
print(">> Opening Google sign-in in your default browser...")
print(">> If the browser does not open automatically, look at the URL printed below.")
print("--------------------------------------------------------")

try:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)

    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    print("\n========================================================")
    print("  [SUCCESS] token.json has been created successfully!")
    print(f"  Saved at: {TOKEN_PATH}")
    print("========================================================")
except Exception as e:
    print(f"\n[!] Error during authentication: {e}")

