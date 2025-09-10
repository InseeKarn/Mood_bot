import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PIXABAY_KEY")


query = "night mood"

url = f"https://pixabay.com/api/videos/?key={API_KEY}&q={query}&per_page=10"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    hits = data.get("hits", [])

    if not hits:
        print("Videos not found.")
    else:
        for i, video in enumerate(hits, start=1):
            print(f"video {i}:")
            print("  URL main:", video.get("pageURL"))

            videos = video.get("videos", {})
            for quality, info in videos.items():
                print(f"  {quality}: {info.get('url')}")
            print("-" * 50)
else:
    print("Error:", response.status_code)