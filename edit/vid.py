import requests
import os
import random
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PIXABAY_KEY")
QUERY = "lonely night"
BG_FOLDER = "src/bg"
JSON_FILE = "src/downloaded.json"
BLACKLIST_FILE = "src/blacklist.json"
MAX_IDS = 40

os.makedirs(BG_FOLDER, exist_ok=True)

# Load used IDs
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        used_ids = json.load(f)
else:
    used_ids = []

# Load blacklist
if os.path.exists(BLACKLIST_FILE):
    with open(BLACKLIST_FILE, "r") as f:
        blacklist_ids = json.load(f)
else:
    blacklist_ids = []

def save_used_ids():
    with open(JSON_FILE, "w") as f:
        json.dump(used_ids, f)

def get_vids():
    global used_ids
    all_videos = []
    page = 1
    url = "https://pixabay.com/api/videos/"
    while len(all_videos) < 200:
        params = {
            "key": API_KEY,
            "q": QUERY,
            "per_page": 70,
            "orientation": "vertical",
            "page": page,
        }

        response = requests.get(url, params=params, timeout=20)
        if response.status_code != 200:
            print("Error:", response.status_code)
            return

        data = response.json()
        hits = data.get("hits", [])
        if not hits:
            print("Videos not found.")
            return
        all_videos.extend(hits)
        page += 1

    if not all_videos:
        print("No videos found")
        return

    # 🔹 filter vertical videos
    vertical_videos = [
        v for v in all_videos
        if (v["videos"].get("large") or v["videos"].get("medium") or v["videos"].get("small")) 
        and (v["videos"].get("large") or v["videos"].get("medium") or v["videos"].get("small"))["width"] < (v["videos"].get("large") or v["videos"].get("medium") or v["videos"].get("small"))["height"]
        and v["id"] not in used_ids
        and v["id"] not in blacklist_ids
    ]

    if len(vertical_videos) < 5:
        # reset used_ids if not enough videos
        print("Not enough available videos, resetting used IDs.")
        used_ids = []
        save_used_ids()
        vertical_videos = [
            v for v in all_videos
            if (v["videos"].get("large") or v["videos"].get("medium") or v["videos"].get("small")) 
            and (v["videos"].get("large") or v["videos"].get("medium") or v["videos"].get("small"))["width"] < (v["videos"].get("large") or v["videos"].get("medium") or v["videos"].get("small"))["height"]
            and v["id"] not in blacklist_ids
        ]

    selected_videos = random.sample(vertical_videos, min(5, len(vertical_videos)))

    for i, video in enumerate(selected_videos, start=1):
        vid_id = video["id"]
        vid_info = video["videos"].get("large") or video["videos"].get("medium") or video["videos"].get("small")
        video_url = vid_info["url"]
        filename = os.path.join(BG_FOLDER, f"video_{vid_id}.mp4")

        print(f"Downloading video {i} (ID: {vid_id}): {video_url}")
        r = requests.get(video_url, stream=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Saved as {filename}")
        print("-" * 50)

        # Save ID
        used_ids.append(vid_id)

    # Reset if >= MAX_IDS
    if len(used_ids) > MAX_IDS:
        used_ids = []

    save_used_ids()


if __name__ == "__main__":
    get_vids()
