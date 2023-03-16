import cv2
import numpy as np


def imagePreProcess(image: np.ndarray) -> np.ndarray:
    # Convert the images color space
    # Maybe do a scan for bright yellow/white to highlight crosswalks instead of just a flat color transformation?
    return image


def getFrames(video: cv2.VideoCapture) -> "list[np.ndarray]":
    # Length of video in ms
    vidDuration = video.get(cv2.CAP_PROP_MSEC)
    # How many frames we want to scan per second
    fps = 2

    frames = []
    # Iterate up to the video duration in steps of 1000 (ms) / fps
    for timestamp in range(vidDuration, 1000 / fps):
        # Set the videos position to our calculated moment
        video.set(cv2.CAP_PROP_POS_MSEC, timestamp)
        # Read that moment, getting a return value indicating success/failure and the frame itself
        ret, frame = video.read()
        if ret:
            # Process the image before appending it to the list that we'll return
            frames.append(imagePreProcess(frame))
    return frames


# Runs detection on an image, in this case a frame from the video, and returns
# a string describing whether the user is centered, to the left, or to the right
#
# Syntax:
# 	direction = detection(frame, classes, weights, config)
#
# Input:
# 	frame = the image itself, opencv represents these as a numpy ndarray so the type should be np.ndarray
#   classes = a list of strings, where each string is a class name (for detection)
#   weights = the path to the file with the weights
#   config = the path to the file with the config
#
# Output:
# 	direction = A string describing which way to face
def detection(
    frame: np.ndarray, classes: "list[str]", weights: str, config: str
) -> str:
    w, h = frame.shape
    scale = 0.00392

    # generate different colors for different classes
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    # read pre-trained model and config file
    net = cv2.dnn.readNet(weights, config)

    # TODO based on https://towardsdatascience.com/yolo-object-detection-with-opencv-and-python-21e50ac599e9
    # should check what changing the constants there do
    # the (416, 416) is the size/shape for the output image
    # the (0,0,0) is the mean, or a scalar with mean values which are subtracted from channels. Seems like an offset?
    # create input blob
    blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)

    # set input blob for the network
    net.setInput(blob)

    # run the NN on the blob
    # returns an array of boxes (a list of lists [x,y,w,h] where (x,y) are top left coordinate and w/h are width/height)
    # and other data the nms will use

    # run non max suppression on results
    # returns an array of indices telling us which boxes in our array from the last step we actually want to use

    # Determine whether that box is centered, and thus whether the user seems to be staying in the crosswalk or headed off
    # Maybe compare width/height of the box to see if they seem to be walking straight? If in
    #   portrait mode, we'd expect the crosswalk to be tall and skinny, if it's too wide they're probably facing the wrong way


def main():
    pass
    # Pass video to getFrames

    # Pass frames to image detection

    # Give user feedback based on result of image detection


if __name__ == "__main__":
    main()
