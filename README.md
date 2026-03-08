# Jarvis AI V2 (CV-Ready Baseline Project)

A clear, fundamentals-focused AI assistant project using Python + Flask + Gemini.

## What This Demonstrates
- Voice input pipeline (`SpeechRecognition`)
- Voice output pipeline (`pyttsx3`)
- Flask dashboard + REST endpoints
- Gemini API integration for AI responses
- Real-time system monitoring (CPU/RAM via `psutil`)
- SQLite-based conversation memory (`jarvis_memory.db`)
- Basic OS automation commands (Notepad, Calculator, YouTube)

## Architecture (Simple and Clear)
- `main.py`
  - Flask routes: `/`, `/data`, `/health`
  - Voice loop (`listen -> command handler -> response`)
  - Built-in command handler + Gemini fallback
  - SQLite memory store (`add_memory`, `recent_memory`)
- `templates/index.html`
  - Live dashboard for query/response/stats/history

## Project Structure
```text
Jarvis-AI/
|-- main.py
|-- templates/
|   `-- index.html
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- README.md
```

## Setup (Windows PowerShell)
```powershell
cd C:\Users\ADMIN\Downloads\mukesh\Jarvis-AI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Environment
```env
GEMINI_API_KEY=your_real_api_key
GEMINI_MODEL=gemini-1.5-flash
PORT=5000
JARVIS_NO_VOICE=false
```

## Run
Normal mode (voice + dashboard):
```powershell
python main.py
```

No-voice mode (dashboard only, useful for demo/testing):
```powershell
$env:JARVIS_NO_VOICE='true'; python main.py
```

Dashboard URL:
```text
http://127.0.0.1:5000
```

## CV Description (Use This)
Designed a voice-enabled AI assistant with Flask dashboard, Gemini API integration, and SQLite memory.
Implemented modular command handling for system automation and real-time monitoring of CPU/RAM metrics.

## Notes
- Keep `.env` private (never commit API key).
- `jarvis_memory.db` is auto-created and git-ignored.
