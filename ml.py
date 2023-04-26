from ultralytics import YOLO
from tts import say

ped_model = YOLO('YOLOpedlight/yolov8l_custom.pt')
# cross_model = YOLO('YOLOcrosswalk/yolov8l_custom.pt') #Uncomment this for crosswalk

ped_result = ped_model('YOLOpedlight/val/images/image71.jpg')
print(ped_result)


# Results is a list, need to extract just the predicted value 1 (go) or 0 (stop)
# need to check the resulting value type
# Passing in a live feed from app.py?
# Call the 'say()' function with go

def check_pedlight(live_feed):
    ped_result = ped_model(live_feed) # Need to find location of the live feed
    
    if(ped_result == 1): # If sign shows go
        say("You can cross")
    
    elif(ped_result == 0):
        say("Wait")

    else:
        say("Adjust camera to locate sign")


# Same as the previous code but for the crosswalk instead of the light
def check_crosswalk(live_feed):
    cross_result = cross_model(live_feed)

    if(cross_result == 1):
        say("This is a crosswalk.")
    else:
        say("No crosswalk detected.")

