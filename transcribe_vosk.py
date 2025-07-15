import os
import queue
import sounddevice as sd
import vosk
import sys
import json

VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
if not os.path.exists(VOSK_MODEL_PATH):
    print(f"Please download the Vosk model and unpack as '{VOSK_MODEL_PATH}' in the current folder.")
    print("Download from: https://alphacephei.com/vosk/models")
    sys.exit(1)

q = queue.Queue()
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

model = vosk.Model(VOSK_MODEL_PATH)
rec = vosk.KaldiRecognizer(model, 16000)

print("Say something (Ctrl+C to stop)...")
with sd.RawInputStream(samplerate=16000, blocksize = 8000, dtype='int16', channels=1, callback=callback):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get('text', '')
            print("You said:", text)
            break
        # else: rec.PartialResult() # can print partial results if desired 