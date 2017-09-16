from Connection import Connection
import time
import math as m
import threading
from ControllerHandler import DroneHandler
from camera import Camera
import subprocess

#0.1.0
class Drone:
    mCon = None
    mEnd = False
    
    def __init__(s):
        s.mCon = Connection()
        s.mCon.connect()
        s.mDrone = DroneHandler(s.mCon)
        s.mCamera = Camera(s.mCon)
        s.cameraThread = threading.Thread(target=s.mCamera.start)
        s.cameraThread.start()
        s.mCamera.resume()
        while (not s.mEnd):
            com = s.mCon.receive()
            if com is None:
                s.mDrone.state = 0
                s.mCamera.pause()
                s.mCon.reconnect()
                s.mCamera.resume()
                continue
            if com == "exit":
                s.mEnd = True
                print "Stop"
                s.mCamera.stop()
                s.mCon.stop()
                s.mDrone.state = 0
            else:
                s.convertToAction(com)
        #subprocess.call("/home/pi/shutdown.sh", shell=True)
            
    def __del__(s):
        s.mEnd = True

    def convertToAction(s, command):#convert received data into commands
        para = 1
        if len(command) > 15:
            s.mDrone.stop()
            return
        while len(command) > 0:
            c = command[0]
            print c
            if c == "0":
                command = command[1:]
                s.mDrone.stop()
                print "Send"
            else:
                speed = command[1:]
                print speed
                command = command[3:]
                if c == "1":
                    s.mDrone.forward(int(speed))
                elif c == "2":
                    s.mDrone.turnLeft(int(speed))
                elif c == "3":
                    s.mDrone.turnRight(int(speed))
                elif c == "4":
                    s.mDrone.reverse(int(speed))
                elif c == "5":
                    s.mDrone.state = int(speed)
Drone()
