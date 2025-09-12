import os
import random
import numpy as np
from .tts import get_sentences
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips,
    AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
)

BG_FOLDER = "src/bg"
TTS_FOLDER = "src/tts"
MUSIC_FOLDER = "src/music"
FONT_PATH = "src/fonts/bold_font.ttf"

def create_video():
    # ------------------- load clips -------------------
    video_files = [os.path.join(BG_FOLDER, f) for f in os.listdir(BG_FOLDER) if f.endswith(".mp4")]
    video_files = video_files[:5]
    random.shuffle(video_files)

    sentence = get_sentences()

    tts_file = os.path.join(TTS_FOLDER, "sentence.mp3")
    if not os.path.exists(tts_file):
        raise FileNotFoundError("์NOT FOUND TTS: sentence.mp3")

    tts_audio = AudioFileClip(tts_file)
    tts_duration = tts_audio.duration

    # Load clips and resize properly
    clips = [VideoFileClip(vf).resize((720,1280)) for vf in video_files]

    # Adjust clips to match TTS duration
    total_clip_duration = sum(clip.duration for clip in clips)
    adjusted_clips = [clip.set_duration(clip.duration / total_clip_duration * tts_duration) for clip in clips]

    background_clip = concatenate_videoclips(adjusted_clips, method="compose")


    # ------------------- text overlay -------------------
    words = sentence.split()
    per_word_duration = tts_duration / len(words)

    def make_text_clip(word, duration, size=(720,1280), stroke_width=3, stroke_fill="black"):
        img = Image.new("RGBA", size, (0,0,0,0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(FONT_PATH, 50)
        except:
            font = ImageFont.load_default()

        w, h = draw.textsize(word, font=font)
        x = (size[0]-w)/2
        y = (size[1]-h)/2

        # draw stroke
        for dx in range(-stroke_width, stroke_width+1):
            for dy in range(-stroke_width, stroke_width+1):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, y+dy), word, font=font, fill=stroke_fill)

        # draw text
        draw.text((x, y), word, font=font, fill="white")

        img_np = np.array(img)
        return ImageClip(img_np).set_duration(duration)

    word_clips = []
    current_start = 0
    for w in words:
        txt_clip = make_text_clip(w, per_word_duration)
        txt_clip = txt_clip.set_start(current_start).crossfadein(0.1).crossfadeout(0.1) 
        word_clips.append(txt_clip)
        current_start += per_word_duration

    # ------------------- add random music -------------------
    from moviepy.audio.fx.all import audio_loop
    music_files = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith((".mp3", ".wav"))]
    if music_files:
        music_file = random.choice(music_files)
        music_clip = audio_loop(AudioFileClip(music_file), duration=tts_duration).volumex(0.3)
        final_audio = CompositeAudioClip([tts_audio, music_clip])
    else:
        final_audio = tts_audio

    # ------------------- combine video and audio -------------------
    final_clip = CompositeVideoClip([background_clip, *word_clips])
    final_clip = final_clip.set_audio(final_audio.set_start(0))

    OUTPUT_FILE = "src/outputs/final.mp4"
    final_clip.write_videofile(OUTPUT_FILE, codec="libx264", fps=17, threads=4)

    print("✅ Done! Saved as", OUTPUT_FILE)

    # ------------------- close all clips -------------------
    final_clip.close()
    tts_audio.close()
    for clip in clips:
        clip.close()
    for clip in word_clips:
        clip.close()

    # ------------------- Deleate BG_FOLDER -------------------
    for f in os.listdir(BG_FOLDER):
        file_path = os.path.join(BG_FOLDER, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("🗑️ Cleared BG_FOLDER")

    return OUTPUT_FILE

if __name__ == "__main__":
    create_video()
