# Speech to Text - Real-time Multilingual Transcription

A modern web application for real-time speech-to-text transcription powered by OpenAI's Whisper AI. Supports 17+ languages with a clean, professional interface.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-green)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

## Features

✨ **Real-time Transcription**
- Live audio transcription as you speak
- Continuous text accumulation across sessions
- Automatic language detection or manual language selection

🌍 **Multilingual Support**
- Supports 17+ languages including:
  - English, Hindi, Tamil, Telugu, Bengali, Marathi
  - Gujarati, Kannada, Malayalam, Punjabi, Urdu
  - Spanish, French, German, Chinese, Japanese, Arabic

🎨 **Modern UI**
- Dark-themed professional interface
- Responsive design (desktop & mobile)
- Clean, intuitive controls
- Real-time transcription indicators

🔧 **Technical Features**
- FastAPI backend with HTTP POST endpoints
- OpenAI Whisper base model (139MB, ~1GB RAM required)
- FFmpeg for audio format conversion
- MediaRecorder API for browser audio capture
- Professional icon-based UI (no emojis)

## Requirements

- **Python:** 3.8+
- **FFmpeg:** Must be installed and available in PATH
- **RAM:** Minimum 2GB (for Whisper base model)
- **Browser:** Chrome, Firefox, Edge, Safari (with microphone support)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ChetandeepSingh/speech-to-text.git
cd speech-to-text
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r app/requirements.txt
```

### 4. Install FFmpeg

**Windows (using winget):**
```bash
winget install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

## Usage

### Start the Server

```bash
python app/main.py
```

The server will start at `http://localhost:8000`

### Using the Application

1. **Open the Web Interface:**
   - Navigate to `http://localhost:8000` in your browser
   - Allow microphone access when prompted

2. **Select Language (Optional):**
   - Choose a language from the dropdown for better accuracy
   - Leave as "Auto-detect" to let Whisper detect the language

3. **Record:**
   - Click the microphone button to start recording
   - Speak clearly into your microphone
   - The button turns red with a pulsing animation while recording

4. **Real-time Transcription:**
   - Every 3 seconds, audio is sent to the server for transcription
   - Transcript appears in the text box below
   - "Transcribing..." indicator shows when processing

5. **Stop Recording:**
   - Click the stop button (square icon) to stop recording
   - Final audio chunk is automatically transcribed
   - Transcript persists in the box

6. **Manage Transcript:**
   - **Copy:** Copy the entire transcript to clipboard
   - **Clear:** Clear the transcript to start fresh

## Project Structure

```
speech-to-text/
├── app/
│   ├── main.py                 # FastAPI backend server
│   ├── requirements.txt         # Python dependencies
│   ├── static/
│   │   └── index.html          # Frontend UI
│   └── README.md               # App documentation
├── start.ps1                    # PowerShell startup script
├── PROJECT_STATUS.md            # Project status tracking
└── README.md                    # This file
```

## API Endpoints

### GET /
Returns the frontend HTML interface.

### POST /transcribe
Transcribes uploaded audio file.

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- audio (file): Audio file (webm, wav, mp3, ogg, m4a, flac)
- language (string): Language code (e.g., 'en', 'hi', 'ta') - optional
```

**Response:**
```json
{
  "text": "Transcribed text here",
  "language": "en",
  "success": true
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "text": "",
  "success": false
}
```

## Supported Language Codes

| Language | Code |
|----------|------|
| English | `en` |
| Hindi | `hi` |
| Tamil | `ta` |
| Telugu | `te` |
| Bengali | `bn` |
| Marathi | `mr` |
| Gujarati | `gu` |
| Kannada | `kn` |
| Malayalam | `ml` |
| Punjabi | `pa` |
| Urdu | `ur` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |
| Chinese | `zh` |
| Japanese | `ja` |
| Arabic | `ar` |

## Configuration

### Environment Variables

```bash
# Set custom Whisper model (default: base)
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large
```

Model sizes:
- **tiny:** ~39MB (fastest, lower accuracy)
- **base:** ~139MB (recommended, good balance)
- **small:** ~466MB (better accuracy)
- **medium:** ~1.5GB (good accuracy)
- **large:** ~2.9GB (best accuracy, slower)

### Server Configuration

Edit `app/main.py` to change:
- Host: Default `0.0.0.0` (accessible from network)
- Port: Default `8000`
- Reload: Default `True` (for development)

```python
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

## Performance Tips

1. **Optimize Audio Chunks:**
   - Frontend sends audio every 3 seconds
   - Adjust `CHUNK_INTERVAL_MS` in `index.html` for faster/slower transcription

2. **Use Auto-detect:**
   - If accuracy is low, explicitly select the language
   - Whisper works better with longer audio clips

3. **GPU Support:**
   - For faster transcription, use GPU
   - Requires CUDA-capable GPU and `torch` with CUDA
   - Installation: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

## Troubleshooting

### Issue: "No module named 'whisper'"
**Solution:** Install dependencies
```bash
pip install -r app/requirements.txt
```

### Issue: FFmpeg not found
**Solution:** Ensure FFmpeg is installed and in PATH
```bash
ffmpeg -version  # Test if FFmpeg is accessible
```

### Issue: "Microphone access denied"
**Solution:**
- Check browser permissions for microphone
- Chrome: Settings → Privacy → Site Settings → Microphone
- Firefox: Preferences → Privacy → Permissions → Microphone

### Issue: Low accuracy
**Solution:**
- Speak clearly and slowly
- Reduce background noise
- Explicitly select the language instead of auto-detect
- Use a larger Whisper model (small, medium, large)

### Issue: Server crashes or slow transcription
**Solution:**
- Check RAM availability (Whisper base needs ~2GB)
- Reduce `CHUNK_INTERVAL_MS` to send smaller chunks
- Switch to a smaller model (tiny)

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Recommended |
| Firefox | ✅ Full | Full support |
| Safari | ✅ Full | macOS 14.1+ |
| Edge | ✅ Full | Chromium-based |
| Opera | ✅ Full | Chromium-based |

## Development

### Running in Development Mode

```bash
# Start with auto-reload
python app/main.py
```

### Code Structure

**Backend (`app/main.py`):**
- FastAPI application
- `/transcribe` endpoint for audio processing
- FFmpeg integration for audio conversion
- Whisper integration for transcription

**Frontend (`app/static/index.html`):**
- Pure HTML/CSS/JavaScript (no build tools)
- MediaRecorder API for audio capture
- Fetch API for server communication
- Responsive design with CSS Grid

## Deployment

### Local Network Access
The application is accessible from other devices on your network:
```
http://<your-machine-ip>:8000
```

### Production Deployment Options

1. **Render.com** (Free tier available)
   - Supports Python applications
   - WebSocket-capable
   - ~512MB RAM free tier

2. **Railway.app**
   - Easy Python deployment
   - Pay-per-use pricing

3. **Fly.io**
   - Docker-based deployment
   - Generous free tier

**Note:** Netlify and Vercel don't support long-running Python backends required for this app.

## Limitations

- **File Size:** Maximum practical audio length depends on RAM (Whisper processes entire file in memory)
- **Accuracy:** Depends on audio quality, language, and model size
- **Latency:** Transcription speed depends on CPU/GPU and model size
- **Concurrent Users:** Single instance handles one user at a time (consider load balancing for production)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/ChetandeepSingh/speech-to-text/issues)
- Check existing issues and discussions

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition model
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [FFmpeg](https://ffmpeg.org/) - Audio processing

## Changelog

### Version 1.0.0 (Initial Release)
- Real-time speech-to-text transcription
- Multilingual support (17+ languages)
- Modern, professional UI
- HTTP-based audio transmission
- Auto-language detection
- Transcript persistence
- Copy to clipboard functionality

---

**Last Updated:** December 2024
**Author:** Chetandeep Singh
