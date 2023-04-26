###################################################
#                     Imports                     #
###################################################
# Generic imports
from flask import Flask, render_template, request, url_for, redirect, session

# For the session secret key
from os import urandom

# Text to speech funciton(s)
from tts import say


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
    return render_template("on.html")