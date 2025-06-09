from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app)

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('voice_input')
def handle_voice_input(data):
    try:
        # Process voice input here
        response = "I heard you say: " + data['text']
        emit('jarvis_response', {'text': response})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('text_input')
def handle_text_input(data):
    try:
        # Process text input here
        response = "You said: " + data['text']
        emit('jarvis_response', {'text': response})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True) 