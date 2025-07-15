from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import os
import torch

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp:
            content = await audio.read()
            tmp.write(content)
            tmp_path = tmp.name
        model = whisper.load_model('base')
        result = model.transcribe(tmp_path, language='en', fp16=torch.cuda.is_available())
        os.remove(tmp_path)
        return {"transcription": result['text']}
    except Exception as e:
        print("Transcription error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)}) 