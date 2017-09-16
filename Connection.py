import sys
import socket
import time as t

class Connection:
    mPort = 6713
    mServerSock = None
    mIp = ""
    mConnected = False
    mBlock = False
    mClient = None
    mClientSock = None

    mEnd = False
    
    def __init__(s):
        s.mServerSock = socket.socket()
        s.mServerSock.bind((s.mIp, s.mPort))
        s.mServerSock.listen(1)
        s.mServerSock.settimeout(1)
        
    def connect(s):#continues awaiting connection
        sys.stdout.write("Waiting for Connection")
        while not s.mEnd:
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                s.mClientSock, s.mClient = s.mServerSock.accept()
                break
            except IOError:
                pass
        print "\nConnected : ", s.mClient
        s.mConnected = True
        
    def receive(s):
        while not s.mEnd:
            try:
                data = s.mClientSock.recv(1024)
                if len(data) == 0:
                    return None
                else:
                    print "Received : %s" % data 
                    return data
            except IOError:
                return None
                
    def reconnect(s):
        print "Disconnected"
        s.mConnected = False
        s.mClientSock.close()
        print "Restarting..."
        s.connect()
        
    def Send(s, data, _type):
        data = _type + data
        while s.mBlock:
            pass
        s.mBlock = True
        try:
            s.mClientSock.send(str(len(data)).ljust(16) + data)
        except:
            pass
        s.mBlock = False
        
    def stop(s):
        s.mEnd = True
    
    def __del__(s):
        print "Server Ending"
        if s.mClientSock is not None:
            s.mClientSock.close()
        if s.mServerSock is not None:
            s.mServerSock.close()

