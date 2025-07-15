import speech_recognition as sr
import os

# Ensure Vosk model is downloaded
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
if not os.path.exists(VOSK_MODEL_PATH):
    print(f"Please download the Vosk model and unpack as '{VOSK_MODEL_PATH}' in the current folder.")
    print("Download from: https://alphacephei.com/vosk/models")
    exit(1)

# Set up recognizer and microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Set Vosk as the recognizer
try:
    from vosk import Model, KaldiRecognizer
    model = Model(VOSK_MODEL_PATH)
except ImportError:
    print("vosk not installed. Please install with 'pip install vosk'.")
    exit(1)

print("Say something (press Ctrl+C to exit)...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_vosk(audio, model_path=VOSK_MODEL_PATH)
    print("You said:", text)
except Exception as e:
    print("Recognition error:", e) 