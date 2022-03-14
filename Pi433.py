import RPi.GPIO as GPIO
import argparse
import time
import signal

from Pulse import Pulse
from copy import deepcopy
import json


# Static Globals
tolerance = .20
collect = False
LISTEN_PIN = 13
signal_detected = False

currentPulse = Pulse()
currentPulse.rise = time.time()
currentPulse.fall = currentPulse.rise
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
    dest.length = src.length

    return dest

def pulseDetect(LISTEN_PIN):

    if(GPIO.input(LISTEN_PIN) == GPIO.HIGH):
        # Get the rise time of the next pulse
        rise = time.time()

        # Calculate the period of the current pulse (us)
        currentPulse.period = (rise - currentPulse.rise) *1000000
        currentPulse.length = (currentPulse.fall - currentPulse.rise) * 1000000

        # Add valid Pulses to the process queue
        if (currentPulse.length > 0) :
            qPulse = pulseCopy(currentPulse)
            pulseQueue.append(qPulse)

        # Update Current Pulse with the rise time of the next pulse
        currentPulse.rise = rise

    else:
        # Get the time of the falling edge
        fall = time.time()
        currentPulse.fall = fall

def inTolerance(sigPulse, sigH, sigL):

    # Calculate the durations of high and low segments of the pulse
    highTime = sigPulse.length
    lowTime = sigPulse.period - highTime

    # Are the durations in tolerance for this protocol?
    rc = sigH * (1-tolerance) < highTime < sigH * (1+tolerance)
    rc &= sigL * (1-tolerance) < lowTime < sigL * (1+tolerance)

    return rc

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
        code = 0

        while(True):
            time.sleep(2)

            # Process the pulse queue
            pulseCnt = len(pulseQueue)
            for i in range(0,pulseCnt):
                sigPulse = pulseQueue.pop(0)
                logfile.write(str(sigPulse.period)+",\n")

                # Long Pulse - Could be a Sync pulse or other large break in data
                if sigPulse.period > 4300:
                    collect = False
                    if (code != 0):
                        print(code)
                    code = 0

                # Search in protocols for a sync
                for p in protos:

                    # If we are in the collection state -
                    if collect:
                        segLength = sigPulse.period  / (protos[p]['1']['low'] + protos[p]['1']['high'])

                        code << 1

                        dataBit1H = protos[p]['1']['high'] * segLength
                        dataBit0H = protos[p]['0']['high'] * segLength
                        dataBit1L = protos[p]['1']['low'] * segLength
                        dataBit0L = protos[p]['0']['low'] * segLength

                        if inTolerance(sigPulse,dataBit1H,dataBit1L):
                            code |= 1
                        elif not inTolerance(sigPulse,dataBit0H,dataBit0L):
                            # Garbage Data - Abort collection
                            code = 0
                            collect = False

                    else :
                        # Calculate the size of a sync bit segment
                        pulseSeg = sigPulse.period / (protos[p]['syncBit']['low'] + protos[p]['syncBit']['high'])

                        # Calculate the appropriate high and low timing for this signal and protocol
                        syncBitH = protos[p]['syncBit']['high'] * pulseSeg
                        syncBitL = protos[p]['syncBit']['low'] * pulseSeg

                        # Check for sync bit timing
                        if inTolerance(sigPulse,syncBitH,syncBitL):
                            print("SYNC BIT DETECTED " + p)
                            collect = True
                            break

