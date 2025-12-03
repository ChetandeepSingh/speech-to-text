import os
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import whisper

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Load Whisper model once at startup. Use 'base' for speed and multilingual transcription.
MODEL_NAME = os.environ.get("WHISPER_MODEL", "base")
print(f"Loading Whisper model: {MODEL_NAME}")
model = whisper.load_model(MODEL_NAME)
print("Model loaded successfully!")


@app.get("/")
async def index():
    """Serve the main HTML page"""
    html_file = STATIC_DIR / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return {"error": "Frontend not found. Please ensure static/index.html exists."}


def convert_audio_to_wav(audio_bytes: bytes, input_format: str = "webm") -> str:
    """Convert audio bytes to WAV format using FFmpeg.
    Returns the path to the WAV file.
    """
    # Create temp input file
    with tempfile.NamedTemporaryFile(suffix=f".{input_format}", delete=False) as inp:
        inp.write(audio_bytes)
        inp.flush()
        in_path = inp.name
    
    # Create temp output file
    out_fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(out_fd)
    
    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-err_detect", "ignore_err",
            "-i", in_path,
            "-ac", "1",
            "-ar", "16000",
            "-f", "wav",
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if os.path.exists(out_path) and os.path.getsize(out_path) > 44:
            return out_path
        else:
            raise RuntimeError(f"FFmpeg conversion failed: {result.stderr.decode()}")
    finally:
        # Clean up input file
        try:
            os.remove(in_path)
        except OSError:
            pass


@app.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form(default="")
):
    """
    Transcribe audio file using Whisper.
    
    - audio: Audio file (webm, wav, mp3, etc.)
    - language: Optional language code (e.g., 'en', 'hi', 'ta'). Leave empty for auto-detect.
    """
    wav_path = None
    try:
        # Read uploaded audio
        audio_bytes = await audio.read()
        print(f"Received audio: {len(audio_bytes)} bytes, filename: {audio.filename}")
        
        if len(audio_bytes) < 100:
            return JSONResponse(
                status_code=400,
                content={"error": "Audio file too small", "text": ""}
            )
        
        # Determine input format from filename or content type
        input_format = "webm"
        if audio.filename:
            ext = audio.filename.split(".")[-1].lower()
            if ext in ["webm", "wav", "mp3", "ogg", "m4a", "flac"]:
                input_format = ext
        
        # Convert to WAV
        print(f"Converting {input_format} to WAV...")
        wav_path = convert_audio_to_wav(audio_bytes, input_format)
        print(f"Conversion complete: {wav_path}")
        
        # Transcribe with Whisper
        print(f"Transcribing... (language: {language or 'auto-detect'})")
        
        options = {}
        if language and language.strip():
            options["language"] = language.strip()
        
        result = model.transcribe(wav_path, **options)
        transcript = result.get("text", "").strip()
        detected_language = result.get("language", "unknown")
        
        print(f"Transcript: {transcript}")
        print(f"Detected language: {detected_language}")
        
        return {
            "text": transcript,
            "language": detected_language,
            "success": True
        }
        
    except Exception as e:
        print(f"Transcription error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "text": "", "success": False}
        )
    finally:
        # Clean up WAV file
        if wav_path:
            try:
                os.remove(wav_path)
            except OSError:
                pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
