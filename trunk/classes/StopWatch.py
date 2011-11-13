import time
import math

class StopWatch:
    """
    """
    
    def __init__(self):
        """
        """
        self.startTime = 0
        self.stopTime = 0
        self.duration = 0

    def start(self):
        """
        """
        self.startTime = time.time()

    def stop(self):
        """
        """
        self.stopTime = time.time()

    def reset(self):
        """
        """
        self.startTime = 0
        self.stopTime = 0

    def time(self):
        """
        """
        self.duration = self.stopTime - self.startTime

        return round(self.duration, 2)
