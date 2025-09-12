# Dev by InseeKarn

from edit.vid import get_vids
from edit.edit import create_video
from yt.upload import run_upload
from notify.discord import discord_message
import asyncio

async def main():
    await get_vids()          
    create_video()            
    video_url = run_upload()
    if video_url:
        print("upload step pass")
        user_id = "304548816907010050"
        discord_message(f"✅ <@{user_id}> Uploaded vids: {video_url} ✅")
    else:
        print("⚠️ Upload failed, skipping Discord notify")

if __name__ == "__main__":
    asyncio.run(main())

