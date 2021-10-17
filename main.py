#!/usr/bin/env pybricks-micropython

# ---------------------------------------------------------------
# This is our 2021 digital magic missions code
# Change log:
#  9-14-21 ecv  started the progaming by copying an example
#  9-21-21 ipk  was here learning while waiting on the engineers 
#  9-28-21 ipk  added run1 function
#  9-28-21 ecv  Worked with coach to test comands 
# 10-05-21 ecv  Started run 1
# 10-12-21 kahk added more to run 1
# 10-12-21 lmh  claw placement 
# 10-16-21 lmh  trying a new strategy for run 1 (run1b)
# 10-16-21 lmh  added line follow code from example
# 10-16-21 cjh  work with coach to pass loop value into line follow function
# 10-16-21 dlc  picked up where lily left off on run1b
# 10-17-21 kahk made the function for the forklift retrofitted from last year
# 10-17-21 ipk  added run2 function
# ---------------------------------------------------------------
 
# these are the libraries of code writen by pybricks
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color 
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# we got this code from the samples
from menu import wait_for_button


# Initialize the EV3.
ev3 = EV3Brick()

# Initialize the motors.
am = Motor(Port.C)
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S4)

# Initialize the drive base. ecv put in measurements 9/28 (9cm=90mm) (6cm=60mm)
robot = DriveBase(left_motor, right_motor, wheel_diameter=90, axle_track=60)

#***** OUR FUNCTIONS START HERE *****


# ---------------------------------------------------------------
# This is the function for run 2 plattooning trucks
#   
#    
# ---------------------------------------------------------------
def run2(): 
    #drive to line 
    robot.straight(150)

    #follow line over to other truck
    followline(250,75)
    ev3.speaker.beep(800)  #DEBUG

    #turn toward the other truck
    #robot.turn(200)
    #ev3.speaker.beep(800)  #DEBUG

    #drive forward and hook up
    #robot.straight(50)
    #ev3.speaker.beep(800)  #DEBUG

    # Set the drive base speed and turn rate.
    # robot.drive(speed, turn_rate)

    #turn toward the other truck
    robot.drive(speed=75, turn_rate=40)
    wait(2500)
    robot.straight(150)
    robot.stop()
    ev3.speaker.beep(800)  #DEBUG
    robot.straight(-1000)

# ---------------------------------------------------------------
# This is the function for the forklift retrofitted from last year
#   <comment about how distance determined>
#   <comment about speed> 
# ---------------------------------------------------------------
def forkliftmove(direction,time):
    speed=200000
    if direction == "down":
        speed = speed * -1


    am.run_time(speed,time)

# ---------------------------------------------------------------
# This is the function to follow line. from example
#   loop = how many times we loop = distance travelled
#   speed = how fast it follows the line
# ---------------------------------------------------------------
def followline(loop, speed):
    # Calculate the light threshold. Choose values based on your measurements.
    # all black and all white values can be read from brick
    BLACK = 9
    WHITE = 100
    threshold = (BLACK + WHITE) / 2

    # Set the drive speed at 100 millimeters per second.
    # DRIVE_SPEED = 100

    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drivebase to 1.2 degrees per second.

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.
    PROPORTIONAL_GAIN = .8

    
    

    # variable to store what loop we are on
    i=1

    # Start following the line endlessly.
    while i < loop:
        # print(i) - debug
        # Calculate the deviation from the threshold.
        deviation = line_sensor.reflection() - threshold

        # Calculate the turn rate.
        turn_rate = PROPORTIONAL_GAIN * deviation

        # Set the drive base speed and turn rate.
        robot.drive(speed, turn_rate)

        # You can wait for a short time or do other things in this loop.
        wait(10)
 
        #adding 1 to i
        i=i+1

    #stop and exit
    robot.stop()

# ---------------------------------------------------------------
# This is the function for our first set of misions
# 1. Flip Engine 
# 2. Cargo Plane
# ---------------------------------------------------------------

def run1b():
    #drive to line 
    robot.straight(280)

    #follow line over unused capacity
    followline(230,75)

    robot.stop()
    robot.settings(600, 837, 400, 1600)


    #hockey unused capacity off map
    robot.turn(-130)

    robot.stop()
    robot.settings(100, 837, 400, 1600)

    #turn robot back to line
    robot.turn(90)

     #follow line to just before it turns left
    followline(340,75)
    ev3.speaker.beep(800)  #DEBUG

    #drive strait ahead
    robot.straight(230)
    ev3.speaker.beep(800)  #DEBUG
    
    #drive towards motor
    robot.turn(45)
    robot.straight(20)

    # Lift the attachment fliping motor
    am.run_time(speed=-500,time=900)
    
    # back it up
    robot.straight(-180)

    # turn to face the wall
    robot.turn(-90) 

    # go square up on wall
    robot.straight(300)

    # back up again 
    robot.straight(-180)

    # turn and face the plane
    robot.turn(-90) 

    #lower arm to clear tail
    am.run_time(speed=500,time=500)
        
    #drive closer to plane
    robot.straight(20)
    
    #flip down plane door
    am.run_time(speed=500,time=400)
    
    #try to get over block 
    am.run_time(speed=-500,time=300)

    robot.turn(90)

    am.run_time(speed=700,time=300)

    robot.turn(-90)

# ---------------------------------------------------------------
# This is function for our first set of misions but with a different 
# strategy using line following. 
# 1. Flip Engine 
# 2. Cargo Plane
# ---------------------------------------------------------------

def run1():
    #turn the speed down a little from default
    #(209, 837, 400, 1600)
    robot.settings(109, 837, 400, 1600)

    # Drive over and aline to the wall
    robot.straight(1000)

    # Back up a little
    robot.straight(-250)

    # Turn toward engine 
    robot.turn(90)  

    # Lower the attachment
    am.run_time(speed=500,time=900)

    # Drive over to engine
    robot.straight(260)

    # Lift the attachment fliping motor
    am.run_time(speed=-500,time=900)

    # back it up
    robot.straight(-180)

    # turn to face the wall
    robot.turn(-90) 

    # go square up on wall
    robot.straight(220)

    # back up again 
    robot.straight(-180)

    # turn and face the plane
    robot.turn(-90)

    # drive to plane and flip it open



    #ecv learned & tried out these commands with coach, can copy from here
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

#print (robot.settings())  #default = (209, 837, 400, 1600)

while True:
    # Show the menu and wait for one button to be selected.
    button = wait_for_button(ev3)

    # Now you can do something, based on which button was pressed.

    # In this demo, we just play a different sound for eachps -ef | grep  button.
    if button == Button.LEFT:

        # using left button for calling run 1
        run1()
        
    elif button == Button.RIGHT:
        #do not use this button it sticks
        ev3.speaker.beep(600)

    elif button == Button.UP:
        run1b()

    elif button == Button.DOWN:
        ev3.speaker.beep(800)
        # test forklift 7000 is max range
        forkliftmove("up",7000)
        forkliftmove("down",7000)

    elif button == Button.CENTER:
        ev3.speaker.beep(1000)
        ev3.speaker.beep(800)
        ev3.speaker.beep(600)
        ev3.speaker.beep(1000)
        ev3.speaker.beep(800)
        ev3.speaker.beep(600)
        run2()

     

  