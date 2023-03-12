import speech_recognition as sr
import pyttsx3
import requests
import json
import webbrowser
import os
import subprocess
from datetime import datetime

# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Get the current time and greet the user accordingly
now = datetime.now()
hour = now.hour
if hour >= 0 and hour < 12:
    greet = "Good morning"
elif hour >= 12 and hour < 18:
    greet = "Good afternoon"
else:
    greet = "Good evening"

speak(f"{greet}, sir. How can I assist you?")

# Main loop
while True:
    # Listen for a command
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    # Recognize the command
    try:
        command = r.recognize_google(audio)
        print("Command:", command)
    except:
        print("Could not understand command.")
        continue

    # Perform the command
    if "open" in command:
        if "code" in command: # If the command contains "code"
            if "directory" in command:
                dir_name = command.split("directory")[1].strip() # Get the directory name from the command
                dir_path = os.path.abspath(dir_name) # Get the absolute path of the directory
                try:
                    subprocess.Popen(['code', dir_path]) # Open the directory in VSCode
                    speak(f"Opening directory {dir_name} in Visual Studio Code")
                except Exception as e:
                    print(e)
                    speak("Sorry, I was unable to open the directory in Visual Studio Code.")
            else:
                speak("Sorry, I didn't understand which directory to open.")
        elif "HTB" in command.upper(): # If the command contains "HTB"
            speak("Opening Hack The Box website")
            webbrowser.open("https://www.hackthebox.com")
        else:
            website = command.replace("open", "").strip()
            speak(f"Opening {website}")
            webbrowser.open(f"https://www.{website}.com")
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query} on Google")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "weather" in command:
        # Make a request to the OpenWeatherMap API
        API_KEY = "YOUR_API_KEY"
        URL = "https://api.openweathermap.org/data/2.5/weather"
        city = "New York" # You can replace "New York" with any city of your choice
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(URL, params=params)
        data = json.loads(response.text)

        # Parse the response and speak the weather information
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius and the weather is {description}")
    elif "stop" in command:
        speak("Goodbye!")
        break
    else:
        speak("Sorry, I didn't understand that command.")
