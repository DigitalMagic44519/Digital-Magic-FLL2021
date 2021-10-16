#!/usr/bin/env pybricks-micropython

# ---------------------------------------------------------------
# This is our 2021 digital magic missions code
# Change log:
# 9-14-21 ecv started the progaming by copying an example
# 9-21-21 ipk was here learning while waiting on the engineers 
# 9-28-21 ipk added run1 function
# 9-28-21 ecv Worked with coach to test comands 
# 10-5-21 ecv Started run 1
# 10-12-21 kahk did more run 1 
# ---------------------------------------------------------------
 
# these are the libraries of code writen by pybricks
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Port, 
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.robotics import DriveBase

# < >
from menu import wait_for_button



# Initialize the EV3.
ev3 = EV3Brick()

# Initialize the motors.
am = Motor(Port.C)
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

# Initialize the drive base. ecv put in measurements 9/28 (9cm=90mm) (6cm=60mm)
robot = DriveBase(left_motor, right_motor, wheel_diameter=90, axle_track=60)

# ---------------------------------------------------------------
# This is the function for our first set of misions
# 1. Cargo Plane 
# 2. 
# ---------------------------------------------------------------

def run1():
    #turn the speed down a little from default
    #(209, 837, 400, 1600)
    robot.settings(109, 837, 400, 1600)

    #Drive over and aline to the wall
    robot.straight(1000)

    #Back up a little
    robot.straight(-225)

    #Turn toward engine 
    robot.turn(90)  

    # Lower the attachment
    am.run_time(speed=500,time=900)

    #Drive over to engine
    robot.straight(260)

    #Lift the attachment fliping motor
    am.run_time(speed=-500,time=900)

    #back it up
    robot.straight(-180)

    #turn to face the wall
    robot.turn(-90) 

    #go square up on wall
    robot.straight(220)

    #back up again 
    robot.straight(-180)

    #turn and face the plane
    robot.turn(-90)

    #drive to plane and flip it



    #ecv tried out these commands with coach, will copy from here
    #robot.straight(100)
    #robot.turn(90)   
    #robot.drive(50,10)
    #robot.settings(209, 837, 400, 1600)

    #ev3.speaker.beep(200)
    
    #mcMoveDistance=1300
    #am.run_time(speed=500,time=mcMoveDistance)
    #am.run_time(speed=-500,time=mcMoveDistance)
    
    #ev3.speaker.beep(800)
    #am.run_time(speed=1000,time=1000)
    #am.run_time(speed=-1000,time=1000)

    



# ---------------------------------------------------------------
# This is the button code from the example code
# ---------------------------------------------------------------

print (robot.settings())  #default = (209, 837, 400, 1600)

while True:
    # Show the menu and wait for one button to be selected.
    button = wait_for_button(ev3)

    # Now you can do something, based on which button was pressed.

    # In this demo, we just play a different sound for eachps -ef | grep  button.
    if button == Button.LEFT:
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

     

  