from djitellopy import tello
from Basics import ImageCaputer, KeyboardControl
from time import sleep

def init():
    global me
    global img
    me = tello.Tello()
    me.connect()
    me.get_battery()

    KeyboardControl.initKeyboardControl()

    me.streamon()
    print("hier")


if __name__ == '__main__':
    init()
    while True:
        ImageCaputer.getStream(me)
        values = KeyboardControl.getKeyboardInput(me)
        me.send_rc_control(values[0], values[1], values[2], values[3])