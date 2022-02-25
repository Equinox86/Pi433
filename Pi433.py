import RPi.GPIO as GPIO
import argparse
import time

LISTEN_PIN = 13

class Pulse:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

if __name__ == '__main__':
    
    # Parse args
    parser = argparse.ArgumentParser(description="Listens and sends codes on the 433Mhz band")
    parser.add_argument("-l", "--listen", help="Listen for codes", action="store_true")
    parser.add_argument("-c", "--code", help="Code to transmit")
    args = parser.parse_args()
    # print(args)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LISTEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Listen Flag
    if(args.listen): 
        
        while(True): 
            GPIO.wait_for_edge(LISTEN_PIN, GPIO.RISING)
            rise_time = (time.time()*1000)
            GPIO.wait_for_edge(LISTEN_PIN, GPIO.FALLING)
            fall_time = (time.time()*1000)


    # Send code