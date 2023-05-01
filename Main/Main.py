#   Order
#   Program starts when front end presses start
#       Imports
#       -   gtts Google text to speech
#       -   os Access to operating system
#       -   time In this case used to cause a delay
#   
#       Functions
#       -   say(direction) Converts text to speech
#       -   sign() Detects changes in the sign
#       -   skew() Determines the offset between where the person is and where the crosswalk is
#
#       Main
#       -   Loop while waiting for crosswalk to be detected
#       -   Let the user know the crosswalk has changed signs
#       -   Loop wo check where the use is in regards to the crosswalk and alert them
#   Program ends when fron end presses stop

from gtts import gTTS
import os
import time

# Functions 
def say(direction):
    text = str(direction)
    text_audio = gTTS(text)
    text_audio.save("speech.mp3")
    # os.system("start speech.mp3")
    os.system("mpg321 speech.mp3")

# Placeholder
def sign():
    return True
# Placeholder
def skew():
    return 1

# Main
while (sign() != True):
    say("Wait.")
    time.sleep(1)

say("Go.")

while (True):
    value = skew()
    if(value > 1):
        say("Turn right.")
    elif(value < -1):
        say("Turn left.")
    time.sleep(1)
