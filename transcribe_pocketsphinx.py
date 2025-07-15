import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Say something (press Ctrl+C to exit)...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_sphinx(audio)
    print("You said:", text)
except Exception as e:
    print("Recognition error:", e) 