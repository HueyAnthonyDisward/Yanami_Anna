import os
import re
import struct
import time
import smtplib
import pvporcupine
import pyaudio
import requests
import pyautogui
import wikipedia
from datetime import datetime
from googletrans import Translator
from selenium import webdriver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extract_yt_term(text):
    # Define a regular expression pattern to capture the song name
    patterns = [
        r"play\s+(.*?)\s+on\s+youtube",
        r"find\s+(.*?)\s+on\s+youtube",
        r"show\s+(.*?)\s+on\s+youtube"
    ]

    # Use re.search to find the match in the comment
    # If a match is found, return the extracted song name; otherwise, return None
    try:
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        return f"Error: {e}"

def translate_to_vietnamese(text):
    translator = Translator()
    try:
        translation = translator.translate(text, src='en', dest='vi')
        return translation.text
    except Exception as e:
        return f"Error: {e}"

def information_from_wiki(text):    
    try:
        # Get the content of the Wikipedia article
        page = wikipedia.page(text)
        content = page.content[:]

        # Split the content into sentences and take the first 3
        lines = content.split('. ')[:3]

        # Remove newline characters from each sentence
        cleaned_lines = [line.replace('\n', ' ') for line in lines]

        list = []

        for sentence in cleaned_lines:
            if "." in sentence:
                sentence = sentence.split(". ")
                for text in sentence:
                    list.append(text)
            else:
                list.append(sentence)

        # The list of sentence      
        # print(list)
            
        # Join the cleaned sentences into a single string
        sentences = '. '.join(list[:3]) + '...'

        return sentences

    except Exception as e:
        return f"Error: {e}"

def open_google_and_search(text):
    # Set up and initialize ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open Google website
    driver.get("http://www.google.com")

    # Find the search input box
    que = driver.find_element(By.NAME, "q")

    # Enter the search query into the search box
    que.send_keys(text)

    # Press Enter to perform the search
    que.send_keys(Keys.RETURN)

    # Keep the browser open 1 minute after the search is performed
    time.sleep(60)

def get_weather_today(city):
    API_KEY = "b64d563220f54bfa8cd171045242611"
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    response = requests.get(url)
    try:
        if response.status_code == 200:
            data = response.json()
            location = data['location']['name']
            temp = data['current']['temp_c']
            condition = data['current']['condition']['text']
            return f"The weather in {location}: {temp}°C, {condition}."
        else:
            return "Error when to retrieve weather data."
    except Exception as e:
        return f"Error: {e}"

def capture_screenshot(save_path="screenshots"):
    # Create the storage directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Generate a file name based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"screenshot_{timestamp}.png"
    file_path = os.path.join(save_path, file_name)

    # Capture the screenshot
    time.sleep(3)
    screenshot = pyautogui.screenshot()

    # Save the image
    screenshot.save(file_path)

    return file_path

def send_a_letter(text):
    # Sender email information
    sender_email = "lhbaophuc0802@gmail.com"
    sender_password = "fopu pbze ondj szqe"

    # Receiver email information
    receiver_email = "aminbacon80@gmail.com"

    # Create email content
    subject = "Sent A Email"
    body = text

    # Create MIME email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the content to the email
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail server and send the email
    try:
        # Connect to Gmail server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        # Start TLS encryption
        server.starttls()  
        
        # Log in to Gmail account
        server.login(sender_email, sender_password) 

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        return "Email has been sent successfully!"
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Close the connection
        server.quit()

def hotword():
        porcupine = None
        paud = None
        audio_stream = None

        try:
            # Pre-Trained Keywords
            porcupine = pvporcupine.create(keywords=["VA", "AI"])
            paud = pyaudio.PyAudio()
            audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

            # Loop for streaming
            while True:
                keyword = audio_stream.read(porcupine.frame_length)
                keyword = struct.unpack_from("h"*porcupine.frame_length, keyword)

                # Processing keyword comes form mic
                keyword_index = porcupine.process(keyword)

                # Checking first keyword detected for not
                if keyword_index >= 0:
                    print("VA: Hotword detected!")

                    # Pressing shortcut key win + j
                    import pyautogui as autogui
                    autogui.keyDown("win")
                    autogui.press('j')
                    time.sleep(2)
                    autogui.keyUp("win")
        except:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if paud is not None:
                paud.terminate()
    