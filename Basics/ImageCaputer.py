from djitellopy import tello
from time import sleep
import cv2


def initImageCapture(me: tello):
    return


def getStream(me: tello):
    img = me.get_frame_read().frame
    cv2.imshow("Image", img)
    cv2.waitKey(1)  # Delay to see the Frame
