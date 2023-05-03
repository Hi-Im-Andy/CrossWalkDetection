###################################################
#                     Imports                     #
###################################################
# Generic imports
from flask import Flask, render_template, request, url_for, redirect, session
import base64

# For the session secret key
from os import urandom

# Text to speech funciton(s)
# from tts import say

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
    session["crosswalk_detected"] = False
    # say("Off.")
    return render_template("off.html")


@app.route("/on")
def on():
    session["crosswalk_detected"] = False
    # say("Camera on.")
    # live_feed(1)
    # check_pedlight.delay(live_feed)
    return render_template("on.html")


# @app.route("/process_frame", methods=["POST"])
# def process_frame():
#     image = open("./stored_images/image.jpg", "wb")
#     image.write(base64.b64decode(request.get_json()["image"]))
#     image.close()
#     check_pedlight()
#     return "Request completed"


# Uncomment below to run the crosswalk detecrtion THEN the light
@app.route("/process_frame", methods=["POST"])
def process_frame():
    # Open the file with the mode set to write bytes
    with open("./stored_images/image.jpg", "wb") as image:
        # The image data is encoded in base64, so get the image from the json,
        # decode it's data from base64 to bytes
        # then write those bytes to the image file
        image.write(base64.b64decode(request.get_json()["image"]))

    if(session["crosswalk_detected"]):
        check_light = check_pedlight()
        if(check_light == None):
            return "No light detected"
        elif(check_light == False):
            return "Not ready to cross"
        elif(check_light == True):
            return "You can cross"
    else:
        check_cross = check_crosswalk()
        if(check_cross == None):
            return "No crosswalk detected"
        elif(check_cross == True):
            session["crosswalk_detected"] = True
            return "Crosswalk detected"
        
    return "No detection"        