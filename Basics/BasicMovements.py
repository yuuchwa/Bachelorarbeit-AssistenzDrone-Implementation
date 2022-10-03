from djitellopy import tello
from time import sleep

tel = tello.Tello()
tel.connect()
print(tel.get_battery())

tel.send_rc_control(0,50,0,0)
sleep(1)
tel.send_rc_control(0,0,0,0)
tel.land()

