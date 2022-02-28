import RPi.GPIO as GPIO
from time import sleep

txPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(txPin, GPIO.OUT)
GPIO.output(txPin, GPIO.LOW)

# 15us pulse example
pulseWidth = .00150
longOn = pulseWidth * .75
shortOn = pulseWidth * .25

while(True):

	# Long Pulse
	GPIO.output(txPin, GPIO.HIGH)
	sleep(longOn)
	GPIO.output(txPin, GPIO.LOW)
	sleep (pulseWidth - longOn)

	# Short Pulse
	GPIO.output(txPin, GPIO.HIGH)
	sleep(shortOn)
	GPIO.output(txPin, GPIO.LOW)
	sleep (pulseWidth - shortOn)

