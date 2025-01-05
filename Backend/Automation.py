from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt 
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Google API key.

# Define CSS class for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb VaWMnf", "pclqee", "tw-data-text tw-text-small tw-ta",
          "IZ6rdc", "Colour Lyric", "VLc64", "webanswers-webanswers-table__webanswers-table", "dDoNo ikb4Bb gpt", "sXLaOe",
          "LGOjhe", "VQF4g", "qv3Wpe", "kno-rdesc", "sXLaOe"]

# Define a user agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Initialize the Groq client for API requests
client = Groq(api_key=GroqAPIKey)

# Define professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatbot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    """Function to perform a Google search."""
    search(Topic)  # Use DuckDuckGo's search function to perform a Google search
    return True  # Indicate success.

def Content(Topic):
    """Function to generate content using AI and save it to a file."""

    def OpenNotepad(File):
        """Nested function to open a file in Notepad."""
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, File])  # Open the file in Notepad.

    def ContentWriterAI(prompt):
        """Nested function to generate content using the AI chatbot."""
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's proper messages.

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Specify the AI model.
            messages=SystemChatbot + messages,  # Include system instructions and chat history.
            max_tokens=2048,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness.
            top_p=1,  # Use nucleus sampling for response diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine stopping conditions.
        )

        Answer = ""  # Initialize an empty string for the response.

        # Process response in proper byte chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("<s/>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer
    
    Topic: str = Topic.replace("Content ", "")  # Remove the "Content" prefix from the topic.
    ContentByAI = ContentWriterAI(Topic)  # Generate content using the AI chatbot.
    
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as f:
        f.write(ContentByAI)  # Write the content to the file.
        f.close()  # Close the file.

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
    return True  # Indicate success.


def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Create the YouTube search URL.
    webbrowser.open(Url4Search)  # Open the YouTube search page in the user's default browser.
    return True  # Indicate success.

def PlayYoutube(Topic):
    playonyt(Topic)  # Play the YouTube video.
    return True  # Indicate success.

def OpenApp(app, sess=requests.session()):
    """Function to open an application."""
    # Handle social media and common websites directly
    common_sites = {
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "linkedin": "https://www.linkedin.com",
        "youtube": "https://www.youtube.com",
        "canva" : "https://www.canva.com"
    }
    
    app_lower = app.lower()
    if app_lower in common_sites:
        webopen(common_sites[app_lower])
        return True
        
    try:
        # First try to open as a desktop app
        appopen(app, output=True, throw_error=True)
        return True
    except:
        try:
            # Try direct website access first
            webopen(f"https://{app}.com")
            return True
        except:
            # If both above methods fail, use a search query to find the app
            try:
                webopen(f"https://www.google.com/search?q={app}")
                return True
            except:
                print(f"Could not find or open {app}")
                return False


def CloseApp(app):

    if "chrome" in app:
        pass # Close Chrome browser.
    else:
        try:
            close(app, output=True, throw_error=True)  # Attempt to close the application.
            return True  # Indicate success.
        except:
            return False  # Indicate failure.

def System(command):
    """Function to execute system-level commands."""
    
    def mute():
        """Nested function to mute the system volume."""
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.
    
    def unmute():
        """Nested function to unmute the system volume."""
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.
    
    def volume_up():
        """Nested function to increase the system volume."""
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.
    
    def volume_down():
        """Nested function to decrease the system volume."""
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True  # Indicate success.

async def TranslateAndExecute(commands: list[str]):
    """Asynchronous function to translate and execute user commands."""
    funcs = []  # List to store asynchronous tasks.


    for command in commands:
        command.lower()
        if command.startswith("open "):  # Handle "open" commands.
            if "open it" in command:  # Ignore "open it" commands.
                pass
            
            if "open file" == command:  # Ignore "open file" commands.
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)

        elif command.startswith("general"):  # Placeholder for general commands.
            pass

        elif command.startswith("realtime"):  # Placeholder for real-time commands.
            pass

        elif command.startswith("close"):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)

        elif command.startswith("play"):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))  # Schedule YouTube playback.
            funcs.append(fun)

        elif command.startswith("content"):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation.
            funcs.append(fun)

        elif command.startswith("google search"):  # Handle search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search
            funcs.append(fun)

        elif command.startswith("youtube search"):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule YouTube search.
            funcs.append(fun)

        elif command.startswith("system"):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
            funcs.append(fun)

        else:
            print(f"No function found. For {command}")  # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.
    
    for result in results:  # Process the results.
        if isinstance(result, str):
            pass
        else:
            yield result

async def Automation(commands: list[str]):
    """Asynchronous function to handle automation execution."""
    async for result in TranslateAndExecute(commands):  # Translate and execute commands.
        pass
    
    return True  # Indicate success.
