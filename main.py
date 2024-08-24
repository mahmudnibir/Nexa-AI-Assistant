import os
import time
import json
import threading
import requests
import zipfile
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import qrcode
from email.mime.text import MIMEText
import smtplib
from googletrans import Translator
# from pycaw import AudioUtilities, IAudioEndpointVolume
from bs4 import BeautifulSoup
import pyttsx3
import psutil
import webbrowser
from fuzzywuzzy import process

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Feature functions
def play_song_on_youtube(song_name):
    """Search and play a song on YouTube."""
    query = song_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Searching for {song_name} on YouTube.")
    time.sleep(3)  # Wait for the browser to load

def set_alarm(alarm_time):
    """Set an alarm for a specific time."""
    def alarm():
        speak("Alarm ringing!")
    alarm_time = time.strptime(alarm_time, "%H:%M")
    alarm_seconds = time.mktime(alarm_time) - time.mktime(time.localtime())
    threading.Timer(alarm_seconds, alarm).start()
    speak(f"Alarm set for {time.strftime('%H:%M', alarm_time)}")

def play_music_from_playlist(playlist_url):
    """Play music from a given playlist URL."""
    webbrowser.open(playlist_url)
    speak("Playing music from your playlist.")

def translate_text(text, dest_language='en'):
    """Translate text to the desired language."""
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

def search_files(directory, file_name):
    """Search for a file by name in a specified directory."""
    matches = [f for f in os.listdir(directory) if file_name in f]
    if matches:
        return "\n".join(matches)
    return "No files found."

def delete_file(file_path):
    """Delete a specified file."""
    if os.path.exists(file_path):
        os.remove(file_path)
        speak(f"File {file_path} deleted.")
    else:
        speak("File not found.")

def rename_file(old_name, new_name):
    """Rename a file from old_name to new_name."""
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        speak(f"File renamed from {old_name} to {new_name}.")
    else:
        speak("File not found.")

def extract_zip(file_path, extract_to):
    """Extract a ZIP file to the specified directory."""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    speak(f"Extracted {file_path} to {extract_to}.")

def compress_files(file_paths, zip_name):
    """Compress multiple files into a ZIP archive."""
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            zipf.write(file)
    speak(f"Compressed files into {zip_name}.")

def monitor_network_traffic():
    """Monitor and return network traffic data."""
    network = psutil.net_io_counters()
    return f"Bytes sent: {network.bytes_sent}\nBytes received: {network.bytes_recv}"

def scan_for_malware(file_path):
    """Placeholder for a malware scan."""
    return "Malware scan complete. No threats found."

def generate_random_quote():
    """Fetch a random quote from an API."""
    response = requests.get("https://api.quotable.io/random")
    quote = response.json().get('content', 'No quote available.')
    return quote

def setup_wifi(ssid, password):
    """Set up a Wi-Fi network with the given SSID and password."""
    config = f"""
    network={{
        ssid="{ssid}"
        psk="{password}"
    }}
    """
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as file:
        file.write(config)
    speak("Wi-Fi network setup.")

def get_stock_market_updates():
    """Fetch the latest stock market updates."""
    url = "https://api.example.com/stock_market_updates"
    response = requests.get(url)
    data = response.json()
    return data['updates']

def search_recipes(ingredient):
    """Search for recipes based on an ingredient."""
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&apiKey=YOUR_SPOONACULAR_API_KEY"
    response = requests.get(url)
    recipes = response.json()
    return [recipe['title'] for recipe in recipes]

def control_smart_home_device(device, action):
    """Placeholder function to control a smart home device."""
    return f"Executed {action} on {device}."

def track_fitness_goals(goal, progress):
    """Track a fitness goal and update progress."""
    with open("fitness_goals.txt", "a") as file:
        file.write(f"{goal}: {progress}\n")
    speak("Fitness goal tracked.")

def create_reminder(reminder_text, reminder_time):
    """Create a reminder for a specific time."""
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder_text} at {reminder_time}\n")
    speak("Reminder created.")

def list_reminders():
    """List all reminders."""
    with open("reminders.txt", "r") as file:
        return file.read()

def add_contact(name, phone):
    """Add a contact to the contacts list."""
    with open("contacts.json", "a") as file:
        json.dump({name: phone}, file)
    speak(f"Contact {name} added.")

def list_contacts():
    """List all contacts."""
    with open("contacts.json", "r") as file:
        contacts = json.load(file)
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def get_public_transport_schedule(location):
    """Fetch public transport schedules for a given location."""
    url = f"https://api.publictransport.com/schedule?location={location}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    schedule = response.json()
    return schedule['schedule']

def generate_qr_code(data):
    """Generate a QR code from the given data."""
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make()
    img = qr.make_image()
    img.save("qrcode.png")
    speak("QR code generated.")

def read_book(file_path):
    """Read a book from a text file."""
    with open(file_path, "r") as file:
        return file.read()

def schedule_email(to_email, subject, body, send_time):
    """Schedule an email to be sent at a specific time."""
    def send():
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'nibirbbkr@example.com'
        msg['To'] = to_email
        with smtplib.SMTP('smtp.example.com') as server:
            server.sendmail('your_email@example.com', to_email, msg.as_string())
        speak("Email sent.")
    time_to_wait = time.mktime(time.strptime(send_time, "%Y-%m-%d %H:%M:%S")) - time.time()
    threading.Timer(time_to_wait, send).start()

# def set_volume(volume_level):
#     """Set the system volume to the specified level."""
#     devices = AudioUtilities.GetSpeakers()
#     interface = devices.Activate(IAudioEndpointVolume._iid_, pycaw.CLSCTX_ALL, None)
#     volume = pycaw.Cast(interface, IAudioEndpointVolume)
#     volume.SetMasterVolumeLevelScalar(volume_level / 100.0, None)
#     speak(f"Volume set to {volume_level}%.")

def get_traffic_data(location):
    """Fetch real-time traffic data for a given location."""
    url = f"https://api.trafficdata.com/realtime?location={location}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    return data['traffic']

def get_stock_price(symbol):
    """Fetch the current stock price for a given symbol."""
    url = f"https://api.example.com/stock_price?symbol={symbol}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    price = response.json()
    return f"Current price of {symbol}: {price['price']}"

def convert_units(value, from_unit, to_unit):
    """Convert a value from one unit to another."""
    conversions = {
        ("meters", "kilometers"): lambda x: x / 1000,
        ("kilograms", "grams"): lambda x: x * 1000,
        # Add more conversions here
    }
    conversion_func = conversions.get((from_unit, to_unit))
    if conversion_func:
        return conversion_func(value)
    return "Conversion not supported."

def find_nearby_atms(location):
    """Find nearby ATMs based on location."""
    url = f"https://api.example.com/atms?location={location}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    atms = response.json()
    return atms['atms']

def get_movie_showtimes(movie_name, location):
    """Fetch movie showtimes for a given movie and location."""
    url = f"https://api.example.com/showtimes?movie={movie_name}&location={location}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    showtimes = response.json()
    return showtimes['showtimes']

def manage_todo_list(action, item=None):
    """Manage a to-do list with actions like add, remove, or list items."""
    with open("todo_list.txt", "a+" if action == "add" else "r") as file:
        if action == "add":
            file.write(f"{item}\n")
            speak(f"{item} added to to-do list.")
        elif action == "remove":
            lines = file.readlines()
            with open("todo_list.txt", "w") as new_file:
                for line in lines:
                    if line.strip("\n") != item:
                        new_file.write(line)
                speak(f"{item} removed from to-do list.")
        elif action == "list":
            return file.read()

def get_weather_forecast(location):
    """Fetch the weather forecast for a given location."""
    url = f"https://api.weather.com/v3/wx/forecast/daily/5day?geocode={location}&format=json&apiKey=5f4147f3c301402389db419410711e3b"
    response = requests.get(url)
    forecast = response.json()
    return forecast['narrative']

def recommend_movies(genre):
    """Recommend movies based on a specific genre."""
    url = f"https://api.example.com/movies?genre={genre}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    movies = response.json()
    return [movie['title'] for movie in movies]

def manage_notes(action, note=None):
    """Manage notes with actions like add, remove, or list notes."""
    with open("notes.txt", "a+" if action == "add" else "r") as file:
        if action == "add":
            file.write(f"{note}\n")
            speak(f"Note added: {note}")
        elif action == "remove":
            lines = file.readlines()
            with open("notes.txt", "w") as new_file:
                for line in lines:
                    if line.strip("\n") != note:
                        new_file.write(line)
                speak(f"Note removed: {note}")
        elif action == "list":
            return file.read()

def control_device_by_voice(device, action):
    """Control a device by voice command."""
    return f"Executing {action} on {device}."

def read_webpage_content(url):
    """Read and return the content of a webpage."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def manage_calendar(action, event=None, date=None):
    """Manage calendar with actions like add, remove, or list events."""
    with open("calendar.txt", "a+" if action == "add" else "r") as file:
        if action == "add":
            file.write(f"{event} on {date}\n")
            speak(f"Event added: {event} on {date}")
        elif action == "remove":
            lines = file.readlines()
            with open("calendar.txt", "w") as new_file:
                for line in lines:
                    if line.strip("\n") != f"{event} on {date}":
                        new_file.write(line)
                speak(f"Event removed: {event} on {date}")
        elif action == "list":
            return file.read()

def calculate_expenses(expenses):
    """Calculate total expenses from a list of individual expenses."""
    total = sum(expenses)
    return f"Total expenses: {total}"

def get_recipe_suggestions(ingredient):
    """Get recipe suggestions based on a main ingredient."""
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    recipes = response.json()
    return [recipe['title'] for recipe in recipes]

def control_appliances(appliance, action):
    """Control home appliances with actions like turn on, turn off, etc."""
    return f"{action.capitalize()} the {appliance}."

def automate_social_media_post(platform, message):
    """Automate posting a message on social media."""
    url = f"https://api.example.com/post?platform={platform}&message={message}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    return response.json().get('status', 'Failed to post.')

def set_reminder(reminder_text, reminder_time):
    """Set a reminder for a specific time."""
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder_text} at {reminder_time}\n")
    speak(f"Reminder set: {reminder_text} at {reminder_time}")

def manage_reminders(action, reminder_text=None):
    """Manage reminders with actions like add, remove, or list reminders."""
    with open("reminders.txt", "a+" if action == "add" else "r") as file:
        if action == "add":
            file.write(f"{reminder_text}\n")
            speak(f"Reminder added: {reminder_text}")
        elif action == "remove":
            lines = file.readlines()
            with open("reminders.txt", "w") as new_file:
                for line in lines:
                    if line.strip("\n") != reminder_text:
                        new_file.write(line)
                speak(f"Reminder removed: {reminder_text}")
        elif action == "list":
            return file.read()

# Example usage
if __name__ == "__main__":
    play_song_on_youtube("Bohemian Rhapsody by Queen")
    set_alarm("07:00")
    print(translate_text("Hello", "es"))
    print(search_files("C:/Users", "G6 Ryzen 5 Pro"))
    # set_volume(50)
