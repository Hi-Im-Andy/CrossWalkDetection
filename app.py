###################################################
#                     Imports                     #
###################################################
# Generic imports
from flask import Flask, render_template, request, url_for, redirect, session

# For the session secret key
from os import urandom
import os

# Import for backgound tasks
from celery import Celery

# Import for text to speech
from gtts import gTTS

# Import for sleep
import time

app = Flask(__name__)
# Set a secret_key to use session/login_manager
app.secret_key = urandom(12)

# create a celery instance
celery = Celery(app.name, broker='pyamqp://guest@localhost//')

# Set up configuration for celery
celery.conf.update(
    result_expires=3600,
)

##################################################
#               Debugging functions              #
##################################################

from sys import stdout
# Since print needs to have the file specified to stdout just make a separate function to simplify debug calls
def p(*kwargs):
    print(kwargs, file=stdout)


##################################################
#             Text to Speech Functions           #
##################################################

# Used for the actual text to speech
@celery.task
def say(words):
    text = str(words)
    text_audio = gTTS(text)
    text_audio.save("speech.mp3")
    # os.system("start speech.mp3") # Windows
    os.system("mpg321 speech.mp3") # Linux 

# Used to repeat the same words 
@celery.task
def repeat(words):
    while True:
        say(words)
        time.sleep(2)

# Stops background processes
def repeat_revoke():
    task_id = session.get('repeat_task_id')
    if task_id:
        celery.control.revoke(task_id, terminate=True)


###################################################
#                Route definitions                #
###################################################
# Just to avoid the favicon error, favicon.ico is an empty file
@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"))


@app.route("/")
def home():
    return redirect(url_for("off"))

@app.route("/off")
def off():
    say("Off.")
    repeat_revoke()
    return render_template("off.html")
    
@app.route("/on")
def on():
    say("Camera on.")
    repeat_task = repeat.delay("Face camera towards crosswalk sign.",) # Working on getting this to repeat the render_template
    session['repeat_task_id'] = repeat_task.id
    return render_template("on.html")