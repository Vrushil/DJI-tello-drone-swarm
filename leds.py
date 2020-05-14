
import  netaddr
import  netifaces
import  socket
import  threading
import  time
import  ipaddress
import numpy as np


class LED:


    def __init__(self):
     #   str(ip) for ip in ipaddress.IPv4Network('192.168.0.80/100'):
        self.lednum=0
        self.led_port = 8090
        self.led_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.led_socket.bind(('', self.led_port))

        self.ip_adrress={'a':'192.168.0.81','b':'192.168.0.82','c':'192.168.0.83','d':'192.168.0.84','e':'192.168.0.85','f':'192.168.0.86','g':'192.168.0.87','h':'192.168.0.88','i':'192.168.0.89','j':'192.168.0.90','k':'192.168.0.91','l':'192.168.0.92'}




    def led_com(self,uav:str,led_command:str,):

        x=uav
        x.split()
        print("LED command for drone(s) %s" %x)
        #led_command='fill 0 0 255'
        #for ip in self.ip_adrress.values():
         #   print(ip)
          #  print()

        for num in range(0,len(x)):

                print(str(x[num]))
                self.led_socket.sendto((led_command).encode(),(self.ip_adrress.get(str(x[num])),self.led_port))

                print("Command sent to Arduno: %s"% led_command)

              #      print("num")
            #except:
             #   print("Command sent to Arduno exception:%s"% led_command)
              #  print("Led Exception")



#        for ip in self.ip_adrres:

        #for num in np.arange(0,255):
        #for num in range(0,256):
         #   x='fill %s %s %s'.format(num,num,num)
 #           self.led_socket.sendto((led_command).encode(),(ip,led_port))
            #time.sleep(0.9)





