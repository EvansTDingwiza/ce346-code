# This is barely modified from Kivy tutorials: 
#     https://kivy.org/doc/stable/tutorials/pong.html
# ...to integrate serial input from the MSP430FR5994

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import random
import serial
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation
import datetime as dt
from itertools import count
Lightval = 50;
Watervalue = 50;
reservoir = 50;
sensorreading = 0;
import csv
import time

x_var =[]
y_var =[]

index = count()
def initialize_serial():
    try:
        mspserial = serial.Serial('COM10', 9600)

    except:
        print("Failed to connect. Check your port name")
        exit()
    return mspserial


def serial_read(serial_obj):
    data = serial_obj.read()
    return data
    #read the serial data from the port
#def processdatato_ints():
   
# Read input from serial port for movement
# value = arduino.readline()
def isaHundredNum(nums):
    count = 0;
    itis = True
    hunnid = [b'1', b'0',b'0']
    while(count):
        itis =  itis and (nums[count]==hunnid[count])
    return itis

def animate(i):
        data = pd.read_csv('data.csv')
        x = data['timeval']
        y = data['light']
        plt.cla()
        plt.plot(x,y)

    #ani = animation.FuncAnimation(plt.gcf(), animate, interval= 1000)
    #plt.show()
if __name__ == '__main__':
    # Connect to serial port first
    # Make sure to replace this with YOUR MSP430s serial port
    #PongApp().run()
    # Cleanup
    #databits = [b'1',b'2',b'3']
    #while(True):
    x_value = 0#dt.datetime.now().strftime('%H:%M:%S.%f')
    fieldnames = ["timeval", "sensoreading"]
    with open('newdata.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames= fieldnames)
        csv_writer.writeheader()
   
    serial_obj = initialize_serial()
    count = 0;
    num = []
    numbers = []
    empty = " "
    bits = [b'1' ,b'2',b'3']
    index = 0;
    single = False
    sensordefined = False
    resultvalues = []
    
    variable = input("type the variable you want to observe in real time: ")
    if(variable== "water"):
        index = 2
    elif(variable == "Light"):
        index = 0
    else:
        index = 1
    serial_obj.flushInput()
    

    while(True):
       
        serial_obj.flushOutput()
        
        """
        if(count == 300):
            time.sleep(1)
            
            serial_obj.close()
            serial_obj = initialize_serial()
            variable = input("type the variable you want to observe in real time: ")
            if(variable== "water"):
                index = 2
            elif(variable == "Light"):
                index = 0
            else:
                index = 1
            count = 0
            serial_obj.flushInput()
        """
        #time.sleep(1)
        #count = 0
        serial_obj.write(bits[index])
        #print(count)
        data = serial_read(serial_obj)
        #print(data)
        if(data == b'.' and len(num) == 2):
            for a in num:
                empty += str(a)
            if(empty != " "):
                sensorreading = (int(empty))
                sensordefined = True
            empty = " "
            num.clear()
            print(sensorreading)
            #return Lightvalue
        elif(data == b'.' and len(num)== 1):
            single = True
            for a in num:
                empty += str(a)
            if(empty != " "):
                sensorreading = (int(empty))
                sensordefined = True
            empty = " "
            num.clear()
            print(sensorreading)
        else:
            if(not(single)):
                if(data != b'.'):
                    num.append(str(int(data)))
                if(len(num)>=3):
                    if(isaHundredNum(num)):
                        #index += 1
                        for a in num:
                            empty += str(a)
                        sensorreading = (int(empty))
                        print(sensorreading)
                        sensordefined = True
                        empty = " "
                        num.clear()
            else:
                single = False
            
        if(sensordefined):   
            with open('newdata.csv', 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
                info = {
                    "timeval": x_value,
                    "sensoreading": sensorreading
                }
                csv_writer.writerow(info)
                count += 1
                x_value = count
            sensordefined = False

        #serial_obj.flushInput() 
        #time.sleep(1)           
    serial_obj.close()

    



#write data to the msp 430



"""
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
#databits = [1,2,3];
length = len(databits)
newdata = []
while(True):
count = 64
for a in databits:

while(count):
-- count

print(data)
newdata.append(data)
#display the data
#print(data)
newdata.clear()
"""





