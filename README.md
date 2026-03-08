# Jarvis AI - Voice Assistant with Gemini + Live Dashboard

Jarvis AI is a Python-based desktop voice assistant that listens to commands, speaks responses, uses Google Gemini for intelligent conversation, and exposes a lightweight Flask dashboard for live status updates.

## Features
- Voice input via microphone (`SpeechRecognition`)
- Text-to-speech output (`pyttsx3`)
- AI responses powered by `gemini-1.5-flash`
- Session memory/context for more natural conversations
- Windows automation commands (Notepad, Calculator)
- YouTube playback by voice command
- Real-time system stats (CPU and RAM) on dashboard (`psutil`)
- Graceful exit command (`exit` / `stop`)

## Tech Stack
- Python
- Flask
- Google GenAI SDK
- SpeechRecognition + PyAudio
- pyttsx3
- psutil

## Project Structure
```text
Jarvis-AI/
├─ main.py
├─ requirements.txt
├─ jarvis_memory.db
└─ README.md
```

## Quick Start
1. Clone repository:
```bash
git clone https://github.com/surajsahani2004/Jarvis-AI.git
cd Jarvis-AI
```

2. Create virtual environment:
```bash
python -m venv .venv
```

3. Activate environment:
- Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure Gemini API key in `main.py`:
```python
client = genai.Client(api_key="YOUR_API_KEY_HERE")
```

6. Run:
```bash
python main.py
```

## Example Voice Commands
- `open notepad`
- `open calculator`
- `play [song name] on youtube`
- `time`
- `exit` or `stop`

## How It Works
1. Flask server starts and opens local dashboard.
2. Jarvis listens continuously from microphone.
3. If a local command is detected, it executes immediately.
4. Otherwise, Jarvis sends prompt + memory context to Gemini and speaks the response.
5. Dashboard endpoint `/data` streams latest query, response, CPU, RAM, and status.

## Notes
- This project is currently optimized for Windows automation commands.
- Keep your API key private; do not commit real keys to GitHub.
- If you use this as a portfolio project, add dashboard screenshots under a `screenshots/` folder and link them here.

## Author
Suraj Sahani  
B.Sc Computer Science
