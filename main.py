from fastapi import FastAPI
from pydantic import BaseModel
import os, subprocess, uuid
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Req(BaseModel):
    url: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/transcribe-url")
def transcribe(req: Req):
    uid = str(uuid.uuid4())[:8]
    audio = f"/tmp/{uid}.mp3"
    subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", audio, req.url], check=True)
    myfile = genai.upload_file(audio)
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(["Transcribe this audio word by word with timestamps", myfile])
    os.remove(audio)
    return {"transcript": result.text, "title": "Video Transcript"}
