import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
LED = 25

for x in range(100):
    print "Distance Measurement In Progress"

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(LED, GPIO.OUT)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    time.sleep(0.5)

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

    print "Distance:", distance, "cm"

GPIO.cleanup()
