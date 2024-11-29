import os
import eel
import sqlite3
import webbrowser
import pywhatkit as kit
from gtts import gTTS
from playsound import playsound
from datetime import date, datetime
from engine.support import *
from engine.assistant import VirtualAssistant

con = sqlite3.connect("storage.db")
cursor = con.cursor()
assistant = VirtualAssistant()

# Playing assistant sound
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/notify.mp3"
    playsound(music_dir)

class Function:
    def __init__(self):
        pass
    
    def openCommand(self, query):
        query = query.replace("open", "")
        query.lower()

        # Erase space in name
        name = query.strip()

        if name != "":
            try:
                cursor.execute("SELECT path FROM sys_command WHERE sys_name IN (?)", (name,))
                result = cursor.fetchall()

                if len(result) != 0:
                    # Open app in database
                    assistant.speak("Opening app" + query + "...")
                    os.system("start " + result[0][0])
                
                elif len(result) == 0:
                    cursor.execute("SELECT url FROM web_command WHERE web_name IN (?)", (name,))
                    result = cursor.fetchall()

                    if len(result) != 0:
                        # Open web in database
                        assistant.speak("I will opening web" + query + "...")
                        webbrowser.open(result[0][0])

                    else:
                        assistant.speak("I will opening app system" + query + "...")
                        try:
                            # Open app system
                            os.system("start " + query)
                        except:
                            assistant.speak("I don't understand what you say!")
            except:
                assistant.speak("Something went wrong!")

    def playYouTube(self, query):
        search_term = extract_yt_term(query)
        if "Error" not in search_term:
            assistant.speak("I will find '" + search_term + "' on Youtube...")
            kit.playonyt(search_term)
        else:
            assistant.speak("I don't understand what you say!")

    def searchWiki(self, query):
        wiki_script = information_from_wiki(query)
        if "Error" not in wiki_script:
            assistant.speak(wiki_script)
            print(wiki_script)
        else:
            assistant.speak("I don't understand what you say!")

    def searchGoogle(self, query):
        query = query.replace("search", "")
        query = query.replace("google", "")
        search_term = query.strip()
        assistant.speak("I will search '" + search_term + "' on Google...")
        print("VA: Chrome will turn off after 1 minute!")
        open_google_and_search(query)

    def translateVN(self, query):
        assistant.speak(query)
        query = query.replace("translate", "")
        translate_term = translate_to_vietnamese(query)
        if "Error" not in translate_term:
            text = gTTS(text=translate_term, lang='vi')
            filename = "www/assets/audio/voice.mp3"
            text.save(filename)
            eel.DisplayMessage(translate_term)
            playsound(filename)
            eel.receiverText(translate_term)
        else:
            assistant.speak("I don't understand what you say!")

    def announceTime(self):
        current_time = datetime.now().strftime("%H:%M:%S %p")
        assistant.speak("It's " + current_time)
        print(f"VA: Current time: {current_time}")

    def announceDay(self):
        current_day = date.today().strftime("%B %d, %Y")
        assistant.speak("It's " + current_day)
        print(f"VA: Current day: {current_day}")

    def announceWeather(self, query):
        assistant.speak(query)
        query = query.replace("weather", "")
        query = query.replace("today", "")
        weather_term = get_weather_today(query)
        if "Error" not in weather_term:
            print("VA: " + weather_term)
            assistant.speak(weather_term)
        else:
            assistant.speak("I don't understand what you say!")

    def helloUser(self):
        hours = int(datetime.now().strftime("%H"))
        if hours < 12:
            announce = "Good morning, friend. How can I help you?"
            assistant.speak(announce)
            print("VA: " + announce)
        elif 12 <= hours < 18:
            announce = "Good afternoon, friend. How can I help you?"
            assistant.speak(announce)
            print("VA: " + announce)
        else:
            announce = "Good evening, friend. How can I help you?"
            assistant.speak(announce)
            print("VA: " + announce)

    def takeScreenshot(self):
        assistant.speak("Preparing to capture a screenshot in 3 seconds...")
        file_path = capture_screenshot()
        print(f"VA: Screenshot saved: {file_path}")

    def sendEmail(self, query):
        assistant.speak("Send email...") 
        query = query.replace("send", "")
        query = query.replace("email", "")
        query = query.strip()
        letter_term = send_a_letter(query)
        if "Error" not in letter_term:
            print(f"VA: {letter_term}!")
            assistant.speak(letter_term)
        else:
            assistant.speak("I don't understand what you say!")
    
    def repeat(self, query):
        assistant.speak(query)
        print("VA: I don't understand what you say!")
