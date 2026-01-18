import sys
import subprocess
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
from logger import log_event

# =========================
# GLOBAL STATE
# =========================
current_mode = "study"   # study | presentation | idle
mouse_process = None

# =========================
# TEXT TO SPEECH
# =========================
def speak(text):
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("TTS Error:", e)

# =========================
# SPEECH RECOGNITION
# =========================
r = sr.Recognizer()

def update_mode_ui(mode):
    try:
        with open("mode.txt", "w") as f:
            f.write(mode)
    except:
        pass

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source)

        query = r.recognize_google(audio)
        print("User said:", query)
        return query.lower()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        speak("Network error")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""

def contains_any(text, keywords):
    return any(word in text for word in keywords)

# =========================
# MAIN ASSISTANT LOOP
# =========================
def run_voice_assistant():
    global current_mode
    global mouse_process

    speak("Voice assistant activated")
    log_event("Voice Assistant Started")

    while True:
        query = listen()

        if query == "":
            continue

        print("FINAL QUERY:", query)

        # =========================
        # EXIT (ALWAYS ALLOWED)
        # =========================
        if contains_any(query, ["stop", "exit", "quit", "close assistant"]):
            speak("Goodbye")
            log_event("Voice Assistant Stopped")

            if mouse_process:
                mouse_process.terminate()
                mouse_process.wait(timeout=2)
                mouse_process = None

            break

        # =========================
        # MODE SWITCHING (ALWAYS ALLOWED)
        # =========================
        if contains_any(query, ["study mode", "switch to study"]):
            current_mode = "study"
            update_mode_ui("STUDY")

            speak("Study mode activated")
            log_event("Study Mode Activated")

            if mouse_process:
                mouse_process.terminate()
                mouse_process.wait(timeout=2)
                mouse_process = None

            continue

        if contains_any(query, ["presentation mode", "start presentation"]):
            current_mode = "presentation"
            update_mode_ui("PRESENTATION")

            speak("Presentation mode activated. Use hand gestures to control slides.")
            log_event("Presentation Mode Activated")

            if mouse_process is None:
                mouse_process = subprocess.Popen(
                    [sys.executable, "virtual_mouse_basic.py"]
                )

            continue

        if contains_any(query, ["idle mode", "go idle", "rest mode"]):
            current_mode = "idle"
            update_mode_ui("IDLE")

            speak("Idle mode activated")
            log_event("Idle Mode Activated")

            if mouse_process:
                mouse_process.terminate()
                mouse_process.wait(timeout=2)
                mouse_process = None

            continue

        # =========================
        # BLOCK COMMANDS IN NON-STUDY MODES
        # =========================
        if current_mode in ["presentation", "idle"]:
            speak("Commands are disabled during presentation and idle mode")
            log_event("Blocked command attempted")
            continue

        # =========================
        # STUDY MODE COMMANDS
        # =========================
        if "open google" in query:
            speak("Opening Google")
            log_event("Opened Google")
            webbrowser.open("https://www.google.com")
            continue

        if "open youtube" in query:
            speak("Opening YouTube")
            log_event("Opened YouTube")
            webbrowser.open("https://www.youtube.com")
            continue

        if "open notepad" in query:
            speak("Opening Notepad")
            log_event("Opened Notepad")
            os.system("notepad")
            continue

        if "open calculator" in query:
            speak("Opening Calculator")
            log_event("Opened Calculator")
            os.system("calc")
            continue

        if "search" in query:
            search_text = query.replace("search", "").strip()
            if search_text:
                speak(f"Searching for {search_text}")
                log_event(f"Searched: {search_text}")
                webbrowser.open(
                    f"https://www.google.com/search?q={search_text}"
                )
            else:
                speak("What should I search for?")
            continue

        # =========================
        # IOT DEMO COMMANDS
        # =========================
        if "turn on light" in query:
            speak("Turning on smart light")
            log_event("Smart Light ON")
            print("[IoT] Light ON")
            continue

        if "turn off light" in query:
            speak("Turning off smart light")
            log_event("Smart Light OFF")
            print("[IoT] Light OFF")
            continue

        # =========================
        # FALLBACK
        # =========================
        speak("Sorry, I don't know how to do that yet")
        log_event("Unknown Command")

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run_voice_assistant()
