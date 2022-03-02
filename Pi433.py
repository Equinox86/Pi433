import RPi.GPIO as GPIO
import argparse
import time
import signal
from Pulse import Pulse
from copy import deepcopy
import json



LISTEN_PIN = 13
signal_detected = False

currentPulse = Pulse()
pulseQueue = [currentPulse]

logfile = open("logfile.csv", "w+")

def signalHandler(signum, frame):
    GPIO.cleanup(LISTEN_PIN)
    logfile.close()
    print("\nExiting")
    exit(0)

def pulseCopy(src):
    dest = Pulse()
    dest.rise = src.rise
    dest.fall = src.fall
    dest.period = src.period
    dest.width = src.width

    return dest


def pulseDetect(LISTEN_PIN):

    if(GPIO.input(LISTEN_PIN) == GPIO.HIGH):
        # Get the rise time of the next pulse
        rise = time.time()

        # Calculate the period of the current pulse
        currentPulse.period = rise - currentPulse.rise
        currentPulse.width = currentPulse.fall - currentPulse.rise

        # Add Pulse to the process queue
        qPulse = pulseCopy(currentPulse)

        # Noise filter
        # if (qPulse.period > .01):
        pulseQueue.append(qPulse)

        # Update Current Pulse with the rise time of the next pulse
        currentPulse.rise = rise

    else:
        # Get the time of the falling edge
        fall = time.time()
        currentPulse.fall = fall

if __name__ == '__main__':

    # Parse args
    parser = argparse.ArgumentParser(description="Listens and sends codes on the 433Mhz band")
    parser.add_argument("-l", "--listen", help="Listen for codes", action="store_true")
    parser.add_argument("-c", "--code", help="Code to transmit")
    args = parser.parse_args()


    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LISTEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #Signal
    signal.signal(signal.SIGINT, signalHandler)

    # Listen Flag
    if(args.listen):
        # Pin Event detect and Callback
        GPIO.add_event_detect(LISTEN_PIN, GPIO.BOTH)
        GPIO.add_event_callback(LISTEN_PIN, pulseDetect)

        # Load the protocols
        f = open('protocols.json', 'r')
        protos = json.loads(f.read())

        while(True):
            time.sleep(2)
            # Process the pulse queue
            pulseCnt = len(pulseQueue)

            for i in range(0,pulseCnt):
                sigPulse = pulseQueue.pop(0)
                codes = {}

                # Search in protocols
                for k,v in protos():
                    print(k)
                    print(v)

                    # Calculate protcol tolerance
                    protoLowBound = (protos[k]['pulseLength'] - (protos[k]['pulseLength'] * tolerance/50))
                    protoUpperBound = (protos[k]['pulseLength'] + (protos[k]['pulseLength'] * tolerance/50))

                    # Is the period in line with the tolerance?
                    if (sigPulse.period  in range(protoLowBound, protoLowBound):

                # print(str(i) + ":" +  str(sigPulse.period) + ":" + str((sigPulse.width)/sigPulse.period))

