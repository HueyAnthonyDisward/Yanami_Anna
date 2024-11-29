import eel
import pyttsx3
import time
import speech_recognition as sr

class VirtualAssistant:
    def __init__(self):
        pass

    # Speak the text
    def speak(self, text):
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        
        # Man voice
        engine.setProperty("voice", voices[1].id)
        engine.setProperty("rate", 125)
        
        eel.DisplayMessage(text)
        engine.say(text)
        eel.receiverText(text)
        
        engine.runAndWait()

    # Listen and return the text
    def listen(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("Listening...")
            eel.DisplayMessage("Listening...")
            audio = r.record(source, duration=5)

        try:
            print("Recognizing...")
            
            try:
                eel.DisplayMessage("Recognizing...")
                query = r.recognize_google(audio, language="en")
                eel.DisplayMessage(query)
                print(f"User said: {query}")
            except:
                query = "..."

            time.sleep(2)
            eel.Interface()
        except Exception as e:
            print("Error:", e)
        
        return query.lower()
