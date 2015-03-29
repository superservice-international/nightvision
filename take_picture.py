import picamera
import time
import datetime


with picamera.PiCamera() as camera:
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d-%H:%M:%S')
    camera.resolution = (1024, 768)
    time.sleep(2)
    picture_name = now_str + '.jpg'
    camera.capture(picture_name)
