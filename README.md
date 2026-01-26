Jarvis AI - Smart Virtual Assistant
Jarvis AI V3.6 is an advanced, voice-activated virtual assistant developed in Python. It leverages the Google Gemini 1.5 Flash API for intelligent, context-aware conversations and features a Real-time Web Dashboard for monitoring system performance and chat logs.

Key Features
Smart Memory (Context Awareness): Jarvis remembers previous interactions within a session, allowing for natural, human-like conversations.

Live Web Dashboard: A sleek, Flask-powered web interface that displays real-time voice commands and AI responses.

System Health Monitoring: Tracks live hardware performance, including CPU and RAM usage, using the psutil library.

Windows Automation: Executes voice commands to launch native applications like Notepad, Calculator, and Command Prompt.

Media Control: Seamlessly plays music or videos on YouTube and JioSaavn via voice commands.

Auto-Exit System: To prevent microphone feedback, Jarvis automatically shuts down its listener when media playback begins.

Tech Stack
Language: Python 3.13

AI Engine: Google Gemini-1.5-Flash

Web Framework: Flask (For the Dashboard)

Core Libraries:

SpeechRecognition: For processing voice input.

Pyttsx3: For high-quality text-to-speech output.

psutil: For real-time hardware analytics.

Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/SahaniSuraj/Jarvis-AI-V2.git
cd Jarvis-AI-V2
Install Dependencies:

Bash
pip install -r requirements.txt
Configure API Key: Open main.py and enter your Gemini API Key: client = genai.Client(api_key="YOUR_API_KEY")

Run the Application:

Bash
python main.py
Dashboard Preview
The dashboard provides a centralized view of the assistant's operations:

User Command: Displays the recognized text from your voice input.

Jarvis Intelligence: Shows the AI-generated response in real-time.

System Stats: Visual indicators for current CPU and RAM consumption.

Developed by: Suraj Sahani Education: B.Sc Computer Science Student, Mumbai University