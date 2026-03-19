import pyttsx3
from gtts import gTTS
import pygame
import pywhatkit
import webbrowser
import datetime
import os
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import speech_recognition as sr


# -------------------- INIT --------------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    print("Jarvis:", text)

    tts = gTTS(text=text, lang='en')
    tts.save("voice.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.unload()
    os.remove("voice.mp3")
    
    
# -------------------- VOICE INPUT --------------------


def listen():
    print("Listening...")

    fs = 16000
    duration = 3  

    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
    except:
        print("Mic error")
        return None

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, fs, recording)

    with sr.AudioFile(temp_file.name) as source:
        audio = recognizer.record(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        print("Could not understand")
        return None

# -------------------- COMMAND PROCESS --------------------

def process_command(command):

    if not command:
        return   

    if "hello" in command:
        speak("Hello, how can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {current_date}")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")   

    elif "instagram" in command:
        speak("Opening Instagram")   
        webbrowser.open("https://instagram.com")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "play" in command:
        song = command.replace("play", "").strip()

        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Please say the song name")

    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "exit" in command or "stop" in command:
        speak("Goodbye")
        exit()

    else:
        speak("Sorry, I don't understand")


# -------------------- MAIN --------------------


speak("Jarvis initialized")

while True:
    command = listen()

    if command is None:
        continue

    process_command(command)