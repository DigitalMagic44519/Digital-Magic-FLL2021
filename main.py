#!/usr/bin/env pybricks-micropython

# ---------------------------------------------------------------
# This is our 2021 digital magic missions code
# Change log:
# 9-14-21 ecv started the progaming by coping an example
# 9-21-21 ipk was here learning while waiting on the engineers
# 
# ---------------------------------------------------------------
 
# these are the libraries of code writen by pybricks
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Port, 
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.robotics import DriveBase
from menu import wait_for_button



# Initialize the EV3.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=60, axle_track=90)

# ---------------------------------------------------------------
# This is the function for our first misions
# 1. Cargo Plane
# 2. 
# ---------------------------------------------------------------

def run1():
    ev3.speaker.beep(200)
    ev3.speaker.beep(400)

# 
while True:
    # Show the menu and wait for one button to be selected.
    button = wait_for_button(ev3)

    # Now you can do something, based on which button was pressed.

    # In this demo, we just play a different sound for eachps -ef | grep  button.
    if button == Button.LEFT:
        run1()
        run1()
    elif button == Button.RIGHT:
        ev3.speaker.beep(400)
    elif button == Button.UP:
        ev3.speaker.beep(600)
    elif button == Button.DOWN:
        ev3.speaker.beep(800)
    elif button == Button.CENTER:
        ev3.speaker.beep(1000)
        ev3.speaker.beep(800)
        ev3.speaker.beep(600)
        ev3.speaker.beep(1000)
        ev3.speaker.beep(800)
        ev3.speaker.beep(600)

     

  