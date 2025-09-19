import json
import os
import random
import requests
from dotenv import load_dotenv

from elevenlabs import ElevenLabs, VoiceSettings

load_dotenv()

SAD_JSON = "sad.json"
USED_JSON = "used_sad.json"
OUTPUT_DIR = "src/tts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Eleven TTS Config
client = ElevenLabs(api_key=os.getenv("ELEVEN_API"))

API_KEY = os.getenv("ELEVEN_API")
headers = {
    "xi-api-key": API_KEY
}

response = requests.get("https://api.elevenlabs.io/v1/user", headers=headers)
data = response.json()

print(json.dumps(data, indent=2))

credits = data.get("subscription", {}).get("credits_remaining", 0)
print("Real credits available:", credits)

if credits < 160:
    print("Not enough credits! Stop run")
    exit()


def get_sentences():
    # load sentences
    with open(SAD_JSON, "r", encoding="utf-8") as f:
        sentences = json.load(f)

    # load used sentences
    if os.path.exists(USED_JSON):
        with open(USED_JSON, "r", encoding="utf-8") as f:
            used_sentences = json.load(f)
    else:
        used_sentences = []

    # randomly select a sentence that hasn't been used
    available = [s for s in sentences if s not in used_sentences]

    if not available:
        print("Not have alivable sentences!")
        exit()

    sentence = random.choice(available)
    print("Selected sentence:", sentence)

    # TTS
    audio_generator = client.text_to_speech.convert(
        voice_id="uhw0FsfiUiP7FZzm1Yue",
        text=sentence,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=0.9,
        ),
    )

    # save audio
    filename = os.path.join(OUTPUT_DIR, "sentence.mp3")
    timestamps = None
    with open(filename, "wb") as f:
        for chunk in audio_generator:
            if isinstance(chunk, dict) and "timestamps" in chunk:
                timestamps = chunk["timestamps"]  # รับ timestamps ของคำ
            elif isinstance(chunk, bytes):
                f.write(chunk)

    print("Saved audio as:", filename)

    # Save used sentence
    used_sentences.append(sentence)
    with open(USED_JSON, "w", encoding="utf-8") as f:
        json.dump(used_sentences, f, ensure_ascii=False, indent=2)

    print("Done!")
    return sentence

if __name__ == "__main__":
    get_sentences()