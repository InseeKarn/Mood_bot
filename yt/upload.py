import os
import random
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
load_dotenv()
youtube_api = os.getenv("YT_API")


def get_service():
    """
    created and return service object YouTube API
    """
    creds = None  # token/credentials

    # if token.json (has been login) → load token.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # if not or token expire → create new OAuth flow 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh TOKEN
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(
                port=0,
                access_type="offline",
                prompt="consent"
            )
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # build YouTube API service object
    return build("youtube", "v3", credentials=creds)

def upload_video(file_path, title, description, 
                 category=None, privacy=None):
    """
    Upload YouTube videos
    """
    youtube = get_service()  # get service object

    # load .env if not have use , ""
    category = category or os.getenv("YT_CATEGORY", "24")
    privacy = privacy or os.getenv("YT_PRIVACY", "unlisted")

    #body (data of videos)
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category,
            "tags": [
                "shorts", "fyp", "viral", "sadmood", "quotes", "lifequotes",
                "inspiration", "motivation", "deepquotes", "emotional",
                "selfhelp", "mentalhealth", "selfcare", "mindfulness"
            ]
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        }
    }

    # Prepare file to upload
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    # request to API
    request = youtube.videos().insert(
        part="snippet,status",  # Must match fields in body
        body=body,
        media_body=media
    )

    print(f"Uploading...")
    response = request.execute()  # wait for result
    video_id = response["id"]     # save videoId 
    video_url = f"https://youtu.be/{video_id}"
    print(f"✅ Uploaded: https://youtu.be/{video_id}")
    return video_url

    # print(youtube_api)
    
def run_upload():
    # raw_title = """Pick One… If You Dare 😱 | Would You Rather #fyp #shorts #vira'"""
    title_ran = random.choice([
        "Even in Pain, You’re Stronger Than You Think 💔",
        "When Life Feels Heavy, Remember Your Inner Strength 🌧️",
        "Finding Light in the Darkest Moments 🖤",
        "Embrace Your Journey, Resilience Comes From Struggle 🌱",
        "Hope Exists Even When You Can’t Feel It 💭"
        ])

    clean_title = " ".join(title_ran.split())
    # x <= 100
    clean_title = clean_title[:100]

    description_ran = random.choice([
        "💔 Feeling low? These deep thoughts and quotes remind you that survival itself is proof of strength. #sad #mentalhealth #motivation #emotional #deepquotes",
        "🌧️ Life feels heavy sometimes, but even small victories matter. Reflect, heal, and keep going. #sadmood #healing #motivation #mentalhealth",
        "🖤 Emotional reflections for anyone struggling to find hope. Your journey is real, and your strength is undeniable. #emotional #deepthoughts #mentalhealth",
        "🌱 Tough days teach resilience. Let these quotes inspire courage and self-kindness. #motivation #mentalhealth #deepquotes",
        "💭 Feeling isolated or overwhelmed? These words remind you that hope and light are still possible. #sad #healing #emotional #mentalhealth"
    ])

    file_path = "src/outputs/final.mp4"
    video_url = upload_video(
        file_path= file_path,
        title=clean_title,
        description=description_ran
    )

    # 🆕 Delete after uploaded
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"🗑️ Deleted file: {file_path}")
        except Exception as e:
            print(f"⚠️ Failed to delete file: {e}")

    return video_url

if __name__ == "__main__":
    run_upload()