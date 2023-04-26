###################################################
#                     Imports                     #
###################################################
# Generic imports
from flask import Flask, render_template, request, url_for, redirect, session
import base64
import cv2
import numpy as np

# For the session secret key
from os import urandom

# Text to speech funciton(s)
from tts import say

# Importing machine learning
from ml import check_pedlight, check_crosswalk


app = Flask(__name__)
# Set a secret_key to use session/login_manager
app.secret_key = urandom(12)


##################################################
#               Debugging functions              #
##################################################

from sys import stdout

# Since print needs to have the file specified to stdout just make a separate function to simplify debug calls
def p(*kwargs):
    print(kwargs, file=stdout)


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
    return render_template("off.html")


@app.route("/on")
def on():
    say("Camera on.")
    # check_pedlight.delay(live_feed)
    return render_template("on.html")


@app.route("/process_frame", methods=["POST"])
def process_frame():
    image = open("./stored_images/tmp.png", "wb")
    image.write(base64.b64decode(request.get_json()["image"]))
    image.close()
    return "Request completed"
