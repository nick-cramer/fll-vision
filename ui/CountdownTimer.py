from datetime import datetime
from threading import Thread
import time
import math

class CountdownTimer:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self, ui, countdown_start):
        self.countdown_start = countdown_start
        self.stopped = False
        self.ui = ui 

    def reset(self):
        self._start_time = datetime.now()
        self.ui.update_time(self.time_label())

    def start(self):
        self.reset()
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            self.ui.update_time(self.time_label())
            time.sleep(1)
        self.stop()

    def stop(self):
        self.stopped = True

    def time_label(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        remain_time = self.countdown_start - elapsed_time
        mins = math.floor(remain_time / 60)
        secs = int(round(remain_time - (mins * 60), 0))
        return str(mins) + ":" + ("0" if secs < 10 else "") + str(secs)
