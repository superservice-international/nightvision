import picamera
import time
import datetime
import os
import requests
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
        print(file_name + " taken")
        return file_name


def reduce_filezise(file_name):
    im = Image.open(file_name)
    im.save(file_name, 'JPEG', quality=90)


class TokenAuth(requests.auth.AuthBase):
    def __call__(self, r):
        token = 'Token %s' % os.environ.get('API_TOKEN')
        r.headers['Authorization'] = token
        return r


def post_picture(file_name):
    host = os.environ.get('API_URL')

    query = "?query=mutation{postPicture(input: {}){success errors clientMutationId}}"

    print("now posting " + file_name)
    post = requests.post(
            url=host + query,
            auth=TokenAuth(),
            files={'image': open(file_name, 'rb')}
        )
    return post.json()['data']['postPicture']['success']


def delete_picture(file_name):
    print("now deleting " + file_name)
    os.remove(file_name)


def post_remaining():
    path = os.path.dirname(os.path.abspath(__file__))
    for pic in os.listdir(path):
        if pic.split('.')[-1] == 'jpg':
            post = post_picture('/'.join([path, pic]))
            if post:
                delete_picture('/'.join([path, pic]))


if __name__ == "__main__":
    #  picture = '/Users/creimers/Downloads/2017-03-06_17-19-55.jpg'
    picture = take_picture()
    reduce_filezise(picture)
    posted = post_picture(picture)
    if posted:
        delete_picture(picture)
    post_remaining()
