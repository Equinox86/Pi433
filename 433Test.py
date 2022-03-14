import RPi.GPIO as GPIO
from time import sleep
import json

txPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(txPin, GPIO.OUT)
GPIO.output(txPin, GPIO.LOW)

f = open('protocols.json', 'r')
protos = json.loads(f.read())


def sendCode(p,v):
	GPIO.output(txPin, GPIO.HIGH)
	# print(protos[p]['pulseLength'] * protos[p][v]['high'] / 1000000)
	sleep(protos[p]['pulseLength'] * protos[p][v]['high'] / 1000000)
	GPIO.output(txPin, GPIO.LOW)
	# print(protos[p]['pulseLength'] * protos[p][v]['low'] / 1000000)
	sleep(protos[p]['pulseLength'] * protos[p][v]['low'] / 1000000)

while(True):
	GPIO.output(txPin, GPIO.LOW)
	sleep(.5)
	for s in range(0,2):
		sendCode('Generic 1','1')
		for i in range(0,32):
			sendCode('Generic 1','0')


