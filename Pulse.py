tolerance = 60

class Pulse:
    def __init__(self):
        self.rise = 0 # Rising edge of pulse
        self.fall = 0 # falling edge of pulse
        self.period = 0 # time between two rising edges
        self.width = 0  # time between rising edge and falling edge
