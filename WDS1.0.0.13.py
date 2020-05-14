
import string
import sys, os, json, time
from fly_tello import FlyTello
import logging
import datetime
from leds import LED
import pandas as pd

colnames=['Serial No']
ID=pd.read_csv('DroneID.csv',names=colnames)

my_tellos = list() #Creating a list for the drones

led=LED() #Object created for Led program to access the method from leds.py




###Definitions for String modification



import string
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
buffer_Size = 40  # Defining the buffer size that is received from Beyond
type(buffer_Size)


def String_Modified(x: string):  # An important function that modifies the string received from Beyond/ User/PacketSender



    global drones
    global parameters
    # A list that separates string received from beyond
    parameters = x.split(' ')
    drones = parameters[0]  # Reading the first parameter as drones to be given command
    global move  # Reading the 2nd parameter as move which takes input for various commands eg. up down takeoff
    move = parameters[1]
    global numofdrones  # reads the length of first parameter to figure out number of drones
    numofdrones = int(len(list(drones)))
    drones = drones.lower()
    drone_list = list(drones)
    print(" %s Command for following drones %s"%(move ,list(drones)))







def nameofdrones(drones):  # Reads the first parameter and separates the alphabets to make a list
    return list(drones)


values = dict() #Creating a variable of type dictionary
for index, dronename in enumerate(string.ascii_lowercase):  # Converts alphabets to num for eg a=1,b=2
    values[dronename] = index + 1 #Creates a key value type pair .For eg  values[a]= index +1






# Instruction received from client(from Beyond)

#################################################################################################
#######     CONNECTION SETUP OF TCP WITH BEYOND

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 50524)  #localhost for using our own PC as server
#server_address = ('192.168.0.118', 50524) #or you can enter address of the server

print('starting up on %s port %s' % server_address)

sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)


####################################################################################################


###### DIFFERENT MOTION FUNCTIONS


def hover(): # Hover is a command to stay in air. This command is necessary when you want it in the air witjout any specific movement
    with fly.individual_behaviours():

        if numofdrones == 1:
            try:
                fly.stop(tello=values[drones[0]])
            except:
                print("Error for hover of single drone: " )
        else:
            for num in range(0,
                             numofdrones):
                # For loop to give commands to number of drones from 0 to the number of drones mentioned
                try:
                    fly.stop(tello=values[drones[num]])
                except:
                    print("Exception for hovering Drone %s" % values[drones[num]])


def rotate(r_dir: str, degree: int): #Function to rotate the drone in clockwise or anticlockwise direction by entered degree

    if numofdrones == 1:
            try:
                if r_dir == 'ac':
                    fly.rotate_ccw(tello=values[drones[0]], angle=degree)
                    time.sleep(hold)
                elif r_dir == 'c':
                    fly.rotate_cw(tello=values[drones[0]], angle=degree)
                    time.sleep(hold)
            except:
                print("Error for rotate of single drone: %s" %values[drones[0]] )

    else:
        for num in range(0, numofdrones):
            try:
                if r_dir == 'ac':
                    fly.rotate_ccw(tello=values[drones[num]], angle=degree)
                    time.sleep(hold)
                elif r_dir == 'c':
                    fly.rotate_cw(tello=values[drones[num]], angle=degree)
                    time.sleep(hold)
            except:
                print("Rotation error for Drone %s" %values[drones[num]])

# for front,right,up values=+1 to +500 cm
# for back,left,down values=-1 to -500 cm

def go_to_point(front_back: int, left_right: int, up_down: int,
                dronespeed: int):  # front_back=x axis left_right=yaxis and up down=z axis

# go_to_point is a dunction for directly going to a point in xyz coordinate system.
    if numofdrones == 1:
            try:
                fly.straight(x=front_back, y=left_right, z=up_down, speed=dronespeed, tello=values[drones[0]])
                time.sleep(hold)
            except:
                print("Go to Point exception for Drone %s" %values[drones[0]])

    else:

        for num in range(0, numofdrones):
            try:
                fly.straight(x=front_back, y=left_right, z=up_down, speed=dronespeed, tello=values[drones[num]])
                time.sleep(hold)
            except:
                print("Go to Point exception for Drone %s" %values[drones[num]])


def wave_ORIGINAL():
    with fly.individual_behaviours():
        for num in range(0, numofdrones):
            fly.run_individual(fly.up(dist=100, tello=values[drones[num]]))
            time.sleep(0.35)

        time.sleep(1)
        for num in range(0, numofdrones):
            fly.run_individual(fly.down(dist=100, tello=values[drones[num]]))
            time.sleep(0.35)



def Bird():
    left_wing=int(parameters[2])
    right_wing=int(parameters[2])
    with fly.individual_behaviours():

        if numofdrones%2==0:
            center= numofdrones/2
        else:
            center=(numofdrones+1)/2
            center=int(center)

        if parameters[3] is None:
            parameters[3]=1
        for num in range(0,int(parameters[3])):
            fly.run_individual(fly.straight(x=0, y=0, z=int(parameters[2]) - act_height[center], speed=50, tello=center))
            for num in range(center, numofdrones):
                right_wing=right_wing+30
                fly.run_individual(fly.straight(x=0, y=0, z=int(right_wing - act_height[num]), speed=50,tello=values[drones[num]]))


            for num in range(0,center-1):
                left_wing=left_wing + 30
                fly.run_individual(fly.straight(x=0, y=0, z=int(left_wing - act_height[num]), speed=50,tello=values[drones[num]]))
            time.sleep(1)


            fly.run_individual(fly.straight(x=0, y=0, z=int(parameters[2])+right_wing - act_height[center], speed=50, tello=center))
            for num in range(center, numofdrones):
                right_wing=int(act_height[num])-30
                fly.run_individual(fly.straight(x=0, y=0, z=int(right_wing), speed=50,tello=values[drones[num]]))


            for num in range(0,center-1):
                left_wing=int(act_height[num]) - 30
                fly.run_individual(fly.straight(x=0, y=0, z=int(left_wing), speed=50,tello=values[drones[num]]))






#def wave():
    # with fly.individual_behaviours():
    # for num in range(0,numofdrones):
    #   fly.run_individual(fly.up(dist=100,tello=values[drones[num]]))
    # time.sleep(0.35)
    #  fly.run_individual(fly.down(dist=100,tello=values[drones[num]]))
    # time.sleep(0.35)
    # for num in range(0,numofdrones):
    #   fly.run_individual(fly.down(dist=100,tello=values[drones[num]]))
    #  time.sleep(0.35)


def Motion(mot: str):# Function to call different kinds of motion(All drones will do the same motion in the own axis)
    if numofdrones == 1:
            try:
                if mot == 'triangle':
                    fly.straight(x=100, y=100, z=100, speed=100, tello=values[drones[0]])
                    fly.straight(x=0, y=-100, z=0, speed=100, tello=values[drones[0]])
                    fly.straight(x=-100, y=100, z=-100, speed=100, tello=values[drones[0]])
                    time.sleep(hold)
                elif mot == '1':
                    fly.straight(x=0, y=0, z=50, speed=100, tello=values[drones[0]])
                    fly.straight(x=0, y=0, z=-50, speed=100, tello=values[drones[0]])
                    fly.straight(x=0, y=0, z=50, speed=100, tello=values[drones[0]])
                    time.sleep(hold)
                else:
                    print("Unsupported command")
            except :
                print("Motion function error for Drone %s"%values[drones[0]] )
    else:
        for num in range(0, numofdrones):
            try:
                if mot == 'triangle':
                    fly.straight(x=100, y=100, z=100, speed=100, tello=values[drones[num]])
                    fly.straight(x=0, y=-100, z=0, speed=100, tello=values[drones[num]])
                    fly.straight(x=-100, y=100, z=-100, speed=100, tello=values[drones[num]])
                    time.sleep(hold)
                elif mot == '1':
                    fly.straight(x=0, y=0, z=50, speed=100, tello=values[drones[num]])
                    fly.straight(x=0, y=0, z=-50, speed=100, tello=values[drones[num]])
                    fly.straight(x=0, y=0, z=50, speed=100, tello=values[drones[num]])
                    time.sleep(hold)
                else:
                    print("Unsupported command")
            except :
                print("Motion function error for Drone %s"%values[drones[num]] )





def semicircle(dir: str):# DO a semicircle curve with size: s,m,l,xl,xxl
    try:
        if parameters[3]=='s':
            a1=55
            b1=55
            c1=55
            a2=a1*2
            b2=b1*2
            c2=c1*2
        elif parameters[3]=='m':
             a1=70
             b1=70
             c1=70
             a2=a1*2
             b2=b1*2
             c2=c1*2
        elif parameters[3]=='l':
            a1=90
            b1=90
            c1=90
            a2=a1*2
            b2=b1*2
            c2=c1*2
        elif parameters[3]=='xl':
             a1=110
             b1=110
             c1=110
             a2=a1*2
             b2=b1*2
             c2=c1*2
        elif parameters[3]=='xxl':
             a=130
             b=130
             c=130
             a2=a1*2
             b2=b1*2
             c2=c1*2
        else:
            a1=50
            b1=50
            c1=50
            a2=a1*2
            b2=b1*2
            c2=c1*2
    except:
        print("Size of  semi circle not entered")

    if numofdrones == 1:
        try:
            if dir == 'fr':  # A semi-circle going in front from right to left
                fly.curve(x1=a1, y1=-b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)

            elif dir == 'fl':  # A semi-circle going in front from left to right
                fly.curve(x1=a1, y1=b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)
            elif dir == 'bl':  # A semi-circle going back from left to right
                fly.curve(x1=-a1, y1=b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)
            elif dir == 'br':  # A semi-circle going back from left to right
                fly.curve(x1=-a1, y1=-b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)
            elif dir == 'leftl':  # A semi-circle going back from left to right
                    fly.curve(x1=-a1, y1=b1, z1=0, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                    time.sleep(hold)
            elif dir == 'leftr':  # A semi-circle going back from left to right
                fly.curve(x1=a1, y1=b1, z1=0, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)
            elif dir == 'rightl':  # A semi-circle going back from left to right
                fly.curve(x1=a1, y1=-b1, z1=0, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)
            elif dir == 'rightr':  # A semi-circle going back from left to right
                fly.curve(x1=-a1, y1=-b1, z1=0, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)


            else:
                print("Unsupported values entered")
        except:
            print("SemiCircle function error for Single Drone %s" %values[drones[0]])


    else:

        for num in range(0,
                         numofdrones):  # For loop to give commands to number of drones from 0 to the number of drones mentioned
            try:
                if dir == 'fr':  # A semi-circle going in front from right to left
                    fly.curve(x1=a1, y1=-b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)

                elif dir == 'fl':  # A semi-circle going in front from left to right
                    fly.curve(x1=a1, y1=b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)
                elif dir == 'bl':  # A semi-circle going back from left to right
                    fly.curve(x1=-a1, y1=b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)
                elif dir == 'br':  # A semi-circle going back from left to right
                    fly.curve(x1=-a1, y1=-b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)
                elif dir == 'leftl':  # A semi-circle going back from left to right
                        fly.curve(x1=-a1, y1=b1, z1=0, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                        time.sleep(hold)
                elif dir == 'leftr':  # A semi-circle going back from left to right
                    fly.curve(x1=a1, y1=b1, z1=0, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)
                elif dir == 'rightl':  # A semi-circle going back from left to right
                    fly.curve(x1=a1, y1=-b1, z1=0, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)
                elif dir == 'rightr':  # A semi-circle going back from left to right
                    fly.curve(x1=-a1, y1=-b1, z1=0, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)

                else:
                    print("Unsupported values entered")
            except:
                print("SemiCircle function error for Drone %s" %values[drones[num]])



def circle(type: str): # Command Format: abcdefghij circle ac s
      #Draw a circle of  size S,m,l,xl,xxl
    try:
        if parameters[3]=='s':
            a1=55
            b1=55
            c1=55
            a2=a1*2
            b2=b1*2
            c2=c1*2
        elif parameters[3]=='m':
             a1=70
             b1=70
             c1=70
             a2=a1*2
             b2=b1*2
             c2=c1*2
        elif parameters[3]=='l':
            a1=90
            b1=90
            c1=90
            a2=a1*2
            b2=b1*2
            c2=c1*2
        elif parameters[3]=='xl':
             a1=110
             b1=110
             c1=110
             a2=a1*2
             b2=b1*2
             c2=c1*2
        elif parameters[3]=='xxl':
             a=130
             b=130
             c=130
             a2=a1*2
             b2=b1*2
             c2=c1*2
        else:
            a1=50
            b1=50
            c1=50
            a2=a1*2
            b2=b1*2
            c2=c1*2
    except:
        print("Size of circle not entered")




    if numofdrones==1:
          try:
                if type == 'ac':
                    fly.curve(x1=a1, y1=-b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    fly.curve(x1=-a1, y1=b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    time.sleep(hold)

                elif type == 'c':  # Clockwise circle parallel to ground
                    fly.curve(x1=a1, y1=b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    fly.curve(x1=-a1, y1=-b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    time.sleep(hold)

                elif type == 'du':  # Circle that goes first down then up and  motion parallel to wall
                    fly.curve(x1=a1, y1=0, z1=-c1, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    fly.curve(x1=-a1, y1=0, z1=c1, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    time.sleep(hold)

                elif type == 'ud':  # Circle that goes first up and then down and motion parallel to wall
                    fly.curve(x1=a1, y1=0, z1=c1, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    fly.curve(x1=-a1, y1=0, z1=-c1, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[0]]))
                    time.sleep(hold)
                elif type == 'lr':  # Circle that goes first up and then down and motion parallel to wall
                    fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=-b2, z2=0, speed=60, tello=int(values[drones[0]]))
                    fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=b2, z2=0, speed=60, tello=int(values[drones[0]]))
                    time.sleep(hold)
                elif type == 'rl':  # Circle that goes first up and then down and motion parallel to wall
                    fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=b2, z2=0, speed=60, tello=int(values[drones[0]]))
                    fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=-b2, z2=0, speed=60, tello=int(values[drones[0]]))
                    time.sleep(hold)

                else:
                    print("Unsupported values entered")

          except:
                print("Circle exception for Single Drone %s" %values[drones[0]])


    else:
        for num in range(0, numofdrones):

            try:
                if type == 'ac':
                    fly.curve(x1=a1, y1=-b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=-a1, y1=b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)

                elif type == 'c':  # Clockwise circle parallel to ground
                    fly.curve(x1=a1, y1=b1, z1=0, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=-a1, y1=-b1, z1=0, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)

                elif type == 'du':  # Circle that goes first down then up and  motion parallel to wall
                    fly.curve(x1=a1, y1=0, z1=-c1, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=-a1, y1=0, z1=c1, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)

                elif type == 'ud':  # Circle that goes first up and then down and motion parallel to wall
                    fly.curve(x1=a1, y1=0, z1=c1, x2=a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=-a1, y1=0, z1=-c1, x2=-a2, y2=0, z2=0, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)

                elif type == 'lr':  # Circle that goes first up and then down and motion parallel to wall
                    fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=-b2, z2=0, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=b2, z2=0, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)
                elif type == 'rl':  # Circle that goes first up and then down and motion parallel to wall
                    fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=b2, z2=0, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=-b2, z2=0, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)

                else:
                    print("Unsupported values entered")
            except:
                print("Circle exception for Drone %s" %values[drones[num]])


#Draw an eight  of different sizes s,m,lxl,xxl()
def eight(direction: str):# Command Format: abcdefghij eight vu s
    try:

        if parameters[3]=='s':
            a1=52
            b1=52
            c1=52
            a2=a1*2
            b2=b1*2
            c2=c1*2
        elif parameters[3]=='m':
             a1=52
             b1=52
             c1=52

             a2=a1*2
             b2=b1*2
             c2=c1*2
        elif parameters[3]=='l':
            a1=90
            b1=90
            c1=90
            a2=a1*2
            b2=b1*2
            c2=c1*2
        elif parameters[3]=='xl':
             a1=110
             b1=110
             c1=110
             a2=a1*2
             b2=b1*2
             c2=c1*2
        elif parameters[3]=='xxl':
             a=130
             b=130
             c=130
             a2=a1*2
             b2=b1*2
             c2=c1*2
        else:
            a1=50
            b1=50
            c1=50
            a2=a1*2
            b2=b1*2
            c2=c1*2
    except:
        print("Size of circle not entered")


    if numofdrones==1:

        try:
            if direction == 'vu':  # vertical up to down: does circle up then does circle down
                # ledblink()
                fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=int(values[drones[0]]))
                fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=int(values[drones[0]]))
                fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=int(values[drones[0]]))
                fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=int(values[drones[0]]))
                time.sleep(hold)

            elif direction == 'vd':  # Vertical down then goes up
                fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=values[drones[0]])
                time.sleep(hold)

            elif direction == 'hr':  # horizontal right to left : does a circle in front starting from right and then back
                fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)

            elif direction == 'hl':  # horizontal left to right: does a circle in front starting from right and then back
                fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)

            elif direction == 'criscross':  # Makes  an eight diagonally from its original position
                fly.curve(x1=a1, y1=-b1, z1=-c1, x2=a2, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=-a1, y1=b1, z1=c1, x2=-a2, y2=b2, z2=-0, speed=60, tello=values[drones[0]])
                fly.curve(x1=-a1, y1=b1, z1=-c1, x2=-a2, y2=b2, z2=0, speed=60, tello=values[drones[0]])
                fly.curve(x1=a1, y1=-b1, z1=c1, x2=a2, y2=-b2, z2=0, speed=60, tello=values[drones[0]])
                time.sleep(hold)
        except:
            print("Figure 8 exception for Single Drone %s" %values[drones[0]])



    else:# Same function which go for multiple drones
        for num in range(0, numofdrones):
            try:
                if direction == 'vu':  # vertical up to down
                # ledblink()
                    fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=int(values[drones[num]]))
                    fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=int(values[drones[num]]))
                    time.sleep(hold)

                elif direction == 'vd':  # Vertical down then goes up
                    fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=0, z2=c2, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=0, z2=-c2, speed=60, tello=values[drones[num]])
                    time.sleep(hold)

                elif direction == 'hr':  # horizontal right to left
                    fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)

                elif direction == 'hl':  # horizontal left to right
                    fly.curve(x1=0, y1=b1, z1=-c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=-b1, z1=c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=-b1, z1=-c1, x2=0, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=0, y1=b1, z1=c1, x2=0, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)

                elif direction == 'criscross':  # Makes  an eight diagonally from its original position
                    fly.curve(x1=a1, y1=-b1, z1=-c1, x2=a2, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=-a1, y1=b1, z1=c1, x2=-a2, y2=b2, z2=-0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=-a1, y1=b1, z1=-c1, x2=-a2, y2=b2, z2=0, speed=60, tello=values[drones[num]])
                    fly.curve(x1=a1, y1=-b1, z1=c1, x2=a2, y2=-b2, z2=0, speed=60, tello=values[drones[num]])
                    time.sleep(hold)
            except:
                print("Figure 8 exception for Drone %s" %values[drones[num]])








# MAIN FLIGHT CONTROL LOGIC

# Define the Tello's we're using, in the order we want them numbered

###   my_tellos.append('Serial No. of drone') . This function appends the drone to my_tellos list.
#      Here the order of append matters. The one appended first has tello number 1  and so on.

# my_tellos.append('0TQDG2KEDB4D6B')  #1
# #my_tellos.append('0TQDG3REDB6D33') #2 not working
# my_tellos.append('0TQDG4VEDB7G9V')  #2
# my_tellos.append('0TQDFATEDBUP8P')  #3
# my_tellos.append('0TQDFBNEDBN2N3')  #4
# my_tellos.append('0TQDFBNEDB2EPS')  #5
# my_tellos.append('0TQDFBNEDBR92E')  #6
# my_tellos.append('0TQDFBNEDBGKHB')  #7
# my_tellos.append('0TQDFB7EDB1374')  #8
# my_tellos.append('0TQDFCDEDBXSWP')  #9
# my_tellos.append('0TQDFBNEDB13D0')  #10
# my_tellos.append('0TQDFATEDBGC9L')  #11
# my_tellos.append('0TQDFATEDBV212')  #12


my_tellos=ID['Serial No'].tolist()

global timestamp  
timestamp= time.time()





# Control the flight

with FlyTello(my_tellos) as fly: # Creates an object of FlyTello named fly and My_tellos list is passed as argument


    while True:  # To make the program run continously
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:

            print('connection from', client_address)




            # Receive the data in small chunks
            if True:
                #Data variable contains the string received over network.
                data = connection.recv(buffer_Size).decode().strip()
                print('received DATA "%s"' % data)
                String_Modified(data)  # Calling the function string modifies on the data received from client side


                act_height=[]
                for i in range(1,len(my_tellos)+1):
                    try:
                        print("Drone %s : H=%s  Temp= %s %s Battery=%s"%(i,fly.get_status(key='h',tello=int(i)),fly.get_status(key='templ',tello=int(i)),fly.get_status(key='temph',tello=int(i)),fly.get_status(key='bat',tello=int(i))))
                        act_height.insert(i,fly.get_status(key='h',tello=int(i)))
                        logging.debug("%s ------>>>>> Drone %s : H=%s  Temp= %s %s Battery=%s"%(datetime.datetime.now(),i,fly.get_status(key='h',tello=int(i)),fly.get_status(key='templ',tello=int(i)),fly.get_status(key='temph',tello=int(i)),fly.get_status(key='bat',tello=int(i))))
                    except AttributeError as e:
                        print("Could not get height for Drone: %d"% i)
                        act_height.insert(i,0)



                # Clears the data everytime it loops
                data = ''
                nameofdrones(drones)  # Convert the name of drones as a list

                # Hold is  variable to delay the function by x seconds
                hold=0
                hold=float(hold)


                if parameters[0]=='LED': # If the first argument is LED then it suggests a command for LEDS.


                    abc= parameters[2:]#It takes all the variables from 3rd paramter
                    led_comm=' '.join(abc)
                    led.led_com(str(parameters[1]),str(led_comm)) # Takes the name of drones and led command as input
                    #print(led_comm)
                    print(" %s Led Command called" %led_comm)







                elif move=='wave': #Command Format: abcdefghij wave up(comand) 100(distance) .5(time gap between each drone)
                    move = parameters[3]
                    if move is None: #default wave command as up
                        move='up'

                    hold = float(parameters[2])

                    if hold is None:
                        hold=0.5
                    parameters[2] = parameters[4]
                    if parameters[2] is None:
                        parameters[2]=100


                    for i in range(3,len(parameters)):
                        if i+2>=len(parameters):
                            break
                        parameters[i]=parameters[i+2]
                    print("In wave command")

                if move=='bird': #Create a bird like formation(Currently not working)
                    Bird()


                if move == 'height': # Command Format: 'abcdefghij height 100'(distance from ground in cm/s)
                    data = ''
                    with fly.individual_behaviours():
                        for num in range(0,numofdrones):
                            try:
                                fly.straight(x=0,y=0,z=int(parameters[2])-int(fly.get_status(key='h',tello=int(values[drones[num]]))),speed=70,tello=int(values[drones[num]]))
                                print("The actual height now %s" %act_height[num])
                            except :
                                print("Height Error for drone %s " % values[drones[num]])

                if move == 'takeoff':  # The most important command. Drone cannot accept other commands unles it takes off
                    # Clears the buffer
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                fly.run_individual(fly.takeoff(tello=values[drones[0]]))
                                time.sleep(hold)
                                print("Takeoff")

                            except  AttributeError as ae:
                                print("Exception in takeof for  Single Drone %s "% values[drones[0]] )

                        else:

                            for num in range(0, numofdrones):
                                    try:
                                        fly.run_individual(fly.takeoff(tello=values[drones[num]]))
                                        time.sleep(hold)
                                        print("Takeoff")

                                    except  AttributeError as ae:
                                        print("Exception in takeof for Drone %s "% values[drones[num]] )


                elif move == 'hover': #Command Format:- 'abcdefghij hover'
                    data = ''
                    hover() # Calls the hover function defined above


                elif move == 'emergency': #If there is and emergency stop required in case of accident,it will stop all the drones immediately

                    data = ''
                    try:
                        fly.emergency(tello="All")
                        print("Emergency landing")
                    except:
                        print("Emergency landing failed")

                elif move == 'rotate': #command Format: 'abc rotate c 30'  c-direction of rotattion; 130-degrees
                    #Calls the rotate function defined above
                    with fly.individual_behaviours():
                        try:
                            fly.run_individual(rotate(r_dir=parameters[2], degree=int(parameters[3])))
                        except:
                            print("Rotate error")


                elif move == 'straight': # Command format: 'abcdef x y z speed'
                            # eg: abcdef -100 -100 0 70  MaxSpeed = 70 otherwise gives error
                    #Goes straught to a point in xyz co-ordinate plane
                    with fly.individual_behaviours():
                        fly.run_individual(go_to_point(front_back=int(parameters[2]), left_right=int(parameters[3]),
                                                       up_down=int(parameters[4]), dronespeed=int(parameters[5])))


                elif move == 'up': #Command format: 'abc up 130'
                    # abc = drones; up = command; 130= distance in cm/s
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                fly.run_individual(fly.up(dist=int(parameters[2]), tello=values[drones[0]]))
                                time.sleep(hold)
                            except:
                                print("Up command exception for  SIngle Drone %s" %values[drones[0]])
                        else:
                            for num in range(0, numofdrones):
                                try:
                                    fly.run_individual(fly.up(dist=int(parameters[2]), tello=values[drones[num]]))
                                    time.sleep(hold)
                                except:
                                    print("Up command exception for Drone %s" %values[drones[num]])

                elif move == 'down': #Command format: 'abcde down 100'
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                fly.run_individual(fly.down(dist=int(parameters[2]), tello=values[drones[0]]))
                                time.sleep(hold)
                            except:
                                print("Down command exception for  Single Drone %s" %values[drones[0]])
                        else:
                            for num in range(0, numofdrones):
                                try:
                                    fly.run_individual(fly.down(dist=int(parameters[2]), tello=values[drones[num]]))
                                    time.sleep(hold)
                                except:
                                    print("Down command exception for Drone %s" %values[drones[num]])

                elif move == 'right':#Command Format: 'abcd right 50'
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                fly.run_individual(fly.right(dist=int(parameters[2]), tello=values[drones[0]]))
                                time.sleep(hold)
                                print("Going Right")
                            except:
                                print("Right command exception for Single Drone %s" %values[drones[0]])
                        else:

                            for num in range(0, numofdrones):
                                try:
                                    fly.run_individual(fly.right(dist=int(parameters[2]), tello=values[drones[num]]))
                                    time.sleep(hold)
                                    print("Going Right")
                                except:
                                    print("Right command exception for Drone %s" %values[drones[num]])



                elif move == 'left':    #Command Format: 'abcd left 50'
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                fly.run_individual(fly.left(dist=int(parameters[2]), tello=values[drones[0]]))
                                time.sleep(hold)
                                print("Going Left")
                            except:
                                print("Left command exception for Single Drone %s" %values[drones[0]])
                        else:
                            for num in range(0, numofdrones):
                                try:
                                    fly.run_individual(fly.left(dist=int(parameters[2]), tello=values[drones[num]]))
                                    time.sleep(hold)
                                    print("Going Left")
                                except:
                                    print("Left command exception for Drone %s" %values[drones[num]])

                elif move == 'forward': #Command Format: 'abcd forward 50'
                    #Moves the drone in forward direction
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                                try:
                                    fly.run_individual(fly.forward(dist=int(parameters[2]), tello=values[drones[0]]))
                                    time.sleep(hold)
                                    print("Going forward")
                                except:
                                    print("Forward command exception for Single Drone %s" %values[drones[0]])
                        else:
                            for num in range(0, numofdrones):
                                try:
                                    fly.run_individual(fly.forward(dist=int(parameters[2]), tello=values[drones[num]]))
                                    time.sleep(hold)
                                    print("Going forward")
                                except:
                                    print("Forward command exception for Drone %s" %values[drones[num]])

                elif move == 'flip':  #Command Format: 'abcd flip l'
                    #flips the drone in forward,back,left right direction
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                if parameters[2] == 'r': #right flip
                                    fly.run_individual(fly.flip(direction='right', tello=int(values[drones[0]])))
                                    time.sleep(hold)
                                elif parameters[2] == 'l': #left flip
                                    fly.run_individual(fly.flip(direction='left', tello=int(values[drones[0]])))
                                    time.sleep(hold)
                                elif parameters[2] == 'f': #forward flip
                                    fly.run_individual(fly.flip(direction='forward', tello=int(values[drones[0]])))
                                    time.sleep(hold)
                                elif parameters[2] == 'b': #backward flip
                                    fly.run_individual(fly.flip(direction='back', tello=int(values[drones[0]])))
                                    time.sleep(hold)
                            except:
                                print("Flip command exception for Single Drone %s" %values[drones[0]])


                        else:
                            for num in range(0, numofdrones):
                                try:
                                    if parameters[2] == 'r': #right flip
                                        fly.run_individual(fly.flip(direction='right', tello=int(values[drones[num]])))
                                        time.sleep(hold)
                                    elif parameters[2] == 'l': #left flip
                                        fly.run_individual(fly.flip(direction='left', tello=int(values[drones[num]])))
                                        time.sleep(hold)
                                    elif parameters[2] == 'f': #forward flip
                                        fly.run_individual(fly.flip(direction='forward', tello=int(values[drones[num]])))
                                        time.sleep(hold)
                                    elif parameters[2] == 'b': #backward flip
                                        fly.run_individual(fly.flip(direction='back', tello=int(values[drones[num]])))
                                        time.sleep(hold)
                                except:
                                    print("Flip command exception for Drone %s" %values[drones[num]])

                elif move == 'back':  #Command Format:  'abcdefghij back 50'
                    #Moves the drone backwards
                    data = ''
                    with fly.individual_behaviours():
                        if numofdrones==1:
                            try:
                                fly.run_individual(fly.back(dist=int(parameters[2]), tello=int(values[drones[0]])))
                                time.sleep(hold)
                                print("back multiple")
                            except:
                                print("Back command exception for Single Drone %s" %values[drones[0]])

                        else:
                            for num in range(0, numofdrones):
                                try:
                                    fly.run_individual(fly.back(dist=int(parameters[2]), tello=int(values[drones[num]])))
                                    time.sleep(hold)
                                    print("back multiple")
                                except:
                                    print("Back command exception for Drone %s" %values[drones[num]])


                elif move == 'motion': #Calls the motion function defined above
                    with fly.individual_behaviours():
                        fly.run_individual(Motion(mot=parameters[2]))


                elif move == 'circle':  # Command Format: 'abcd circle ac s'
                    data = ''
                    with fly.individual_behaviours():
                        fly.run_individual(circle(str(parameters[2])))
                    print("Synchronized circle")

                elif move == 'semicircle':  # Command Format: 'abcd semicirclecircle l s'
                    data = ''
                    with fly.individual_behaviours():
                        fly.run_individual(semicircle(str(parameters[2])))
                    print("Semi circle")

                elif move == 'eight':  # Command Format: 'abcd eight  criscross s'
                    data = ''
                    with fly.individual_behaviours():
                        fly.run_individual(eight(str(parameters[2])))
                    print("Eight command completed for number of drones with Synchronization")


                elif move == 'rc': #Command format 'abcde rc up'
                    data = ''
                    if numofdrones == 1:
                        if str(parameters[2]) == 'up':
                            fly.set_rc(left_right=0, forward_back=0, up_down=70, yaw=0, tello=int(values[drones[0]]))
                            fly.stop(tello=int(values[drones[0]]))
                            time.sleep(0.09)
                            fly.set_rc(left_right=0, forward_back=0, up_down=-20, yaw=0, tello=int(values[drones[0]]))
                            time.sleep(0.09)
                            fly.stop(tello=int(values[drones[0]]))
                            print("Going up")
                            # fly.stop(int(values[drones[0]]))
                        elif str(parameters[2]) == 'down':
                            fly.set_rc(left_right=0, forward_back=0, up_down=-20, yaw=0, tello=int(values[drones[0]]))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            print("Going down")
                        elif str(parameters[2]) == 'left':
                            fly.run_individual(fly.set_rc(left_right=-20, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            print("Going left")
                        elif str(parameters[2]) == 'right':
                            fly.run_individual(fly.set_rc(left_right=20, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            print("Going right")
                        elif str(parameters[2]) == 'forward':
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=20, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))

                            print("Going forward")
                        elif str(parameters[2]) == 'back':
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=-20, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))

                            print("Going back")
                        elif str(parameters[2]) == 'yawl':
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=20,
                                                          tello=int(values[drones[0]])))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))

                            print("Rotating(yaw)")
                        elif str(parameters[2]) == 'yawr':
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=-20,
                                                          tello=int(values[drones[0]])))
                            time.sleep(2)
                            fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=0,
                                                          tello=int(values[drones[0]])))

                            print("Rotating(yaw)")
                    else:
                        for num in range(0, numofdrones):
                            if str(parameters[2]) == 'up':
                                fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=20, yaw=0,
                                                              tello=int(values[drones[num]])))
                                print("Going up")
                            elif str(parameters[2]) == 'down':
                                fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=-20, yaw=0,
                                                              tello=int(values[drones[num]])))
                                print("Going down")
                            elif str(parameters[2]) == 'left':
                                fly.run_individual(fly.set_rc(left_right=-20, forward_back=0, up_down=0, yaw=0,
                                                              tello=int(values[drones[num]])))
                                print("Going left")
                            elif str(parameters[2]) == 'right':
                                fly.run_individual(fly.set_rc(left_right=20, forward_back=0, up_down=0, yaw=0,
                                                              tello=int(values[drones[num]])))
                                print("Going right")
                            elif str(parameters[2]) == 'forward':
                                fly.run_individual(fly.set_rc(left_right=0, forward_back=20, up_down=0, yaw=0,
                                                              tello=int(values[drones[num]])))
                                print("Going forward")
                            elif str(parameters[2]) == 'back':
                                fly.run_individual(fly.set_rc(left_right=0, forward_back=-20, up_down=0, yaw=0,
                                                              tello=int(values[drones[num]])))
                                print("Going back")
                            elif str(parameters[2]) == 'yawl':
                                fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=20,
                                                              tello=int(values[drones[num]])))
                                print("Rotating(yaw)")
                            elif str(parameters[2]) == 'yawr':
                                fly.run_individual(fly.set_rc(left_right=0, forward_back=0, up_down=0, yaw=-20,
                                                              tello=int(values[drones[num]])))
                                print("Rotating(yaw)")




                elif move == 'land': #Command Format : 'abcdefghij land'
                    data = ''
                    if numofdrones==1:
                        try:
                            fly.land(tello=int(values[drones[0]]))
                            time.sleep(hold)
                            print("land else")
                        except AttributeError as ae:
                            print("Landing error for Single drone %s" % values[drones[0]] )

                    else:


                        for num in range(0, numofdrones):
                            try:
                                fly.land(tello=int(values[drones[num]]))
                                time.sleep(hold)
                                print("land else")
                            except AttributeError as ae:
                                print("Landing error for drone %s" % values[drones[num]] )


                elif move == '':  # if move is empty
                    data = ''
                    print('Move is empty')

                elif move == 'close': #Avoid using this command
                    data = ''
                    fly.land()
                    print("Closing connection")
                    break

                data = ''


        finally:
            # Clean up the connection
            connection.close()
