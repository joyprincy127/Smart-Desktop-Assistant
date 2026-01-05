import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pyautogui
import time
import os

INTENTS = {
    "OPEN_BROWSER": ["open chrome", "open google", "launch browser", "start browser"],
    "OPEN_YOUTUBE": ["open youtube", "start youtube"],
    "SEARCH": ["search", "find"],
    "OPEN_NOTEPAD": ["open notepad"],
    "OPEN_CALCULATOR": ["open calculator"],
    "OPEN_DOWNLOADS": ["open downloads", "downloads folder", "open download"],
    "EXIT": ["exit", "stop", "quit", "close assistant", "shutdown assistant"]
}


def get_intent(query):
    query = query.lower()
    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in query:
                return intent
    return "UNKNOWN"


def open_browser():
    speak("Opening browser")
    webbrowser.open("https://www.google.com")

def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def open_notepad():
    speak("Opening Notepad")
    os.system("notepad")

def open_calculator():
    speak("Opening Calculator")
    os.system("calc")

def open_downloads():
    speak("Opening Downloads folder")
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.startfile(downloads_path)


def search_google(query):
    speak("Searching")
    query = query.replace("search", "").replace("find", "")
    webbrowser.open(f"https://www.google.com/search?q={query}")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)


# Make assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to microphone
r = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source)

        query = r.recognize_google(audio)
        print("User said:", query)
        speak(query)
        return query.lower()

    except sr.UnknownValueError:
        speak("I didn't understand")
        return ""
    except sr.RequestError:
        speak("Network error")
        return ""
    except Exception as e:
        print("Error:", e)
        return ""

def contains_any(text, keywords):
    return any(word in text for word in keywords)

# Main function for commands
def run_voice_assistant():
    speak("Voice assistant activated")

    while True:
        query = listen()
        print("FINAL QUERY:", query)

        if query == "":
            continue

        print("Processed query:", query)

        # -------- OPEN GOOGLE --------
        if "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
            continue

        # -------- OPEN YOUTUBE --------
        if "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            continue

        # -------- OPEN NOTEPAD --------
        if "open notepad" in query:
            speak("Opening Notepad")
            os.system("notepad")
            continue

        # -------- OPEN CALCULATOR --------
        if "open calculator" in query:
            speak("Opening Calculator")
            os.system("calc")
            continue

        # -------- OPEN CHROME --------
        if contains_any(query, ["open chrome", "open browser", "open google"]):
            speak("Opening Chrome")
            webbrowser.open("https://www.google.com")
            continue

        # -------- SEARCH --------
        if "search" in query:
            search_text = query.replace("search", "").strip()
            if search_text == "":
                speak("What should I search for?")
                continue
            speak(f"Searching for {search_text}")
            webbrowser.open(f"https://www.google.com/search?q={search_text}")
            continue



        # -------- EXIT --------
        if contains_any(query, ["stop", "exit", "quit", "close assistant"]):
            speak("Goodbye")
            break

        # -------- FALLBACK --------
        speak("Sorry, I don't know how to do that yet")



if __name__ == "__main__":
    run_voice_assistant()

