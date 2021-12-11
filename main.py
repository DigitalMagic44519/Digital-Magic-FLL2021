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
# 10-17-21 ipk  added plattooningtrucks function
# 10-19-21 ipk  added back up to plattooningtrucks to get unused cpacity
# 10-26-21 ipk  more work on perfecting plattooningtrucks and run1b
# 10-30-21 bgb  worked on run1b
# 11-03-21 kahk created a cargo plane mission only function
# 11-09-21 ipk  created a flip engine mission only function
# 11-09-21 ipk  a reusable function for changing straight speed and acceleration
# 12-05-21 ipk  created a connect cargo mission function
# 12-05-21 ipk  created innovation model mission function
# 12-05-21 ipk  changed button picture
# 12-05-21 kahk worked more on innovation model mission
# 12-05-21 lmh  worked more on innovation model mission
# 12-05-21 ipk  created package dispenser reusable function
# 12-06-21 kahk worked more tweaking innovation model mission
# 12-10-21 ipk  tweaks for clean wheels
# ---------------------------------------------------------------
 

# ---------------------------------------------------------------
# Initialization section
#  Mostly from example code
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

# ipk did creating and Initialize variables for speed and acceleration
#(209, 837, 400, 1600)
straight_speed = 209
straight_acceleration = 837 #837
turn_rate = 400
turn_acceleration = 1600

# ---------------------------------------------------------------
# These are our reusable functions Ian will explain
# ------------------------------------------------------------

# ---------------------------------------------------------------
# This is the function for changing the straight drive speed
#  Example: straightspeed(100) to change speed to 100 mm/second
# ---------------------------------------------------------------
def straightspeed(speed):
    straight_speed = speed
    robot.stop()
    robot.settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration) 
    
# ---------------------------------------------------------------
# This is the function for the forklift retrofitted from last year
# ---------------------------------------------------------------
def forkliftmove(direction,time):
    speed=200000
    if direction == "down":
        speed = speed * -1


    am.run_time(speed,time)

# ---------------------------------------------------------------
# This is the reusable function for the package dispenser
# ---------------------------------------------------------------
def packagedispenser():
    am.run_time(-2000,700)# speed and time, negative is dispense
    am.run_time(2000,700)# speed and time, positive is reset

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

    #PROPORTIONAL_GAIN = 1.2
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



#***** OUR MISSION FUNCTIONS START HERE *****
# ---------------------------------------------------------------
# This is a simplified function from the old run1b() that just does
# Flip Engine 
#
# ---------------------------------------------------------------
def flipengine():


    #set the speed
    straightspeed(109)


    #drive to line 
    robot.straight(280)


    #follow line (until right before the sharp turn)
    followline(550,75)

    robot.stop()
    
    ev3.speaker.beep(800)  #DEBUG
    # wait(5000) #DEBUG

    #drive strait ahead
    robot.straight(210)
    
    ev3.speaker.beep(800)  #DEBUG
    # wait(5000) #DEBUGThis is the function for changing the straight drive speed
    robot.turn(60)
    #robot.straight(15)

    # Lift the attachment fliping motor
    am.run_time(speed=-500,time=1700)
    


    #bring it on home 
    #turn the speed up 
    straightspeed(500)
    robot.straight(-800)


# ---------------------------------------------------------------
# way more simple cargo plane only function
# ---------------------------------------------------------------
def cargoplane():

    #position the attachment arm
    am.run_time(speed=250,time=900)

    #must stop to change speed
    robot.stop()

    #set the speed
    straightspeed(109)


    #drive to line 
    robot.straight(680)
    ev3.speaker.beep(800)  
    
    #bring da hammer down slightly
    am.run_time(speed=1500,time=1200)

    #must stop to change speed
    robot.stop()

    #drive home fast
    straightspeed(500)
    robot.straight(-750)


# ---------------------------------------------------------------
# This is the function for plattooning trucks  
# ---------------------------------------------------------------
def plattooningtrucks(): 

    #set the speed
    straightspeed(109)

    #drive to line 
    robot.straight(150)

    #follow line over to other truck
    followline(300,75) #260
    ev3.speaker.beep(800)  #DEBUG

    #turn toward the other truck.  The wait is how long it turns
    #robot.drive(speed=75, turn_rate=40)
    robot.drive(speed=75, turn_rate=30)
    wait(1400) #2400
    ev3.speaker.beep(800)  #DEBUG

    #push the truck onto the latch
    robot.straight(150)

    #back up to push unused capacity - the wait is how long it turns
    robot.drive(speed=-1000, turn_rate=30)
    wait(1200)
    robot.straight(-300)
    robot.stop()

# ---------------------------------------------------------------
# This is the function for connect cargo   
# ---------------------------------------------------------------
def connectcargo(): 

    #set the speed
    straightspeed(200)

    #drive to circle 
    robot.straight(620)

    #drive back 
    robot.straight(-700)

# ---------------------------------------------------------------
# This is the function for delivering innovation model  
# ---------------------------------------------------------------
def innovationmodel(): 

    #set the speed
    straightspeed(130)

    #set the speed
    straightspeed(150)

    #drive to circle 
    robot.straight(1130)

    #turn towards circle
    #robot.turn(-50) #12-5-21 lmh
    robot.turn(-100)  #12-6-21 -kahk

    #drive forward a litttle bit # 
    robot.straight(30)  #12-6-21 -kahk

    #drive back a tiny bit dropping drone box
    #robot.straight(-70) #12-5-21 -lmh
    robot.straight(-100)  #12-6-21 -kahk

    #turn toward door
    #robot.turn(160) #12-5-21 -lmh
    robot.turn(190)  #12-6-21 -kahk 220 190

    #drive toward door
    robot.straight(380)

    #turn back toward door #12-6-21 -kahk
    robot.turn(-50)  

    #drive toward door
    robot.straight(100)

    #deliver package
    packagedispenser()

    #drive back a tiny bit
    robot.straight(-70)


# ---------------------------------------------------------------
# This is function for our first set of misions 
# 1. Flip Engine 
# 2. Cargo Plane
# ---------------------------------------------------------------
def run1():
    #turn the speed down a little from default
    straightspeed(100)

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
# This is function for our first set of misions but with a different 
# strategy using line following.
# 1. Flip Engine 
# 2. Cargo Plane
# ---------------------------------------------------------------
def run1b():

    robot.stop()
    #turn the speed down a little from default
    straightspeed(100)

    #drive to line 
    robot.straight(280)


    #follow line (until right before the sharp turn)
    followline(550,75)

    robot.stop()
    
    ev3.speaker.beep(800)  #DEBUG
    # wait(5000) #DEBUG

    #drive strait ahead
    robot.straight(210)
    
    ev3.speaker.beep(800)  #DEBUG
    # wait(5000) #DEBUG

    
    #drive towards motor
    robot.turn(60)
    #robot.straight(15)

    # Lift the attachment fliping motor
    am.run_time(speed=-500,time=1700)
    
    # back it up
    robot.straight(-170)

    # turn to face the wall
    robot.turn(-90) 

    # go square up on wall
    robot.turn(-45)
    robot.straight(800)

    # back up again 
    robot.straight(-180)

    # turn and face the plane
    robot.turn(-105) 

    #lower arm to clear tail
    #I made the chenge so this is no longer needed-Brayden
    #am.run_time(speed=500,time=500)
        
    #drive closer to plane
    robot.straight(20)
    
    #flip down plane door
    am.run_time(speed=500,time=1100)
    
    #try to get over block 
    am.run_time(speed=-500,time=500)

    robot.turn(90)

    am.run_time(speed=500,time=500)

    robot.turn(-90)


# ---------------------------------------------------------------
# This is the function for our first set of misions using line 
# following and forklift
# 1. Flip Engine 
# 2. Cargo Plane
# ---------------------------------------------------------------
def run1c():
    # ev3.speaker.beep(800)
    # test forklift 7000 is max range
    # forkliftmove("up",7000)
    # forkliftmove("down",7000)

    robot.stop()
    #turn the speed down a little from default of (209, 837, 400, 1600)
    straightspeed(100)

    #drive to line 
    robot.straight(280)

    followline(570,75)

    robot.stop()

    #drive strait ahead
    robot.straight(230)
    ev3.speaker.beep(800)  #DEBUG
    
    #drive towards motor
    #robot.turn(60)
    #robot.straight(20)

    # Lift the attachment fliping motor
    #am.run_time(speed=-500,time=900)
    
    # back it up
    #robot.straight(-180)

    # turn to face the wall
    #robot.turn(-90) 

    # go square up on wall
    #robot.straight(400)

    # back up again 
    #robot.straight(-180)

    # turn and face the plane
    #robot.turn(-90) 

    #lower arm to clear tail
    #am.run_time(speed=500,time=500)
        
    #drive closer to plane
    #robot.straight(20)
    
    #flip down plane door
    #am.run_time(speed=500,time=400)
    
    #try to get over block 
    #am.run_time(speed=-500,time=300)

    #robot.turn(90)
    #am.run_time(speed=700,time=300)

    #robot.turn(-90)

  
# ---------------------------------------------------------------
# This is the button code from the example code
# ---------------------------------------------------------------

#print (robot.settings())  #default = (209, 837, 400, 1600)

while True:
    # Show the menu and wait for one button to be selected.
    button = wait_for_button(ev3)

    # Now you can do something, based on which button was pressed.

    if button == Button.LEFT:
        cargoplane()
        
    elif button == Button.RIGHT:
        #this is the button that sticks
        connectcargo()

    elif button == Button.UP:
        flipengine()

    elif button == Button.DOWN:
        innovationmodel()
        #packagedispenser()  #this an example of how we tested our code using reusable functions
        

    elif button == Button.CENTER:
        plattooningtrucks()
