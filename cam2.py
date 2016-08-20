import io
import time
import picamera
from PIL import Image

from clarifai.client import ClarifaiApi
import pprint
import requests

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 50)

p.start(7.5)
p.ChangeDutyCycle(3)  # turn towards 90 degree
time.sleep(1)  # sleep 1 second
# p.ChangeDutyCycle(12)  # turn towards 90 degree
# time.sleep(1)  # sleep 1 second
# p.ChangeDutyCycle(3)  # turn towards 90 degree
# time.sleep(1)  # sleep 1 second

try:
    for i in range(0, 181, 10):
        dc = (0.05 * i) + 3
        print dc
        p.ChangeDutyCycle(dc)
        time.sleep(0.2)


except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
p.stop()
GPIO.cleanup()
#
# while False:
#     # print 'yo'
#     p.ChangeDutyCycle(7.5)  # turn towards 90 degree
#     time.sleep(1)  # sleep 1 second
#     p.ChangeDutyCycle(2.5)  # turn towards 0 degree
#     time.sleep(1)  # sleep 1 second
#     p.ChangeDutyCycle(12.5)  # turn towards 180 degree
#     time.sleep(1)  # sleep 1 second
'''
pp = pprint.PrettyPrinter(indent=2)

clarifai_api = ClarifaiApi()


with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.framerate = 60
    time.sleep(2)

    outputs = [io.BytesIO() for i in range(10)]
    start = time.time()
    for o in outputs:
        camera.capture(o, 'jpeg', use_video_port=True)
        print 'click!'
        time.sleep(0.5)

    finish = time.time()

    print('Captured 10 images at %.2ffps' % (10 / (finish - start)))

    a = 0
    for o in outputs:
        print 'outputting'
        o.seek(0)
        image = Image.open(o)
        s = str(a) + '.jpeg'
        image.save(s, 'JPEG')

        result = clarifai_api.tag_images(open(s, "rb"))
        tags = result["results"][0]["result"]

        # pp.pprint(tags["tag"]["classes"])

        apiKey = "f7b4e46cec678cc5c3a75a13c394605e"

        for i in tags["tag"]["classes"]:
            url = "http://words.bighugelabs.com/api/2/" + apiKey + "/" + i + "/json"
            req = requests.get(url)
            if(req.status_code == requests.codes.ok):
                resp = req.text
                pp.pprint(resp)

        a = a + 1
'''
