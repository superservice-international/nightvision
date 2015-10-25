import picamera
import time
import datetime
import os
import requests
from requests.auth import HTTPBasicAuth
from PIL import Image


def take_picture():
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = path + "/" + now_str + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)
        camera.capture(file_name)
        print (file_name + " taken")
        return file_name


def reduce_filezise(file_name):
    im = Image.open(file_name)
    im.save(file_name, 'JPEG', quality=90)


def post_picture(file_name):
    # host = 'http://kamera.reimers-sportpferde.de/-/pictures/'
    # user = "creimers"
    # pw = "1lb2es!M"
    host = 'http://192.168.178.32:8000/-/pictures/'
    user = os.environ["PIC_USER"]
    pw = os.environ["PIC_USER_PW"]
    print ("now posting " + file_name)
    post = requests.post(
            url=host,
            auth=HTTPBasicAuth(user, pw),
            files={'photo': open(file_name, 'rb')}
        )
    if post.status_code == 201:
        return True


def delete_picture(file_name):
    print ("now deleting " + file_name)
    os.remove(file_name)


def post_remaining():
    path = os.path.dirname(os.path.abspath(__file__))
    for pic in os.listdir(path):
        if pic.split('.')[-1] == 'jpg':
            post = post_picture('/'.join([path, pic]))
            if post:
                delete_picture('/'.join([path, pic]))


if __name__ == "__main__":
    picture = take_picture()
    reduce_filezise(picture)
    posted = post_picture(picture)
    if posted:
        delete_picture(picture)
    post_remaining()
