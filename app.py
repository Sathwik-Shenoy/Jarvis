from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import datetime
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app)

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# JARVIS responses
GREETINGS = [
    "At your service, sir.",
    "How may I assist you today?",
    "I'm here and ready to help.",
    "What can I do for you?",
    "I'm listening."
]

def get_time_based_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

def process_command(text):
    text = text.lower()
    
    # Time-based greeting
    if any(word in text for word in ['hello', 'hi', 'hey']):
        return f"{get_time_based_greeting()}, sir. {random.choice(GREETINGS)}"
    
    # Time query
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}, sir."
    
    # Date query
    elif 'date' in text:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today is {current_date}, sir."
    
    # Weather query (placeholder)
    elif 'weather' in text:
        return "I apologize, but I haven't been connected to the weather service yet, sir."
    
    # System status
    elif 'status' in text or 'how are you' in text:
        return "All systems are operational and running at peak efficiency, sir."
    
    # Default response
    else:
        return "I'm processing your request, sir. Please give me a moment to analyze the parameters."

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('voice_input')
def handle_voice_input(data):
    try:
        response = process_command(data['text'])
        emit('jarvis_response', {'text': response})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('text_input')
def handle_text_input(data):
    try:
        response = process_command(data['text'])
        emit('jarvis_response', {'text': response})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True) 