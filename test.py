from faster_whisper import WhisperModel

CACHE_DIR = "models_cache/ggml-small.bin"
AUDIO_FILE = "src/tts/sentence.mp3"

model = WhisperModel(CACHE_DIR, device="cpu", compute_type="int8")
segments, info = model.transcribe(AUDIO_FILE, beam_size=5, word_timestamps=True)
