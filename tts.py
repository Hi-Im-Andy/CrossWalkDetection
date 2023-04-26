
# Importing os to save and play the audio
import os

# Import google text to speech
from gtts import gTTS

# Import for backgound tasks, can be used to add delays, task be completed after the return
from celery import Celery

from flask import Flask

app = Flask(__name__)

# Create a celery instance
celery = Celery(app.name, broker='pyamqp://guest@localhost//')

# Set up configuration for celery
celery.conf.update(
    result_expires=3600,
)

# Main Text to speech function
@celery.task
def say(words):
    text = str(words)
    text_audio = gTTS(text)
    text_audio.save("speech.mp3")
    # os.system("start speech.mp3") # Windows
    os.system("mpg321 speech.mp3") # Linux 
