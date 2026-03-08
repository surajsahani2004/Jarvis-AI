# JarvisAI - Smart Voice Assistant Dashboard

JarvisAI is a lightweight web + voice assistant project built with PHP and JavaScript.  
It provides:
- Live weather updates
- Top Indian news headlines
- Browser voice-command actions (speech recognition)

## Features
- Voice trigger button with speech recognition (`SpeechRecognition` / `webkitSpeechRecognition`)
- Voice commands like:
  - `weather`
  - `weather in <city>`
  - `news`
- Real-time weather from OpenWeatherMap API
- Top headlines from NewsAPI
- Modern responsive UI dashboard
- Optional MySQL setup scaffold for future user features

## Tech Stack
- PHP (backend rendering + API calls)
- JavaScript (voice commands + browser interaction)
- CSS (custom modern responsive styling)
- MySQL (optional schema included)

## Project Structure
```text
Jarvis-AI/
├─ api/
│  ├─ env.php
│  ├─ config.php
│  └─ functions.php
├─ public/
│  ├─ index.php
│  ├─ index.py
│  ├─ css/
│  │  ├─ style.css
│  │  └─ db/
│  │     ├─ jarvis.sql
│  │     └─ README.md
│  └─ js/
│     └─ main.js
├─ .env.example
├─ .gitignore
├─ requirements-python.txt
└─ README.md
```

## Setup (XAMPP / Local PHP)
1. Clone repo:
```bash
git clone https://github.com/surajsahani2004/Jarvis-AI.git
cd Jarvis-AI
```

2. Create `.env` from sample:
```bash
cp .env.example .env
```

3. Add API keys in `.env`:
- `OPENWEATHER_API_KEY`
- `NEWS_API_KEY`

4. Put project inside XAMPP `htdocs` (or configure virtual host).

5. Open:
```text
http://localhost/Jarvis-AI/public/
```

## Optional Python Assistant
`public/index.py` is a separate CLI assistant flow using Gemini tool-calling.

Run it with:
```bash
pip install -r requirements-python.txt
python public/index.py
```

## Voice Commands
- `weather` -> scrolls to weather panel
- `weather in mumbai` -> reloads weather for city
- `news` -> scrolls to news panel

## Database (Optional)
If you want DB support for future modules:
1. Import `public/css/db/jarvis.sql`
2. Update `.env` DB values
3. Set `DB_CONNECT=true`

## Security Notes
- API keys are now read from `.env`, not hardcoded.
- Do not commit `.env` to GitHub.

## Author
Suraj Sahani
