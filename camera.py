import picamera
import time
import io

class Camera:
    end = False
    pauseBool = False
    def __init__(s, conn):
        s.conn = conn
    def start(s):
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.resolution =(480, 270)
            camera.framerate = 16
            #get camera data
            for x in camera.capture_continuous(stream, "jpeg", use_video_port=True):
                if s.end:
                    stream.close()
                    return
                while s.pauseBool:
                    time.sleep(0.1)
                stream.seek(0)
                img = stream.read()
                try:
                    s.conn.Send(img, "2")#send camera data
                except:
                    pass
                stream.seek(0)
                stream.truncate()
                time.sleep(1/16)
    def stop(s):
        s.end = True
    def pause(s):
        s.pauseBool = True
    def resume(s):
        s.pauseBool = False
