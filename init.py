import os
import eel
from engine.function import *
from engine.command import *

def assist():
    # Specify the directory containing the web interface files
    eel.init("www")

    playAssistantSound()

    # Launch virtual assistant on Microsoft Edge browser in app mode
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Use external browser and keep program running without ending
    eel.start("index.html", mode=None, host="localhost", block=True)
