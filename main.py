#!/usr/bin/env pybricks-micropython

# ---------------------------------------------------------------
# This is our 2021 digital magic missions code
# Change log:
#
# ********* REGIONALS *********
#  9-14-21 ecv  started the progaming by copying an example
#  9-21-21 ipk  was here learning while waiting on the engineers 
#  9-28-21 ipk  added run1 function
#  9-28-21 ecv  Worked with coach to test comands 
# 10-05-21 ecv  Started run1
# 10-12-21 kahk added more to run1
# 10-12-21 lmh  claw placement 
# 10-16-21 lmh  trying a new strategy for run1 (run1b)
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
# ********* STATE *********
# 12-17-21 kahk fixed the runs after making slight adjustments to the wheels
# 12-18-21 ipk  added gyro code and trying it on platooning trucks
# 01-02-22 ipk  changed menu system for more items
# 
# clean up comments and add watch values function?
# 
# ---------------------------------------------------------------
 
# ---------------------------------------------------------------
# Initialization section
#  Mostly from example code
# ---------------------------------------------------------------

# these are the libraries of code writen by pybricks (API)
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color 
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# we got and Ian changed this code from the samples
from menu import wait_for_button
from menu import make_screen

# Initialize the EV3.
ev3 = EV3Brick()

# Initialize the motors.
am = Motor(Port.C)
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

# Initialize the sensors
line_sensor = ColorSensor(Port.S2)
line_sensor2 = ColorSensor(Port.S4)
gyro_sensor = GyroSensor(Port.S3, Direction.CLOCKWISE)

# Initialize the drive base. ecv put in measurements 9/28 kahk chg 12/17 (9cm=90mm) (8.8cm=88mm)
robot = DriveBase(left_motor, right_motor, wheel_diameter=90, axle_track=88)

# ipk did creating and Initialize variables for speed and acceleration
# (209, 837, 400, 1600)
straight_speed = 209
straight_acceleration = 837 #837
turn_rate = 50 #400 
turn_acceleration = 1600

# menu variables by Ian
run_number = 0
last_run_number = 6 

# ---------------------------------------------------------------
# These are our reusable functions Ian will explain
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# This is the function for turning with the gyro sensor
# Shared from FLL Team 50697 Pigeons of London, Ontario
# https://github.com/fll-pigeons/gamechangers/blob/master/programs/1_benchbocciabasket.py
# ---------------------------------------------------------------

def gyro_turn(angle, speed=150):
    gyro_sensor.reset_angle(0)
    print("initial " + str(angle))
    if angle < 0:
        while gyro_sensor.angle() > angle:
            left_motor.run(speed=(-1 * speed))
            right_motor.run(speed=speed)
            wait(10)
    elif angle > 0:  
        while gyro_sensor.angle() < angle:
            left_motor.run(speed=speed)
            right_motor.run(speed=(-1 * speed))
            wait(10)
            print(gyro_sensor.angle())  
    else:
        print("Error: no angle chosen")

    left_motor.brake()
    right_motor.brake()

# ---------------------------------------------------------------
# This is the function for driving straight with the gyro sensor
# Shared from FLL Team 50697 Pigeons of London, Ontario
# https://github.com/fll-pigeons/gamechangers/blob/master/programs/1_benchbocciabasket.py
# ---------------------------------------------------------------
def gyro_straight(distance, robotSpeed=150):
    robot.reset() 
    gyro_sensor.reset_angle(0)
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)

    #PROPORTIONAL_GAIN = 1.1 #Pigeons
    PROPORTIONAL_GAIN = 3.0
    if distance < 0: # move backwards
        while robot.distance() > distance:
            reverseSpeed = -1 * robotSpeed        
            angle_correction = -1 * PROPORTIONAL_GAIN * gyro_sensor.angle()
            print("Gyro Reading:", gyro_sensor.angle(),"Angle Correction:", angle_correction, "Left Motor Turns:", left_motor.angle(), "Right Motor Turns:", right_motor.angle())
            robot.drive(reverseSpeed, angle_correction)
            wait(10)
    elif distance > 0: # move forwards             
        while robot.distance() < distance:
            angle_correction = -1 * PROPORTIONAL_GAIN * gyro_sensor.angle()
            print("Gyro Reading:", gyro_sensor.angle(),"Angle Correction:", angle_correction, "Left Motor Turns:", left_motor.angle(), "Right Motor Turns:", right_motor.angle())
            robot.drive(robotSpeed, angle_correction) 
            wait(10)            
    robot.stop()

# ---------------------------------------------------------------
# This is the reusable function for changing the straight drive speed
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
    PROPORTIONAL_GAIN = 1.0
    #PROPORTIONAL_GAIN = .8

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
# This is a simplified function from old run_number1b() that just does Flip Engine 
# ---------------------------------------------------------------
def flip_engine():

    #set the speed
    straightspeed(109)

    #drive to line 
    robot.straight(280)

    #follow line (until right before the sharp turn)
    followline(550,75)
    robot.stop()
    
    #drive strait ahead then to motor
    robot.straight(210)
    robot.turn(48)
    robot.straight(55)

    # Lift the attachment fliping moto(speed=-500,time=1700)
    
    #bring it on home fast
    robot.turn(-50)
    straightspeed(500)
    robot.straight(-800)

# ---------------------------------------------------------------
# way more simple cargo plane only function
# ---------------------------------------------------------------
def cargo_plane():

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
def plattooning_trucks(): 

    #set the speed
    straightspeed(109)

    #drive to line and follow it awhile
    robot.straight(150)
    followline(200,75) 
    ev3.speaker.beep(200)  # DEBUG BEEP 1

    #turn toward the other truck.  The wait is how long it turns
    robot.drive(speed=75, turn_rate=20)
    wait(1500) #2400 ipk
    ev3.speaker.beep(400)  #DEBUG BEEP 2

    #turn less toward the other truck.  The wait is how long it turns
    robot.drive(speed=75, turn_rate=1)
    wait(1200) #2400 ipk
    ev3.speaker.beep(600)  #DEBUG BEEP 3

    #push the truck onto the latch
    straightspeed(75)
    robot.straight(120)
    ev3.speaker.beep(800)  #DEBUG BEEP 4

    #back up to push unused capacity - the wait is how long it turns
    robot.drive(speed=-1000, turn_rate=20)
    wait(1200)
    robot.straight(-300)
    robot.stop()

# ---------------------------------------------------------------
# This is 2nd version of the function for plattooning trucks  
# ---------------------------------------------------------------
def plattooning_trucks2(): 

    #drive straight out and turn toward other truck and then straight again to latch
    print("Drive North")

    #gyro_straight(500, robotSpeed=150)
    robot.straight(500)

    print("Turn East")
    gyro_turn(88, speed=150)

    print("Drive East")
    #gyro_straight(400, robotSpeed=80)
    robot.straight(400)

# ---------------------------------------------------------------
# This is the function for connect cargo   
# ---------------------------------------------------------------
def connect_cargo(): 

    #set the speed
    straightspeed(200)

    #drive to circle 
    robot.straight(620)

    #drive back 
    robot.straight(-700)

# ---------------------------------------------------------------
# This is the function for delivering innovation model  
# ---------------------------------------------------------------
def innovation_model(): 

    #set the speed
    straightspeed(130)

    #drive to circle 
    robot.straight(1130)

    #turn towards circle
    ## COACH THINKS NEED A TURN SPEED SETTER HERE HE MESSED WITH VARIABLE
    #robot.turn(-50) #12-5-21 lmh
    #robot.turn(-90)  #12-6-21 -kahk
    robot.turn(-65)  ##NEED COMMENT

    #drive forward a litttle bit # 
    robot.straight(35)  #12-6-21 -kahk

    #drive back a tiny bit 
    #robot.straight(-70) #12-5-21 -lmh
    robot.straight(-100)  #12-6-21 -kahk

    #turn toward door
    #robot.turn(140) #12-5-21 -lmh
    #robot.turn(190)  #12-6-21 -kahk ipk 220 190
    robot.turn(90) ## NEED COMMENT

    #drive toward door
    robot.straight(380)

    #turn back toward door #12-6-21 -kahk
    robot.turn(-40)  

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

    # Lower the attachmen(speed=500,time=900)

    # Drive over to engine
    robot.straight(260)

    # Lift the attachment fliping moto(speed=-500,time=900)

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

    # Lift the attachment fliping moto(speed=-500,time=1700)
    
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
    #I made the chenge so this is no longer needed-Brayden(speed=500,time=500)
        
    #drive closer to plane
    robot.straight(20)
    
    #flip down plane doo(speed=500,time=1100)
    
    #try to get over block(speed=-500,time=500)

    robot.turn(90)(speed=500,time=500)

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

    # Lift the attachment fliping motor(speed=-500,time=900)
    
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

    #lower arm to clear tail(speed=500,time=500)
        
    #drive closer to plane
    #robot.straight(20)
    
    #flip down plane door(speed=500,time=400)
    
    #try to get over block (speed=-500,time=300)

    #robot.turn(90)(speed=700,time=300)

    #robot.turn(-90)

def watch_sensors():
    wait(1000)
    gyro_sensor.reset_angle(0)
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)


    while (ev3.buttons.pressed() == []):
        ev3.screen.clear()
        ev3.screen.draw_text(1, 1, "Gyro:")
        ev3.screen.draw_text(100, 1, gyro_sensor.angle())
        ev3.screen.draw_text(1, 20, "R Line:")
        ev3.screen.draw_text(100, 20, line_sensor.reflection())
        ev3.screen.draw_text(1, 40, "L Line:")
        ev3.screen.draw_text(100, 40, line_sensor2.reflection())
        ev3.screen.draw_text(1, 60, "R Motor:")
        ev3.screen.draw_text(100, 60, right_motor.angle())
        ev3.screen.draw_text(1, 80, "L Motor:")
        ev3.screen.draw_text(100, 80, left_motor.angle())
        ev3.screen.draw_text(1, 100, "V (8231):")
        ev3.screen.draw_text(100, 100, ev3.battery.voltage())
        wait(100)
    
    # Now wait for the button to be released, from example code.  If you don't do this, the button that ends it executes next loop.
    while any(ev3.buttons.pressed()):
        pass


# ---------------------------------------------------------------
# This is the menu system (changed from the example code)
# ---------------------------------------------------------------

ev3.speaker.beep(100)
ev3.speaker.beep(900)
ev3.speaker.beep(100)
ev3.speaker.beep(900)

while True:
    # Draw screen based on what run we are on
    if run_number == 0:
        make_screen(ev3,"Check Sensors", " +  -  -  -  -  -  -",  "White 90-100", "Black 0 - 10","You Got This!","Go Magic!")

    elif run_number == 1:
        make_screen(ev3,"Platooning Trucks", " -  +  -  -  -  -  -", "Load Truck", "Catch Line Right","Check Boundry","Returns Hot")

    elif run_number == 2:
        make_screen(ev3,"Flip Engine", " -  -  +  -  -  -  -", "Catch Line Right", "Fill Blue","Pray for Turn","Returns Hot")

    elif run_number == 3:
        make_screen(ev3,"Cargo Plane", " -  -  -  +  -  -  -", "Aim for Bar", "Jump Up n Down","Let's Go!","Returns Hot")

    elif run_number == 4:
        make_screen(ev3,"Deliver Cargo", " -  -  -  -  +  -  -", "Aim for Circle", "Dance","Cheer","Returns Hot")

    elif run_number == 5:
        make_screen(ev3,"Innovation Model", " -  -  -  -  -  +  -", "Package!", "Just in Bounds","Three Sides","Rescue?")
    
    elif run_number == 6:
        make_screen(ev3,"Something New"," -  -  -  -  -  -  + ","Menu Code", "Looping!","Anyone?","Anyone?")

    # Wait for one button to be selected.
    button = wait_for_button(ev3)

    # Now you can do something, based on which button was pressed.
    if button == Button.LEFT:
        if run_number > 0: 
            run_number = run_number - 1
        else:
            run_number = last_run_number

    elif button == Button.RIGHT:
        if run_number < last_run_number: 
            run_number = run_number + 1
        else:
            run_number = 0

    elif button == Button.UP:
        if run_number > 0: 
            run_number = run_number - 1
        else:
            run_number = last_run_number

    elif button == Button.DOWN:
        if run_number < last_run_number: 
            run_number = run_number + 1
        else:
            run_number = 0

    elif button == Button.CENTER:
        if run_number == 0:
            watch_sensors()

        elif run_number == 1:
            plattooning_trucks()

        elif run_number == 2:
            flip_engine()

        elif run_number == 3:
            cargo_plane()

        elif run_number == 4:
            connect_cargo()

        elif run_number == 5:
            innovation_model()

        elif run_number == 6:
            ev3.speaker.beep(800)

        # Move on to next run screen
        if run_number < last_run_number: 
            run_number = run_number + 1
        else:
            run_number = 0  