# Before running, make sure to install ultralytics
##################################################
#           Machine learning results             #
##################################################

from ultralytics import YOLO
from tts import say
from sys import stdout

ped_model = YOLO('YOLOpedlight/yolov8l_custom.pt')
cross_model = YOLO('YOLOcrosswalk/yolov8n_custom.pt') #Uncomment this for crosswalk


# ped_result = ped_model.predict('YOLOpedlight/val/images/image71.jpg', save_txt=True)


# ped_result = ped_model.predict('stored_images/image.jpg', save_txt=True)
# print(ped_result)

# print(ped_result.boxs.conf)

# print(ped_result[0].boxes.conf, ped_result[0].boxes.cls)
# probability = ped_result[0].boxes.cls


# Results is a list, need to extract just the predicted value 1 (go) or 0 (stop)
# need to check the resulting value type
# Passing in a live feed from app.py?
# Live_feed can also be a directory
# Call the 'say()' function with go


# for these functions, returning None means no detection, false/true means negative/positive detection

def check_pedlight():
    ped_result = ped_model("stored_images/image.jpg") # Need to find location of the live feed
    probability_ped = ped_result[0].boxes.cls

    print(probability_ped, file=stdout)

    if(len(probability_ped) < 1):
        say("Adjust camera to locate sign")
        print("Adjust camera to locate sign")
        return None

    elif(probability_ped[0] == 1): # If sign shows go
        say("You can cross")
        print("You can cross")
        return True
    
    elif(probability_ped[0] == 0):
        say("Wait")
        print("Wait")
        return False
        
    return None


# Same as the previous code but for the crosswalk instead of the light
def check_crosswalk():
    cross_result = cross_model('YOLOcrosswalk/val/images/Test (177).jpg') # Need to find location of the live feed
    probability_cross = cross_result[0].boxes.cls

    print(probability_cross, file=stdout)

    # return True

    if(len(probability_cross) < 1):
        say("Find crosswalk")
        print("Find crosswalk")
        return None

    elif(probability_cross[0] >= 1): # If sign shows go
        say("Crosswalk found")
        print("Crosswalk found")
        return True
    
    elif(probability_cross[0] == 0):
        say("Find the crosswalk")
        print("Find the crosswalk")
        return None
        
    return None

