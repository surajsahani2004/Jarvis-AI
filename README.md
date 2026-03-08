# Jarvis AI V2 (Python + Flask + Gemini)

Voice-enabled virtual assistant with a real-time Flask dashboard.

## Features
- Voice command recognition (`SpeechRecognition`)
- Text-to-speech response (`pyttsx3`)
- Gemini AI response generation (`google-genai`)
- Live web dashboard for command/response/system stats
- CPU and RAM monitoring (`psutil`)
- Basic Windows automation commands (Notepad, Calculator)

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

Set `.env` values:
```env
GEMINI_API_KEY=your_real_api_key
GEMINI_MODEL=gemini-1.5-flash
PORT=5000
```

Run:
```powershell
python main.py
```

Dashboard:
```text
http://127.0.0.1:5000
```

## Notes
- `venv/` and `jarvis_memory.db` are intentionally ignored in Git.
- Keep your Gemini API key private (never commit `.env`).
