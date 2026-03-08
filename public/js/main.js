const micBtn = document.getElementById("micBtn");
const voiceStatus = document.getElementById("voiceStatus");
const voiceOutput = document.getElementById("voiceOutput");

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;

function setStatus(message) {
  voiceStatus.textContent = `Status: ${message}`;
}

function setOutput(message) {
  voiceOutput.textContent = message;
}

function speak(text) {
  if (!("speechSynthesis" in window)) {
    return;
  }
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1.0;
  utter.pitch = 1.0;
  utter.lang = "en-US";
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utter);
}

function runCommand(command) {
  const cmd = command.toLowerCase();

  if (cmd.includes("weather in")) {
    const city = cmd.split("weather in")[1]?.trim();
    if (city) {
      setOutput(`Fetching weather for ${city}...`);
      speak(`Fetching weather for ${city}`);
      window.location.href = `?city=${encodeURIComponent(city)}`;
      return;
    }
  }

  if (cmd.includes("weather")) {
    const weatherPanel = document.getElementById("weatherPanel");
    weatherPanel?.scrollIntoView({ behavior: "smooth", block: "start" });
    setOutput("Showing weather panel.");
    speak("Showing weather update.");
    return;
  }

  if (cmd.includes("news")) {
    const newsPanel = document.getElementById("newsPanel");
    newsPanel?.scrollIntoView({ behavior: "smooth", block: "start" });
    setOutput("Showing top news headlines.");
    speak("Showing top news headlines.");
    return;
  }

  setOutput(`Command heard: "${command}". No mapped action yet.`);
  speak("Sorry, I did not understand that command.");
}

if (!Recognition) {
  micBtn.disabled = true;
  micBtn.textContent = "Voice Not Supported";
  setStatus("Speech recognition not supported in this browser.");
} else {
  recognition = new Recognition();
  recognition.continuous = false;
  recognition.lang = "en-US";
  recognition.interimResults = false;

  recognition.onstart = () => setStatus("Listening...");
  recognition.onend = () => setStatus("Idle");
  recognition.onerror = (event) => {
    setStatus(`Error (${event.error})`);
    setOutput("Voice recognition error. Try again.");
  };

  recognition.onresult = (event) => {
    const command = event.results[0][0].transcript.trim();
    setOutput(`You said: ${command}`);
    runCommand(command);
  };
}

micBtn.addEventListener("click", () => {
  if (!recognition) {
    return;
  }
  setOutput("Listening for your command...");
  recognition.start();
});
