# Dev by InseeKarn

from edit.vid import get_vids
from edit.edit import create_video
from yt.upload import run_upload
from notify.discord import discord_message


if __name__ == "__main__":

    get_vids()


    import os
    BG_FOLDER = "src/bg"
    video_files = [f for f in os.listdir(BG_FOLDER) if f.endswith(".mp4")]
    if len(video_files) < 1:
        raise RuntimeError(f"❌ BG files not ready. Found {len(video_files)} clips.")


    create_video()

    video_url = run_upload()
    if video_url:
        user_id = "304548816907010050"
        discord_message(f"✅ <@{user_id}> Uploaded vids: {video_url} ✅")