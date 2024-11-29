import eel
import time
from engine.assistant import VirtualAssistant
from engine.function import *

assistant = VirtualAssistant()
function = Function()

@eel.expose
def all_command(message=1):
    # Receive information from voice
    if message == 1:
        query = assistant.listen()
        print(query)
        eel.senderText(query)
    
    # Receive information from keyboard
    else:
        query = message
        eel.senderText(query)
    
    # All command
    try:
        if "hello" in query or "hi" in query:
            function.helloUser()
        elif "open" in query:
            function.openCommand(query)
        elif "google" in query and "search" in query:
            function.searchGoogle(query) 
        elif "wikipedia" in query:
            function.searchWiki(query)
        elif "translate" in query:
            function.translateVN(query)
        elif "youtube" in query:
            function.playYouTube(query)
        elif "weather" in query:
            function.announceWeather(query) 
        elif "time" in query:
            function.announceTime()
        elif "day" in query:
            function.announceDay()
        elif "screenshot" in query:
            function.takeScreenshot()
        elif "email" in query:
            function.sendEmail(query)
        else:
            function.repeat(query)
    except Exception as e:
        print("Error:", e)

    # Return main interface
    eel.Interface()
