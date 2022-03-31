from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()


while True:
        if GPIO.input(37)== GPIO.HIGH:
                print("Smile")
                camera.capture('picture.jpg')
                sleep(2)
