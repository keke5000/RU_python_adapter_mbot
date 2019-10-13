#!/usr/bin/env python3

import socket
import serial
from serial import Serial
import time
from lib.mBot import *

bot = mBot()
bot.startWithSerial("/dev/ttyUSB0")

size = 20
host = ''
speed = 100
port = 1222
debug = False

def log(text):
    if(debug): print(text)

def _int(s):
    s = s.strip()
    return int(s) if s else 0

def calculateAndRun(motorArray):
    lastLeft = 0
    right = 0
    left = 0

    for motorData in motorArray:
        print("mdata  " + motorData)
        if(motorData == ''):
            continue
        if(motorData[0] == 'L'):
            left = _int(motorData.split('L')[1])
        elif(motorData[0] == 'R'):
            lastLeft = left # assign only if right motor is read (end of packet)
            right = _int(motorData.split('R')[1])


    if(lastLeft > 0 and right > 0):
        log("forward")
        #robohat.forward(speed)
        bot.doMove(100,100)
    elif(lastLeft > 0):
        log("left")
        bot.doMove(100, 0)
        #robohat.spinLeft(speed)
        #robohat.turnForward(0, 100)
    elif(right > 0):
        log("right")
        bot.doMove(0,100)
        #robohat.spinRight(speed)
    else:
        bot.doMove(0,0)
        #robohat.stop()

#  family = Internet, type = stream socket means TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#  we have a socket, we need to bind to an IP address and port
#  to have a place to listen on
sock.bind((host, port))
sock.listen(5)
#  we can store information about the other end
#  once we accept the connection attempt
c, addr = sock.accept()
while 1:
    data = c.recv(size)
    if data:
        socketString = data.decode("UTF-8")
        motorArray = socketString.split(' ')
        calculateAndRun(motorArray)
        time.sleep(0.15)
