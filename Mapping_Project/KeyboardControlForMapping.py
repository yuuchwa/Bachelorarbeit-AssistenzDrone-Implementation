from djitellopy import tello
import pygame

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

def initKeyboardControl():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def getKeyboardInput(me: tello):
    left_right, forward_backward, up_down, yield_velocity = 0, 0, 0, 0
    speed = 50
    distance = 0

    if getKey(LEFT_KEY):
        left_right = -speed
    elif getKey(RIGHT_KEY):
        left_right = speed

    if getKey(FORWARD_KEY):
        forward_backward = speed
    elif getKey(BACKWARD_KEY):
        forward_backward = -speed

    if getKey(UP_KEY):
        up_down = speed
    elif getKey(DOWN_KEY):
        up_down = -speed

    if getKey(ROTATE_RIGHT_KEY):
        yield_velocity = speed
    elif getKey(ROTATE_LEFT_KEY):
        yield_velocity = -speed

    if getKey(LAND_KEY): me.land()
    if getKey(TAKE_OFF_KEY): me.takeoff()

    if getKey(HEIGHT_KEY): print(me.query_height())

    return [left_right, forward_backward, up_down, yield_velocity]


def getKey(keyName):
    is_pressed = False

    for eve in pygame.event.get(): pass

    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))

    if keyInput[myKey]:
        is_pressed = True

    pygame.display.update()

    return is_pressed
