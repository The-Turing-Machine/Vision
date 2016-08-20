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
TRIG = 16
ECHO = 18
LED = 22
p = GPIO.PWM(32, 50)
#
#
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
#
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(0.5)
#
#
p.start(7.5)
p.ChangeDutyCycle(3)  # turn towards 90 degree
time.sleep(0.5)  # sleep 1 second
# p.ChangeDutyCycle(12)  # turn towards 90 degree
# time.sleep(1)  # sleep 1 second
# p.ChangeDutyCycle(3)  # turn towards 90 degree
# time.sleep(1)  # sleep 1 second
# p.stop()
# GPIO.cleanup()

pp = pprint.PrettyPrinter(indent=2)

clarifai_api = ClarifaiApi('_IKyhCSHnFAqoJ-UdXc1fm0K7q4nXWiIpysjKl2F',
                           'rIJ3yNCKQyunlrx6AIRvu7XJIZ4-oTXgCMiH1-7A')


def scan():
    with picamera.PiCamera() as camera:
        # camera.resolution = (1024, 768)
        # camera.framerate = 60
        time.sleep(2)
        i = 0
        dc = (0.05 * i) + 3

        outputs = [{'img': io.BytesIO(), "i": 0, "d": 0} for _ in range(11)]
        # outputs = [io.BytesIO() for _ in range(10)]
        start = time.time()
        for o in outputs:
            o["i"] = i

            dc = (0.05 * i) + 3
            p.ChangeDutyCycle(dc)
            time.sleep(0.2)
            # #----------------------------------------------------------------------
            print "Distance Measurement In Progress"

            GPIO.output(TRIG, True)
            GPIO.output(LED, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            GPIO.output(LED, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            print "Distance : ", str(distance)
            o["d"] = distance

            # #----------------------------------------------------------------------

            camera.capture(o['img'], 'jpeg', use_video_port=True)
            print 'click!'

            time.sleep(0.2)
            i = i + 18

        finish = time.time()
        p.stop()
        GPIO.cleanup()
        print('Captured 10 images at %.2ffps' % (10 / (finish - start)))

        a = 0
        # all = set()
        for o in outputs:
            # print o
            print 'outputting'
            o["img"].seek(0)
            # o.seek(0)
            image = Image.open(o["img"])
            # image = Image.open(o)

            s = str(a) + '.jpeg'
            image.save(s, 'JPEG')

            result = clarifai_api.tag_images(open(s, "rb"))
            tags = result["results"][0]["result"]

            print 'For angle ', o['i'], 'at distance ', o["d"]
            pp.pprint(tags["tag"]["classes"])
            # for x in tags["tag"]["classes"]:
            # all.add(x)
            # all.append(tags["tag"]["classes"])
            # pp.pprint(result)
            # o["tags"] = tags

            # apiKey = "f7b4e46cec678cc5c3a75a13c394605e"
            #
            # for i in tags["tag"]["classes"]:
            #     url = "http://words.bighugelabs.com/api/2/" + apiKey + "/" + i + "/json"
            #     req = requests.get(url)
            #     if(req.status_code == requests.codes.ok):
            #         resp = req.text
            #         # resp = resp["noun"]["syn"]
            #         # resp.append(i)
            #         # pp.pprint(resp)

            a = a + 1
        # print '---------'
        # print all

if __name__ == '__main__':
    scan()
