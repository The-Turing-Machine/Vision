import io
import time
import picamera
from PIL import Image

from clarifai.client import ClarifaiApi
import pprint
import requests

import RPi.GPIO as GPIO
import time

# import nltk
# import speech_to_text
# import text_to_speech



GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT)
TRIG = 16
ECHO = 18
LED = 22
p = GPIO.PWM(32, 50)


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
# time.sleep(0.5)


p.start(7.5)
p.ChangeDutyCycle(3)  # turn towards 90 degree
time.sleep(1)  # sleep 1 second
# p.ChangeDutyCycle(12)  # turn towards 90 degree
# time.sleep(1)  # sleep 1 second
# p.ChangeDutyCycle(3)  # turn towards 90 degree
# time.sleep(1)  # sleep 1 second

# try:
#     for i in range(0, 181, 10):
#         dc = (0.05 * i) + 3
#         print dc
#         p.ChangeDutyCycle(dc)
#         time.sleep(0.2)
#
#
# except KeyboardInterrupt:
#     p.stop()
#     GPIO.cleanup()
# p.stop()
# GPIO.cleanup()
#
# while False:
#     # print 'yo'
#     p.ChangeDutyCycle(7.5)  # turn towards 90 degree
#     time.sleep(1)  # sleep 1 second
#     p.ChangeDutyCycle(2.5)  # turn towards 0 degree
#     time.sleep(1)  # sleep 1 second
#     p.ChangeDutyCycle(12.5)  # turn towards 180 degree
#     time.sleep(1)  # sleep 1 second

pp = pprint.PrettyPrinter(indent=2)

clarifai_api = ClarifaiApi("_IKyhCSHnFAqoJ-UdXc1fm0K7q4nXWiIpysjKl2F","rIJ3yNCKQyunlrx6AIRvu7XJIZ4-oTXgCMiH1-7A")
def scan():

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.framerate = 60
        time.sleep(2)
        i = 0
        dc = (0.05 * i) + 3

        # outputs = [{'img':io.BytesIO(),"i":0,"d":0} for _ in range(18)]
        outputs = [io.BytesIO() for _ in range(18)]
        start = time.time()
        for o in outputs:
            i = i + 10
            # o["i"] = i

            dc = (0.05 * i) + 3
            p.ChangeDutyCycle(dc)
            time.sleep(0.50)
            #----------------------------------------------------------------------
            # print "Distance Measurement In Progress"

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

            print "Distance : ",str(distance)
            # o["d"] =distance


            #----------------------------------------------------------------------

            camera.capture(o, 'jpeg', use_video_port=True)
            print 'click!'

            time.sleep(0.50)

        finish = time.time()
        p.stop()
        GPIO.cleanup()
        print('Captured 18 images at %.2ffps' % (18 / (finish - start)))

        a = 0
        for o in outputs:
            print o
            print 'outputting'
            # o["img"].seek(0)
            o.seek(0)
            # image = Image.open(o["img"])
            image = Image.open(o)

            s = str(a) + '.jpeg'
            image.save(s, 'JPEG')

            result = clarifai_api.tag_images(open(s, "rb"))
            tags = result["results"][0]["result"]

            # o["tags"] = tags
            # pp.pprint(tags["tag"]["classes"])

            apiKey = "f7b4e46cec678cc5c3a75a13c394605e"

            for i in tags["tag"]["classes"]:
                url = "http://words.bighugelabs.com/api/2/" + apiKey + "/" + i + "/json"
                req = requests.get(url)
                if(req.status_code == requests.codes.ok):
                    resp = req.text
		    resp = resp["noun"]["syn"]
	 	    resp.append(i)
                    pp.pprint(resp)

            a = a + 1

        # for j in outputs:
        #     if tag
        return outputs


scan()

def noun(answer):

    if "everything" in answer.lower():
        pass
    text = nltk.word_tokenize(answer)
    tags =  nltk.pos_tag(text)

    words =  [word for word, tag in tags if tag in ('NN','NNP','NNS')]
    print words


    if len(words)==1:
        text_to_speech.get_speech("Are you looking for"+ words[0])
        answer = speech_to_text.stt()
        print answer
        if "yes" in answer.lower() or "ye" in answer.lower():
            # result = scan()
            pass

    elif(len(words)>1):
        a = ""
        a = " or ".join(words)
        print a

        text_to_speech.get_speech("What are you looking for"+ a)
        answer = speech_to_text.stt()
        if answer in words:
            pass




#vision

def main():
    while(True):
        text_to_speech.get_speech("command !")
        answer = speech_to_text.stt()
        print answer
        if "vision" in answer.lower():
            text_to_speech.get_speech("How may i help you ?")
            answer = speech_to_text.stt()
            noun(answer)
        else:
            text_to_speech.get_speech("Oops! Didn't catch that,pardon!")
