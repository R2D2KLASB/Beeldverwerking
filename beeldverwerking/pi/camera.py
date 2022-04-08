from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO


class Camera():

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.start_preview()

    def createPic(self, path, file):
        self.camera.capture(path + '/' + file)

    def checkButton(self):
        if GPIO.input(self.pin)== GPIO.HIGH:
            return True
        return False
