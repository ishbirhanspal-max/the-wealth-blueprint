# How to Connect YouTube & Instagram for 100% Cloud Autopilot

This guide explains how to connect your **YouTube Channel** and **Instagram Account** to the automated cloud publisher so it publishes **2 videos every day for 50 days (100 videos total)** even when your **laptop is completely switched off**.

---

## ⚡ How It Works While Your Laptop is Off

1. Your code and 100-video content engine live in your free GitHub repository.
2. Every day at **12:00 PM IST** (lunch scroll peak) and **8:00 PM IST** (evening prime time), **GitHub Actions** automatically wakes up on GitHub's cloud servers.
3. It renders that day's 1080x1920 video with neural speech (US or Indian English voice) and ambient lo-fi music in 15 seconds.
4. It publishes directly to your YouTube Shorts and Instagram Reels, pins the top comment, logs the post, and shuts down.
5. Your laptop does **not** need to be on or connected to the internet.

---

## 🔴 Part 1: Connect YouTube Shorts (Google Cloud API)

Google requires an official OAuth credential to publish Shorts to your channel. Follow these 5 steps (takes ~3 minutes):

### Step 1: Open Google Cloud Console
1. Go to: **[https://console.cloud.google.com](https://console.cloud.google.com)** and log in with your YouTube Google account.
2. Click the project dropdown at the top and click **New Project**.
3. Name it **`The Wealth Blueprint`** and click **Create**.

### Step 2: Enable the YouTube Data API
1. In the search bar at the top, type **`YouTube Data API v3`**.
2. Click on it and click the blue **ENABLE** button.

### Step 3: Configure the OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen** (from the left menu).
2. Choose **External** and click **Create**.
3. Fill in:
   * **App name**: `The Wealth Blueprint`
   * **User support email**: Your email
   * **Developer contact email**: Your email
4. Click **Save and Continue** through the remaining screens.
5. Under **Test users**, click **Add Users** and add your own Google email address.

### Step 4: Create OAuth Client ID Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **+ CREATE CREDENTIALS** at the top > **OAuth client ID**.
3. Application type: Select **Desktop app**.
4. Name: `Autopilot Uploader`.
5. Click **Create**.
6. A popup appears. Click **DOWNLOAD JSON**.
7. Rename the downloaded file to **`client_secret.json`** and place it in your project folder:
   `C:\Users\ishbi\.gemini\antigravity-ide\scratch\faceless-video-autopilot\client_secret.json`

### Step 5: Authorize Once Locally (Generates `token.json`)
Open your terminal in the project folder and run:
```powershell
python youtube_uploader.py
```
* A Google login page will open in your browser.
* Log into your YouTube channel account and click **Allow**.
* This creates a file called **`token.json`** in your project folder.
* **Open `token.json`**, copy the entire text inside it. You will paste this into GitHub Secrets in Part 3.

---

## 📸 Part 2: Connect Instagram Reels

You have two choices for Instagram:

### Option A: Direct Username & Password (Simplest)
* All you need is your Instagram **Username** and **Password**.
* You will add these as two secrets in GitHub:
  * `INSTAGRAM_USERNAME`
  * `INSTAGRAM_PASSWORD`

*(Tip: If you have Two-Factor Authentication enabled on your personal IG, create an App-Specific Password in Instagram Settings > Accounts Center > Password and Security).*

### Option B: Official Meta Graph API (For Professional/Creator Accounts)
If your Instagram account is an Instagram Professional/Creator account linked to a Facebook Page:
1. Go to **[https://developers.facebook.com](https://developers.facebook.com)** and create a free App (Type: Business).
2. Add the **Instagram Graph API** product.
3. Generate a Never-Expiring User Token with permissions: `instagram_basic`, `instagram_content_publish`.
4. Copy your **Access Token** and your **Instagram User ID**.

---

## ☁️ Part 3: Activate GitHub Cloud Autopilot (Laptop Switched Off)

Now that you have your credentials, save them in GitHub so the cloud servers can publish for you:

### Step 1: Create a GitHub Repository
1. Go to **[https://github.com](https://github.com)** and click **New Repository**.
2. Name it: `faceless-video-autopilot` (set to **Private** so your tokens remain confidential).
3. Push your project from your PC to GitHub:
   ```powershell
   cd C:\Users\ishbi\.gemini\antigravity-ide\scratch\faceless-video-autopilot
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/faceless-video-autopilot.git
   git branch -M master
   git push -u origin master
   ```

### Step 2: Add Secrets to GitHub
1. In your GitHub repository, click **Settings** (top tab).
2. In the left sidebar, click **Secrets and variables > Actions**.
3. Click the green **New repository secret** button and add:

| Secret Name | What to Paste In |
|:---|:---|
| **`YOUTUBE_TOKEN_JSON`** | The entire text contents of your `token.json` file |
| **`INSTAGRAM_USERNAME`** | Your Instagram username (e.g. `TheWealthBlueprint`) |
| **`INSTAGRAM_PASSWORD`** | Your Instagram password |

*(Optional: If using Meta Graph API, add `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_USER_ID` instead).*

### Step 3: Enable Workflow Permissions
1. In your GitHub repository, go to **Settings > Actions > General**.
2. Scroll down to **Workflow permissions**.
3. Select **Read and write permissions** (this allows the cloud bot to commit the publish history log back to the repo).
4. Click **Save**.

---

## 🚀 You're Done! The 50-Day Campaign Is Active

* **Schedule**:
  * **12:00 PM IST (06:30 UTC)**: Posts a Global High-RPM Video (S&P 500, Credit Hacks, AI shortcuts).
  * **08:00 PM IST (14:30 UTC)**: Posts an Indian Finance Loophole Video (RuPay UPI rewards, CIBIL 750+ boost, 15-15-15 Mutual Funds, SGB gold hack).
* **Laptop State**: You can turn off your laptop, travel, or sleep. The cloud server will run on schedule twice every single day for the next 50 days!
