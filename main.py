from __future__ import annotations

import datetime as dt
import os
import sqlite3
import threading
import webbrowser
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

try:
    import psutil
except ModuleNotFoundError:
    psutil = None

try:
    from google import genai
except (ModuleNotFoundError, ImportError):
    genai = None

try:
    import pyttsx3
except ModuleNotFoundError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ModuleNotFoundError:
    sr = None

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "jarvis_memory.db"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip() or "gemini-1.5-flash"
WEB_PORT = int(os.getenv("PORT", "5000"))
NO_VOICE_MODE = os.getenv("JARVIS_NO_VOICE", "false").lower() == "true"

client = genai.Client(api_key=GEMINI_API_KEY) if (genai is not None and GEMINI_API_KEY) else None
app = Flask(__name__)

lock = threading.Lock()
chat_context = (
    "System: You are Jarvis, a concise and smart AI assistant. "
    "Developer: Suraj Sahani.\n"
)

data_store = {
    "query": "None",
    "response": "Ready",
    "cpu": 0.0,
    "ram": 0.0,
    "status": "ACTIVE",
    "last_updated": "",
}


def init_memory_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_memory(query: str, response: str, source: str) -> None:
    created_at = dt.datetime.now().isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO memory (query, response, source, created_at) VALUES (?, ?, ?, ?)",
            (query, response, source, created_at),
        )
        conn.commit()


def recent_memory(limit: int = 6) -> list[dict[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT query, response, source, created_at
            FROM memory
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "query": row["query"],
            "response": row["response"],
            "source": row["source"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def update_stats() -> None:
    cpu = 0.0
    ram = 0.0
    if psutil is not None:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent

    with lock:
        data_store["cpu"] = cpu
        data_store["ram"] = ram
        data_store["last_updated"] = dt.datetime.now().strftime("%I:%M:%S %p")


def speak(text: str) -> None:
    with lock:
        data_store["response"] = text
    print(f"Jarvis: {text}")

    if pyttsx3 is None:
        return

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)
        engine.setProperty("rate", 185)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        # Keep assistant running even if TTS engine fails.
        pass


def listen() -> str:
    if sr is None:
        return "none"

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recognizer.pause_threshold = 0.5
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=5)

        print("Recognizing...")
        spoken_text = recognizer.recognize_google(audio, language="en-IN")
        with lock:
            data_store["query"] = spoken_text
        return spoken_text.lower().strip()
    except sr.WaitTimeoutError:
        return "none"
    except sr.UnknownValueError:
        return "none"
    except Exception:
        return "none"


def handle_builtin_command(cmd: str) -> tuple[bool, bool]:
    """
    Returns: (handled, should_exit)
    """
    if "exit" in cmd or "stop" in cmd:
        with lock:
            data_store["status"] = "OFFLINE"
        speak("Goodbye Suraj.")
        add_memory(cmd, "Session stopped", "system")
        return True, True

    if "open notepad" in cmd:
        speak("Opening Notepad.")
        os.system("notepad")
        add_memory(cmd, "Opened Notepad", "system")
        return True, False

    if "open calculator" in cmd:
        speak("Opening Calculator.")
        os.system("calc")
        add_memory(cmd, "Opened Calculator", "system")
        return True, False

    if "time" in cmd:
        now = dt.datetime.now().strftime("%I:%M %p")
        response = f"Sir, the time is {now}"
        speak(response)
        add_memory(cmd, response, "system")
        return True, False

    if "play" in cmd and "youtube" in cmd:
        song = cmd.replace("play", "").replace("on youtube", "").strip()
        response = f"Playing {song} on YouTube."
        speak(response)
        webbrowser.open(
            f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}&sp=EgIQAQ%253D%253D"
        )
        add_memory(cmd, response, "system")
        return True, False

    return False, False


def ask_gemini(cmd: str) -> str:
    global chat_context

    if genai is None:
        return "google-genai package missing. Install dependencies from requirements.txt."
    if client is None:
        return "Gemini API key missing. Please set GEMINI_API_KEY in .env file."

    try:
        with lock:
            chat_context += f"User: {cmd}\nJarvis: "
            prompt = chat_context

        result = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        reply = (result.text or "").strip() or "No response generated."

        with lock:
            chat_context += f"{reply}\n"

        return reply
    except Exception:
        return "Cloud request failed. Please check internet or API key."


def jarvis_loop() -> None:
    speak("All systems are operational, Suraj. Dashboard and memory initialized.")

    while True:
        update_stats()
        cmd = listen()
        if cmd == "none":
            continue

        handled, should_exit = handle_builtin_command(cmd)
        if should_exit:
            break
        if handled:
            continue

        reply = ask_gemini(cmd)
        speak(reply)
        add_memory(cmd, reply, "gemini")


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"ok": True, "status": data_store.get("status", "UNKNOWN")})


@app.route("/data")
def data():
    update_stats()
    with lock:
        snapshot = dict(data_store)
    snapshot["history"] = recent_memory(limit=6)
    return jsonify(snapshot)


if __name__ == "__main__":
    init_memory_db()

    if NO_VOICE_MODE:
        app.run(port=WEB_PORT, debug=False)
    else:
        threading.Thread(
            target=lambda: app.run(port=WEB_PORT, debug=False, use_reloader=False),
            daemon=True,
        ).start()
        webbrowser.open(f"http://127.0.0.1:{WEB_PORT}")
        jarvis_loop()
