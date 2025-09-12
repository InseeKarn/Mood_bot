import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PIXABAY_KEY")
# print(os.getenv("PIXABAY_KEY"))
QUERY = "night"

def get_vids():
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": API_KEY,
        "q": QUERY,
        "per_page": 70,
        "orientation": "vertical"
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code == 200:
        data = response.json()
        hits = data.get("hits", [])

        if not hits:
            print("Videos not found.")
            return
        
        # 🔹 filter onl vertical_videos
        vertical_videos = []
        for video in hits:
            vid_info = video["videos"].get("large") or video["videos"].get("medium") or video["videos"].get("small")
            if vid_info and vid_info["width"] < vid_info["height"]:
                vertical_videos.append(video)

        if not vertical_videos:
            print("No vertical videos found.")
            return

        # 🔹 Random 5
        num_videos = min(5, len(vertical_videos))
        random_videos = random.sample(vertical_videos, num_videos)

        os.makedirs("src/bg", exist_ok=True)

        for i, video in enumerate(random_videos, start=1):
            vid_info = video["videos"].get("large") or video["videos"].get("medium") or video["videos"].get("small")
            video_url = vid_info["url"]
            filename = f"src/bg/video_{i}.mp4"

            print(f"Downloading video {i}: {video_url}")
            r = requests.get(video_url, stream=True)
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Saved as {filename}")
            print("-" * 50)

    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    get_vids()
