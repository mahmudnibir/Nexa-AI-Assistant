import pyttsx3
import speech_recognition as sr
import webbrowser
import json
import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import psutil
import random
import pytz
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import ctypes
import shutil

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize background scheduler
scheduler = BackgroundScheduler()

# User profiles for personalized learning
user_profiles = {}

# Interaction log path
log_path = 'logs/interactions.json'

def setup_voice():
    """Setup the voice for the text-to-speech engine."""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set to the desired female voice
    engine.setProperty('rate', 150)  # Adjust speech rate

setup_voice()

def load_conversations():
    """Load conversation responses from JSON."""
    try:
        with open('conversations.json', 'r', encoding='utf-8') as file:
            conversations = json.load(file)
            print(f"Loaded conversations: {conversations}")  # Debugging line
            return conversations
    except FileNotFoundError:
        return {}


def load_responses(filename):
    """Load responses from a text file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            responses = [line.strip() for line in file.readlines()]
        return responses
    except FileNotFoundError:
        return ["Hello! How can I assist you today?"]  # Fallback greeting

def save_conversations(conversations):
    """Save updated conversations to JSON."""
    with open('conversations.json', 'w', encoding='utf-8') as file:
        json.dump(conversations, file)

def log_interaction(user_id, command, response):
    """Log user interactions for learning."""
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "user_id": user_id,
        "command": command,
        "response": response
    }
    if not os.path.exists('logs'):
        os.makedirs('logs')
    with open(log_path, 'a') as log_file:
        log_file.write(json.dumps(log_entry) + '\n')

def update_user_profile(user_id, command, response):
    """Update user profile with personalized data."""
    if user_id not in user_profiles:
        user_profiles[user_id] = []
    user_profiles[user_id].append({"command": command, "response": response})

def personalize_response(user_id, command):
    """Tailor response based on user's past interactions."""
    if user_id in user_profiles:
        for entry in user_profiles[user_id]:
            if entry["command"] == command:
                return entry["response"]
    return None

def load_interaction_data():
    commands = []
    responses = []
    
    # Open the interactions.json file and read its contents line by line
    with open('logs/interactions.json', 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                print("Entry:", entry)  # Inspect the entry
                commands.append(entry['command'])
                responses.append(entry['response'])
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {e}")
            except KeyError as e:
                print(f"Missing key in entry: {e}")

    return commands, responses
def train_model():
    """Train a machine learning model on interaction data."""
    commands, responses = load_interaction_data()
    
    if len(commands) > 1:
        # Convert text data to numerical features using TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(commands)
        
        # Ensure responses are discrete labels
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(responses)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model, vectorizer
    else:
        print("Not enough data to train the model.")
        return None, None

# Train the model on startup
model, vectorizer = train_model()

def predict_command(command, model, vectorizer):
    """Predict the response for a given command using the trained model."""
    command_vectorized = vectorizer.transform([command])
    prediction = model.predict(command_vectorized)
    # Ensure the prediction maps to a response index correctly
    return prediction[0]  # Assuming the model returns a numeric label


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            response = random.choice([
                "Oops! I missed that. Can you repeat it, please?",
                "I’m having trouble hearing you. Can you say that once more?",
                "I didn’t get that. Can you try saying it differently?",
                "Sorry, I didn’t hear you clearly. Could you say it again?",
                "Hmm, I missed that. Could you try saying it once more?",
                "Looks like I didn’t get that. Can you repeat it?",
                "Oops, I didn’t quite hear you. Can you say that again?"
            ])
            speak(response)
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down. Check your network connection and try again.")
            return ""
        except sr.WaitTimeoutError:
            speak("Timeout exceeded. Please try again.")
            return ""

def set_alarm(alarm_time_str):
    """Set an alarm."""
    try:
        # Normalize time string by converting to lowercase and removing periods
        alarm_time_str = alarm_time_str.lower().replace('.', '').replace(' ', '')
        
        # Handle 24-hour and 12-hour formats
        if 'am' in alarm_time_str or 'pm' in alarm_time_str:
            alarm_time = datetime.datetime.strptime(alarm_time_str, "%I:%M%p")
        else:
            alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")

        now = datetime.datetime.now()
        alarm_time = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)
        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)

        timezone = "Asia/Dhaka"
        tz = pytz.timezone(timezone)
        alarm_time = tz.localize(alarm_time)

        print("Current time:", now)
        print("Scheduled alarm time:", alarm_time)

        def alarm_action():
            speak("Alarm ringing!")
        
        scheduler.add_job(alarm_action, 'date', run_date=alarm_time)
        print("Scheduler jobs:", scheduler.get_jobs())
        scheduler.start()
        print("Scheduler started.")
    
    except ValueError as e:
        speak("Sorry, I didn't understand the time format.")
        print(f"Error parsing time: {e}")

def play_media(query):
    """Play media based on search query."""
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

def search_google(query):
    """Search Google based on query."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def open_platform(platform):
    """Open specified social media platform."""
    urls = {
        'facebook': "https://www.facebook.com/",
        'instagram': "https://www.instagram.com/",
        'tiktok': "https://www.tiktok.com/"
    }
    url = urls.get(platform)
    if url:
        webbrowser.open(url)
    else:
        speak("Platform not recognized.")

def get_joke():
    """Fetch and return a joke."""
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = response.json()
    joke_text = f"{joke['setup']} - {joke['punchline']}"
    print(joke_text)
    return joke_text

def get_news():
    """Fetch and return the latest news headlines."""
    api_key = '048e68c2a5964bec980d23eaeb523fd7' 
    url = f"https://newsapi.org/v2/top-headlines?country=bd&apiKey={api_key}"
    response = requests.get(url)
    headlines = response.json().get('articles', [])
    return [article['title'] for article in headlines]

# Mapping of countries to their capital cities
with open('countries_capitals.json', 'r') as file:
    country_to_capital = json.load(file)

def get_weather_forecast(country):
    """Fetch the weather forecast for the capital of a given country."""
    api_key = "5f4147f3c301402389db419410711e3b"
    capital = country_to_capital.get(country)
    
    if not capital:
        return None

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={capital}&cnt=5&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        forecast = response.json()
        return [day['weather'][0]['description'] for day in forecast['list']]
    else:
        return None

def get_battery_status():
    """Return battery status."""
    battery = psutil.sensors_battery()
    return f"Battery percentage: {battery.percent}%, Plugged in: {battery.power_plugged}"

def get_storage_status():
    """Return storage status."""
    partitions = psutil.disk_partitions()
    status = ""
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        status += f"Drive {partition.device}: {usage.percent}% used, {usage.free // (2**30)} GB free\n"
    return status
def clear_recycle_bin():
    """Clear the recycle bin."""
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1)  # 1 is for emptying the bin without confirmation
        return "Recycle bin cleared."
    except Exception as e:
        return f"Failed to clear recycle bin: {e}"
def check_disk_usage():
    """Check disk usage."""
    total, used, free = shutil.disk_usage("/")
    return f"Total: {total // (2**30)} GB, Used: {used // (2**30)} GB, Free: {free // (2**30)} GB"


def handle_command(command):
    """Handle user command based on context and provide responses."""
    responses = load_responses('response.txt')
    
    print(f"Handling command: {command}")  # Debugging line

    # Here you could integrate the loaded conversations
    conversations = load_conversations()
    
    if "weather" in command:
        country = command.split("in")[-1].strip()
        forecast = get_weather_forecast(country)
        if forecast:
            response = f"Weather forecast for {country}: {', '.join(forecast)}"
        else:
            response = "Sorry, I couldn't fetch the weather forecast."
    elif "news" in command:
        headlines = get_news()
        response = "Here are the latest news headlines."
        for headline in headlines:
            response += f"\n{headline}"
    elif "recycle bin" in command:
        response = clear_recycle_bin()
    elif "disk storage" in command:
        response = check_disk_usage()
    elif "joke" in command:
        joke = get_joke()
        response = joke
    elif "play" in command:
        query = command.split("play")[-1].strip()
        play_media(query)
        response = f"Playing {query}."
    elif "search" in command:
        query = command.split("search")[-1].strip()
        search_google(query)
        response = f"Searching Google for {query}."
    elif "open" in command:
        platform = command.split("open")[-1].strip()
        open_platform(platform)
        response = f"Opening {platform}."
    elif "battery" in command:
        status = get_battery_status()
        response = status
    elif "storage" in command:
        status = get_storage_status()
        response = status
    else:
        # Check if model and vectorizer are available
        if model and vectorizer:
            prediction = predict_command(command, model, vectorizer)
            # Ensure prediction is within the range of the responses list
            if 0 <= prediction < len(responses):
                response = responses[prediction]
            else:
                response = "I'm not sure how to handle that command."
        else:
            # Use a default response if model is not available
            response = random.choice(responses)
    
    if response is None:
        response = "I'm not sure how to handle that command."

    speak(response)
    print(response)
    return response



def main():
    """Main function to continuously listen for commands."""
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command:
            user_id = "default_user"  # Modify for actual user identification
            response = personalize_response(user_id, command)
            if response:
                speak(response)
            else:
                handle_command(command)
                update_user_profile(user_id, command, response)
                log_interaction(user_id, command, response)

if __name__ == "__main__":
    main()
