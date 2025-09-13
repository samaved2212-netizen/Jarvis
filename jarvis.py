import os
import datetime
import random
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import pyautogui
import pyjokes
import wikipedia
import cohere
from dotenv import load_dotenv

# Load .env and get Cohere key
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 150)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
            return None
    try:
        print("🔎 Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
        return command.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return None

def wish_me():
    speak("Welcome back!")
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 17:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("Jarvis at your service. How can I help you?")

def play_music(song_name=None):
    music_dir = os.path.join(os.path.expanduser("~"), "Music")
    try:
        songs = os.listdir(music_dir)
        if song_name:
            songs = [s for s in songs if song_name.lower() in s.lower()]
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song}")
        else:
            speak("No matching songs found.")
    except:
        speak("Couldn't open your music folder.")

def take_screenshot():
    img = pyautogui.screenshot()
    path = os.path.join(os.path.expanduser("~"), "Pictures", "screenshot.png")
    img.save(path)
    speak("Screenshot saved to your Pictures folder.")

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.DisambiguationError:
        speak("Too many results. Please be specific.")
    except:
        speak("I couldn't find anything useful.")

def ask_cohere(prompt):
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        reply = response.generations[0].text.strip()
        speak(reply)
    except Exception as e:
        print("Cohere Error:", e)
        speak("Sorry, I couldn't get a response at the moment.")

# === Main Program ===
if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if not query:
            continue

        if "time" in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")
        elif "date" in query:
            today = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {today}")
        elif "play music" in query:
            song = query.replace("play music", "").strip()
            play_music(song)
        elif "screenshot" in query:
            take_screenshot()
        elif "open youtube" in query:
            wb.open("https://www.youtube.com")
        elif "open google" in query:
            wb.open("https://www.google.com")
        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "").strip()
            search_wikipedia(topic)
        elif "joke" in query:
            speak(pyjokes.get_joke())
        elif "exit" in query or "offline" in query:
            speak("Going offline. Goodbye!")
            break
        else:
            ask_cohere(query)
