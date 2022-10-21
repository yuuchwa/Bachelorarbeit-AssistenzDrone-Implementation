import math
from djitellopy import tello
import numpy as np
import cv2
import pygame
from time import sleep


###### Mapping Parameters ######
F_SPEED = 117/10 # Forward Speed in cm/s (15cm/s)
A_SPEED = 360/10 # Angular Speed Degrees/s (50deg/s)
INTERVAL = 0.25

distance_interval = F_SPEED * INTERVAL
angular_interval = A_SPEED * INTERVAL

###### Keyboard Control CONSTANTS ##################

LEFT_KEY = "LEFT"
RIGHT_KEY = "RIGHT"
FORWARD_KEY = "UP"
BACKWARD_KEY = "DOWN"
UP_KEY = "w"
DOWN_KEY = "s"
ROTATE_LEFT_KEY = "a"
ROTATE_RIGHT_KEY = "d"
LAND_KEY = "l"
TAKE_OFF_KEY = "o"
HEIGHT_KEY = "h"

####################################################

def connectTello():
    global me
    me.connect()
    print(me.get_battery())

def initKeyboardControl():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def getKeyboardInput(me: tello):
    left_right, forward_backward, up_down, yield_velocity = 0, 0, 0, 0
    speed = 15
    angular_speed = 50
    global yaw, x_coordinate, y_coordinate, angle
    distance = 0

    if getKey(LEFT_KEY):
        left_right = -speed
        distance = distance_interval
        angle = -180
    elif getKey(RIGHT_KEY):
        left_right = speed
        distance = -distance_interval
        angle = 180

    if getKey(UP_KEY):
        up_down = speed
        distance = distance_interval
        angle = 270
    elif getKey(DOWN_KEY):
        up_down = -speed
        distance = -distance_interval
        angle = -90

    if getKey(FORWARD_KEY):
        forward_backward = speed

    elif getKey(BACKWARD_KEY):
        forward_backward = -speed

    if getKey(ROTATE_RIGHT_KEY):
        yield_velocity = angular_speed
        yaw += angular_interval

    elif getKey(ROTATE_LEFT_KEY):
        yield_velocity = -angular_speed
        yaw -= angular_interval

    if getKey(LAND_KEY): me.land()
    if getKey(TAKE_OFF_KEY): me.takeoff()

    if getKey(HEIGHT_KEY): print(me.query_height())

    sleep(INTERVAL)
    angle += yaw
    x_coordinate += int(distance * math.cos(math.radians(angle)))
    y_coordinate += int(distance * math.sin(math.radians(angle)))

    return [left_right, forward_backward, up_down, yield_velocity, x_coordinate, y_coordinate]


def getKey(keyName):
    is_pressed = False

    for eve in pygame.event.get(): pass

    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))

    if keyInput[myKey]:
        is_pressed = True

    pygame.display.update()

    return is_pressed

def draw_points(img, points):
    print(points[len(points)-1])
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.putText(img,
                f'({(points[-1][0] - 500)/100},{(points[-1][1] - 500)/100})m',
                (points[-1][0] + 10, points[-1][1] + 30),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255, 0, 255),
                1
                )

x_coordinate, y_coordinate = 500, 500
angle = 0
yaw = 0
me = tello.Tello()
# connectTello()
initKeyboardControl()
points = [(0, 0), (0, 0)]

while True:
    # ImageCaputer.getStream(me)
    values = getKeyboardInput(me)
    me.send_rc_control(values[0], values[1], values[2], values[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    point = (values[4], values[5])
    points.append(point)
    draw_points(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
