import picamera
import time
import datetime


def take_picture():
    with picamera.PiCamera() as camera:
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d-%H:%M:%S')
        camera.resolution = (1024, 768)
        time.sleep(2)
        file_name = now_str + '.jpg'
        camera.capture(file_name)
        return file_name


def post_picture(file_name):

    print ("now posting " + file_name)


def delete_picture(file_name):

    print ("now deleting " + file_name)


if __name__ == "__main__":
    picture = take_picture()
    post_picture(picture)
    delete_picture(picture)
