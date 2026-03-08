import os
import sys
import json
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field

# --- 1. SETUP AND CONFIGURATION ---

# The script will attempt to get the API key from environment variables first,
# then prompt the user for it if needed.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_api_key():
    """Prompts the user for the API key if it's not set."""
    global GEMINI_API_KEY
    if not GEMINI_API_KEY:
        print("--- J.A.R.V.I.S. Setup Required ---")
        print("I need your Gemini API Key to access the intelligence core.")
        # Prompts for input directly
        key = input("Please paste your Gemini API Key here: ").strip()
        if not key:
            print("API Key is mandatory. Exiting.")
            sys.exit(1)
        GEMINI_API_KEY = key
        os.environ["GEMINI_API_KEY"] = key
    return GEMINI_API_KEY

# --- 2. LOCAL SYSTEM TOOLS (The Plugins) ---
# These functions simulate the actions J.A.R.V.I.S. would take locally.

def create_file_or_folder(name: str, path: str, type: str) -> str:
    """
    Creates a new file or folder at the specified path.
    NOTE: This is a simulation. A real implementation would use os.makedirs() or similar.
    """
    if not name or not path or type not in ["file", "folder"]:
        return "ERROR: Missing required parameters for file/folder creation."
    
    # Simulation: Replace this with actual file system code (e.g., using 'os' module)
    print(f"\n[SYSTEM EXECUTION] Attempting to create a {type} named '{name}' in path '{path}'...")
    return f"Execution successful, Sir/Ma'am. A new {type} named '{name}' has been logically created in the path '{path}'. Awaiting next command."

def control_media_playback(action: str) -> str:
    """
    Performs common media playback controls (play, pause, next track).
    NOTE: This is a simulation. A real implementation would use pyautogui or a media API.
    """
    if action not in ["play", "pause", "next", "stop"]:
        return "ERROR: Invalid media action specified. Use 'play', 'pause', 'next', or 'stop'."

    # Simulation: Replace this with actual media control code (e.g., using 'pyautogui')
    print(f"\n[SYSTEM EXECUTION] Controlling media: Action '{action}'...")
    return f"Execution successful, Sir/Ma'am. Media playback has been set to '{action}'. Is there anything else?"

# --- 3. PYDANTIC TOOL SCHEMAS (For the LLM) ---
# We define the structure for the LLM to call these Python functions.

class CreateFileOrFolder(BaseModel):
    """A tool for creating a new file or folder in the local file system."""
    name: str = Field(description="The name of the file or folder to create, e.g., 'Project_Report' or 'notes.txt'.")
    path: str = Field(description="The absolute or relative path where the item should be created, e.g., 'C:\\Users\\Tony\\Documents' or 'Desktop'.")
    type: str = Field(description="The type of item to create, must be 'file' or 'folder'.")

class ControlMediaPlayback(BaseModel):
    """A tool for controlling local music and media playback."""
    action: str = Field(description="The media control action to perform, must be one of 'play', 'pause', 'next', or 'stop'.")


# --- 4. THE J.A.R.V.I.S. CLASS ---

class JarvisAssistant:
    def __init__(self, api_key: str):
        # Initialize Gemini Client
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.5-flash'
        
        # Mapping for function execution
        self.tool_functions = {
            "create_file_or_folder": create_file_or_folder,
            "control_media_playback": control_media_playback,
        }
        
        # Mapping for tool schemas
        self.tool_schemas = [
            CreateFileOrFolder, 
            ControlMediaPlayback
        ]
        
        # System instructions to define the AI's personality and role
        system_instruction = (
            "You are J.A.R.V.I.S., a sophisticated, polite, and slightly formal AI desktop assistant. "
            "Address the user as 'Sir' or 'Ma'am'. "
            "Your primary goal is to manage local system tasks using the provided tools. "
            "ONLY use the provided tools if the user's request explicitly matches the tool's purpose. "
            "For general knowledge or non-system tasks, respond conversationally. "
            "For file paths, assume the user is referring to a common location like 'Documents' or 'Desktop' if not specified."
        )
        
        # Initialize the chat session with tools and system instruction
        self.chat = self.client.chats.create(
            model=self.model,
            system_instruction=system_instruction,
            config=types.GenerateContentConfig(
                tools=self.tool_schemas
            )
        )
        print("\n--- J.A.R.V.I.S. System Initialized ---")
        self.speak("System initialized and ready for commands, Sir. Please enter your first query.")


    # Simulated TTS Function
    def speak(self, text: str):
        """Simulates Text-to-Speech output."""
        # In a real app, this would use pyttsx3.
        print(f"\nJ.A.R.V.I.S. (TTS) > {text}")

    # Simulated STT Function
    def listen(self) -> str:
        """Simulates Speech-to-Text input."""
        # In a real app, this would use SpeechRecognition for voice input.
        return input("\nUSER (Voice/Text) > ")

    def handle_tool_calls(self, tool_calls: list) -> list:
        """
        Executes the Python function requested by the LLM (Tool Use).
        Returns a list of tool responses to be sent back to the LLM.
        """
        tool_responses = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            args = dict(tool_call.function.args)

            if function_name in self.tool_functions:
                # Execute the actual local Python function
                result = self.tool_functions[function_name](**args)
                
                # Format the result back into a Content object for the LLM
                tool_responses.append(
                    types.Content(
                        role="tool",
                        parts=[types.Part.from_tool_response(name=function_name, response={"result": result})]
                    )
                )
                self.speak(result) # J.A.R.V.I.S. immediately speaks the system result
            else:
                tool_responses.append(
                    types.Content(
                        role="tool",
                        parts=[types.Part.from_tool_response(name=function_name, response={"error": f"Tool '{function_name}' not found."})]
                    )
                )
        return tool_responses

    def run_command(self, user_query: str):
        """
        The core loop logic: sends query, processes response, handles tool calls.
        """
        if user_query.lower() in ["quit", "exit", "shutdown"]:
            self.speak("Shutting down core intelligence. Goodbye, Sir.")
            return False # Stop loop flag

        try:
            # 1. Send the user's query and chat history to the model
            response = self.chat.send_message(user_query)

            # 2. Check if the model is calling a tool (local function)
            if response.function_calls:
                
                # 3. Handle the tool call locally
                tool_responses = self.handle_tool_calls(response.function_calls)
                
                # 4. Send the tool execution result back to the model for a final, natural language summary
                final_response = self.chat.send_message(tool_responses)
                
                # 5. Speak the model's final summary
                if final_response.text:
                    self.speak(final_response.text)

            # 6. If no tool is called, respond conversationally
            elif response.text:
                self.speak(response.text)
                
        except APIError as e:
            self.speak(f"System Error: I was unable to connect to the intelligence core. Please check your API key and network connection. Error details: {e}")
        except Exception as e:
            self.speak(f"A critical error occurred: {e}")
            return False
            
        return True # Continue loop flag

    def start(self):
        """Starts the main command-line application loop."""
        running = True
        while running:
            user_input = self.listen()
            running = self.run_command(user_input)

# --- 5. EXECUTION ---

if __name__ == "__main__":
    # Get the key before initializing the assistant
    api_key = get_api_key()
    
    # Initialize and run the assistant
    jarvis = JarvisAssistant(api_key)
    jarvis.start()
