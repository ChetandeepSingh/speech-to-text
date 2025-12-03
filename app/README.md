Speech to Text (FastAPI + Whisper)

Overview
- Real-time transcription of multilingual speech (Hindi + English mixed) using OpenAI's open-source Whisper.
- Modern, minimal frontend captures microphone audio and streams small chunks via WebSocket to the FastAPI backend.
- Backend converts WebM/Opus chunks to WAV using ffmpeg and runs Whisper (base model) to produce near real-time transcripts.
- Supports code-switched languages like Hinglish (Hindi + English mixture).

✅ Completed Setup
- Python 3.12.10 installed and configured
- Virtual environment created at `D:\New folder\Speech to text project\.venv`
- All dependencies installed successfully
- ffmpeg verified and working
- Visual C++ Redistributable installed

Quick Start
```powershell
# From the project root directory
cd "d:\New folder\Speech to text project"

# Option 1: Use the start script (recommended)
.\start.ps1

# Option 2: Manual start
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python app\main.py
```

First Run Note
- On first run, Whisper will download the 'base' model (~139MB)
- This only happens once; subsequent runs will be instant
- Wait for the download to complete before opening the browser

Usage
- Open http://localhost:8000 in your browser
- Click "▶ Start Recording" to begin streaming audio
- Speak naturally in Hindi, English, or mixed (Hinglish)
- Select model (base recommended) and optional language in the UI
- Transcript updates in real-time with modern minimal interface
- Click "⏹ Stop" to end the session

Model Options
- tiny: Fastest, lower accuracy (~39M params, ~39MB download)
- base: Recommended - good speed/accuracy balance (~74M params, ~139MB) ✓ Default
- small: Better accuracy, slower (~244M params, ~461MB)
- medium: Best quality for multilingual (~769M params, ~1.5GB)

Installed Packages
- FastAPI 0.115.2
- PyTorch 2.9.1 (CPU version)
- Whisper 20231117
- Python 3.12.10 with all dependencies

Features
- ✅ Real-time audio streaming via WebSocket
- ✅ Multilingual support (Hindi + English code-switching)
- ✅ Modern, responsive UI with recording status indicator
- ✅ Auto-scrolling transcript display
- ✅ Selectable Whisper models for speed/quality tradeoff
- ✅ Optional language specification or auto-detection

Technical Details
- Whisper processes 30s windows internally
- App sends ~500ms audio chunks for near real-time transcription
- Each chunk is converted from WebM/Opus to WAV via ffmpeg
- Backend runs Whisper inference on each chunk
- Frontend displays results with live updates

Notes
- For better accuracy with longer utterances, consider buffering 1-3s of audio before transcription
- The base model handles multilingual transcription well, including Hindi-English code-switching
- For translation to English from other languages, use medium/large models and modify the transcribe() call to include task="translate"
- First model download requires internet connection
