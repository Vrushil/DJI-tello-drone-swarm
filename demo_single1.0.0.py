import  string
import sys, os, json, time
from fly_tello import FlyTello
my_tellos = list()

#################################################################################################
#######     CONNECTION SETUP OF TCP WITH BEYOND
import socket


# Create a TCP/IP socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('192.168.1.132', 50524)
#control_p=8889
print (sys.stderr, 'starting up on %s port %s' % server_address)

sock.bind(server_address)



# Listen for incoming connections
sock.listen(1)

####################################################################################################



###### DIFFERENT MOTION FUNCTIONS
def Motion(mot:int):

    if mot==2:
        fly.straight(x=0,y=-20,z=60, speed=100)
        fly.straight(x=0,y=20,z=-60, speed=100)
    elif mot==1:
        fly.straight(x=0,y=0,z=50, speed=100)
        fly.straight(x=0,y=0,z=-50, speed=100)
        fly.straight(x=0,y=0,z=50, speed=100)

    else:
        print("Unsupported command")

def semicircle(dir:str):
   # fly.rotate_cw(angle=90, tello=1)
   if dir =='r':
       fly.curve(x1=70, y1=-70, z1=0, x2=140, y2=0, z2=0, speed=60)
   elif dir =='l':
       fly.curve(x1=70, y1=70, z1=0, x2=140, y2=0, z2=0, speed=60)
   else:
       print("Unsupported values entered")
    #fly.rotate_ccw(angle=45, tello=1)

def circle(type:str):
        if type =='ccw':
     #       ledblink()
            fly.curve(x1=70, y1=-70, z1=0, x2=140, y2=0, z2=0, speed=60)
            fly.curve(x1=-70, y1=70, z1=0, x2=-140, y2=0, z2=0, speed=60)
    #        ledstop()

        elif type=='cw':
            fly.curve(x1=70, y1=70, z1=0, x2=140, y2=0, z2=0, speed=60)
            fly.curve(x1=-70, y1=-70, z1=0, x2=-140, y2=0, z2=0,speed=60)
        elif type =='du':
            fly.curve(x1=70, y1=0, z1=-70, x2=140, y2=0, z2=0, speed=60)
            fly.curve(x1=-70, y1=0, z1=70, x2=-140, y2=0, z2=0, speed=60)
        elif type =='ud':
            fly.curve(x1=70, y1=0, z1=70, x2=140, y2=0, z2=0, speed=60)
            fly.curve(x1=-70, y1=0, z1=-70, x2=-140, y2=0, z2=0, speed=60)

        else:
            print("Unsupported values entered")




def eight(direction:str):

 #vertical up to down
        if direction =='vu':
            #ledblink()
            fly.curve(x1=0, y1=-70, z1=70, x2=0, y2=0, z2=140, speed=60)
            fly.curve(x1=0, y1=70, z1=-70, x2=0, y2=0, z2=-140, speed=60)
            fly.curve(x1=0, y1=-70, z1=-70, x2=0, y2=0, z2=-140, speed=60)
            fly.curve(x1=0, y1=70, z1=70, x2=0, y2=0, z2=140, speed=60)

        elif direction=='vd':
            fly.curve(x1=0, y1=-70, z1=-70, x2=0, y2=0, z2=-140, speed=60)
            fly.curve(x1=0, y1=70, z1=70, x2=0, y2=0, z2=140, speed=60)
            fly.curve(x1=0, y1=-70, z1=70, x2=0, y2=0, z2=140, speed=60)
            fly.curve(x1=0, y1=70, z1=-70, x2=0, y2=0, z2=-140, speed=60)

#horizontal right to left
        elif direction=='hr':
            fly.curve(x1=0, y1=-70, z1=-70, x2=0, y2=-140, z2=0, speed=60)
            fly.curve(x1=0, y1=70, z1=70, x2=0, y2=140, z2=0, speed=60)
            fly.curve(x1=0, y1=70, z1=-70, x2=0, y2=140, z2=0, speed=60)
            fly.curve(x1=0, y1=-70, z1=70, x2=0, y2=-140, z2=0, speed=60)
        #horizontal left to right
        elif direction=='hl':
            fly.curve(x1=0, y1=70, z1=-70, x2=0, y2=140, z2=0, speed=60)
            fly.curve(x1=0, y1=-70, z1=70, x2=0, y2=-140, z2=0, speed=60)
            fly.curve(x1=0, y1=-70, z1=-70, x2=0, y2=-140, z2=0, speed=60)
            fly.curve(x1=0, y1=70, z1=70, x2=0, y2=140, z2=0, speed=60)
        elif direction=='criscross':
            fly.curve(x1=70, y1=-70, z1=-70, x2=140, y2=-140, z2=0, speed=60)
            fly.curve(x1=-70, y1=70, z1=70, x2=-140, y2=140, z2=-0, speed=60)
            fly.curve(x1=-70, y1=70, z1=-70, x2=-140, y2=140, z2=0, speed=60)
            fly.curve(x1=70, y1=-70, z1=70, x2=140, y2=-140, z2=0, speed=60)


# MAIN FLIGHT CONTROL LOGIC

# Define the Tello's we're using, in the order we want them numbered
#my_tellos.append('0TQDG2KEDB4D6B')  # 1-Yellow
my_tellos.append('0TQDG3REDB6D33')  # 2-Blue
# my_tellos.append('0TQDFC6EDBH8M8')  # 3-Green
# my_tellos.append('0TQDFC7EDB4874')  # 4-Red

# Control the flight

#fly.takeoff()
#fly.land()
with FlyTello(my_tellos) as fly:
   # while True:
    # Wait for a connection
    while True:
    # Wait for a connection
        print ('waiting for a connection')
        connection, client_address = sock.accept()


        try:
            print ('connection from', client_address)
                # Receive the data in small chunks and retransmit it
            if True:
                data = connection.recv(15).decode().strip()
                print ('received "%s"' % data)
                #data.strip('')
                if data=='circle':
                    circle('ccw')
                    data=''
                    print("wohho ")
                elif data=='takeoff':
                    fly.takeoff()
                    print("wohho")
                    data=''
                elif data== 'up':
                    print('up comm')
                    fly.up(dist=100)
                    data=''

                elif data=='flipr':
                    fly.flip(direction='right',tello=1)
                    data=''
                elif data=='flipl':
                    fly.flip(direction='left',tello=1)
                    data=''
                elif data=='down':
                    fly.down(dist=100)
                    data=''
                elif data=='land':
                    fly.land()
                    x=1



                elif data=='':
                    print ('Data cleared')
                elif data=='close':
                    fly.land()
                    data=''
                    print("Closing connection")
                    break

                     #   print ('sending data back to the client')
                      #  connection.sendall(data.encode())
                    #else:
                     #   print ('no more data from', client_address)
                      #  break


        finally:
            # Clean up the connection
            connection.close()








