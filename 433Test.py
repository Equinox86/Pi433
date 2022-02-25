import RPi.GPIO as GPIO
from time import sleep

txPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(txPin, GPIO.OUT)
GPIO.output(txPin, GPIO.LOW)

while(True):
	sleep(.0625)
	GPIO.output(txPin, GPIO.HIGH)
	sleep(.0625)
	GPIO.output(txPin, GPIO.LOW)
