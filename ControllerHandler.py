import smbus
import time as t
import math as m
import threading
from Sensors import *

class DroneHandler:
    mCon = None
    bus = smbus.SMBus(1)
    mode = 1000
    add = 8
    end = False
    state = 0
    blocking = [0, 0, 0, 0]
    #enum
    FORWARD = 0
    RIGHT = 1
    REVERSE = 2
    LEFT = 3
    STOP = -1
    
    prev = STOP
	
    def __init__(s, con):
        s.writeByteData(s.add, 68, 0)
        s.writeByteData(s.add, 66, 0)
        aiThread = threading.Thread(target=s.aiThread)
        s.mCon = con
        aiThread.start()
    
    def __del__(s):
        s.end = True

    def writeByteData(s, add, loc, val):
        #make sure controller is turned on
        while True:
            try:
                s.bus.write_byte_data(add, loc, val)
                break
            except:
                pass

    def stop(s):
        s.mode = 1001
        s.writeByteData(s.add, 116, 0)
        s.writeByteData(s.add, 117, s.mode)
        s.writeByteData(s.add, 96, 0)
        s.writeByteData(s.add, 97, s.mode)
        s.mode = 1000

    def leftMotor(s, i, m):
        if i > 128:
            i = 128
        s.writeByteData(s.add, 96, i)
        s.writeByteData(s.add, 97, m)
          
    def rightMotor(s, i, m):
        if i > 128:
            i = 128
        s.writeByteData(s.add, 116, i)
        s.writeByteData(s.add, 117, m)

    def start(s):
        s.writeByteData(s.add, 68, 1)
        
    def getSensors(s):
        return readSensors()
            
    #0 front, 1 right, 2 back, 3 left
    def aiThread(s):
        #set speed
        speed = 25
        while not s.end:
            #get sensor data
            sensor = s.getSensors()
            if sensor[s.FORWARD] > 0.3:#something ahead:
                s.blocking[s.FORWARD] = True #if command in progress, stops commands
                s.mCon.Send("FORWARD","1")
                if s.prev == s.FORWARD:
                    s.stop()
            else:
                s.blocking[s.FORWARD] = False
                s.mCon.Send("nFORWARD","1")
                
            if sensor[s.LEFT] > 0.9:#something left
                s.blocking[s.LEFT] = True#if command in progress, stops commands
                s.mCon.Send("LEFT","1")
                if s.prev == s.LEFT:
                    s.stop()
            else:
                s.blocking[s.LEFT] = False
                s.mCon.Send("nLEFT","1")
                
            if sensor[s.REVERSE] > 0.7:#something behind
                s.blocking[s.REVERSE] = True#if command in progress, stops commands
                s.mCon.Send("REVERSE","1")
                if s.prev == s.REVERSE:
                    s.stop()
            else:
                s.blocking[s.REVERSE] = False
                s.mCon.Send("nREVERSE","1")
                
            if sensor[s.RIGHT] > 0.9:#something right
                s.blocking[s.RIGHT] = True#if command in progress, stops commands
                s.mCon.Send("RIGHT","1")
                if s.prev == s.RIGHT:
                    s.stop()
            else:
                s.blocking[s.RIGHT] = False
                s.mCon.Send("nRIGHT","1")
			
            if s.state == 0:
                t.sleep(0.1)
            elif s.state == 1:
                if sensor[s.FORWARD] > 0.8:#if something ahead and left
                    if sensor[s.LEFT] > 0.9:
                        #alert user of blockage and avoid
                        print "blockage"
                        s.mCon.Send("Blockage","0")
                        s.leftMotor(speed-70, s.mode+16)
                        s.rightMotor(speed-70, s.mode)
                        s.start()
                        t.sleep(1.0/10)
                        s.leftMotor(speed-70,s.mode+16)
                        s.rightMotor(speed+50, s.mode)
                        s.start()
                        t.sleep(1.0/6)
                    else:
                        #avoid obstacle ahead
                        print "turning left"
                        s.leftMotor(speed-70, s.mode+16)
                        s.rightMotor(speed-70, s.mode)
                        s.start()
                        t.sleep(1.0/10)
                        s.leftMotor(speed-70,s.mode+16)
                        s.rightMotor(speed+50, s.mode)
                        s.start()
                        t.sleep(1.0/6)
                        
                else:#follow wall on right
                    if sensor[s.RIGHT] > 0.9:#right
                        print "veer left"
                        s.leftMotor(speed-32, s.mode+16)
                        s.rightMotor(speed+20, s.mode)
                    elif sensor[s.RIGHT] < 0.8:
                        print "veer right"
                        s.leftMotor(speed+20, s.mode+16)
                        s.rightMotor(speed-32, s.mode)
                    else:
                        print "Forward"
                        s.leftMotor(speed, s.mode+16)
                        s.rightMotor(speed, s.mode)
                s.start()
                t.sleep(1.0/16)
                s.stop()
                
    def turnLeft(s, i):
        s.prev = s.LEFT
        s.leftMotor(-i,s.mode+16)
        s.rightMotor(i, s.mode)
        s.start()

    def turnRight(s, i):
        s.prev = s.RIGHT
        s.leftMotor(i, s.mode+16)
        s.rightMotor(-i, s.mode)
        s.start()

    #stop user crashing into things ahead and behind
    def forward(s, i):
        if not s.blocking[s.FORWARD]:
            s.prev = s.FORWARD
            s.leftMotor(i, s.mode+16)
            s.rightMotor(i, s.mode)
            s.start()
        else:
            print "stuff ahead"
            s.mCon.Send("Obstacle ahead, cannot go forward.","0")
            s.stop()
        
    def reverse(s, i):
        if not s.blocking[s.REVERSE]:
            s.prev = s.REVERSE
            s.leftMotor(-i, s.mode+16)
            s.rightMotor(-i, s.mode)
            s.start()
        else:
            print "stuff behind"
            s.mCon.Send("Obstacle behind, cannot reverse","0")
            s.stop()
