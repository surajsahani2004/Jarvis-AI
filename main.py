import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import threading
import psutil
from flask import Flask, render_template, jsonify
from google import genai

# --- Configuration ---
# Apni Key Yahan Dalein
client = genai.Client(api_key="YOUR_API_KEY_HERE")
app = Flask(__name__)

# Simple Chat Context for Memory
chat_context = "System: You are Jarvis, a smart female AI. Developer: Suraj Sahani. Date: Jan 23, 2026.\n"
data_store = {"query": "None", "response": "Ready", "cpu": 0, "ram": 0, "status": "ACTIVE"}

@app.route('/')
def home(): return render_template('index.html')

@app.route('/data')
def data():
    data_store["cpu"] = psutil.cpu_percent()
    data_store["ram"] = psutil.virtual_memory().percent
    return jsonify(data_store)

def speak(text):
    data_store["response"] = text
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) # Female Voice
    engine.setProperty('rate', 190)
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 0.5 # Fast response
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=5)
            print("Recognizing...")
            word = r.recognize_google(audio, language='en-IN')
            data_store["query"] = word
            return word.lower()
        except: return "none"

def jarvis_logic():
    speak("All systems are operational, Suraj. Dashboard and memory initialized.")
    global chat_context
    while True:
        cmd = listen()
        
        if 'exit' in cmd or 'stop' in cmd:
            data_store["status"] = "OFFLINE"
            speak("Goodbye Suraj.")
            os._exit(0)
            
        # 1. WINDOWS AUTOMATION
        elif 'open notepad' in cmd:
            speak("Opening Notepad.")
            os.system("notepad")

        elif 'open calculator' in cmd:
            speak("Opening Calculator.")
            os.system("calc")

        # 2. MEDIA CONTROL (Auto-Exit for better experience)
        elif 'play' in cmd and 'youtube' in cmd:
            song = cmd.replace("play", "").replace("on youtube", "").strip()
            speak(f"Playing {song} on YouTube. Goodbye.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}&sp=EgIQAQ%253D%253D")
            os._exit(0)

        elif 'time' in cmd:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {now}")

        # 3. AI BRAIN WITH MEMORY
        elif cmd != "none":
            try:
                chat_context += f"User: {cmd}\nJarvis: "
                res = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=chat_context
                )
                reply = res.text.strip()
                chat_context += f"{reply}\n"
                speak(reply)
            except:
                speak("Sir, cloud latency detected. Local systems are fine.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(port=5000, debug=False, use_reloader=False)).start()
    webbrowser.open("http://127.0.0.1:5000")
    jarvis_logic()