import eel
import pyttsx3
import time
import speech_recognition as sr

class VirtualAssistant:
    def __init__(self):
        pass

    def speak(self, text):
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 125)
        eel.DisplayMessage(text)
        engine.say(text)
        eel.receiverText(text)
        engine.runAndWait()

    def take_command(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("Listening...")
            eel.DisplayMessage("Listening...")
            audio = r.record(source, duration=5)

        try:
            print("Recognizing...")
            eel.DisplayMessage("Recognizing...")
            query = r.recognize_google(audio, language="en")
            print(f"User said: {query}")
            eel.DisplayMessage(query)
            time.sleep(2)
            eel.ShowHood()
        except Exception as e:
            print("Error:", e)
            return ""
        
        return query.lower()

# Tạo một instance của VirtualAssistant
assistant = VirtualAssistant()

@eel.expose
def all_command(message=1):
    if message == 1:
        query = assistant.take_command()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import playYouTube
            playYouTube(query)
        else:
            print("Not run!")
    except Exception as e:
        print("Error:", e)

    eel.ShowHood()
