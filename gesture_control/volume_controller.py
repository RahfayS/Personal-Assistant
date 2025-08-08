import cv2
import mediapipe as mp
import math
import subprocess
import time

class VolumeController:
    def __init__(self):
        self.last_vol = -1
        self.last_update_time = 0

    def set_volume(self, length):

        # The MAX and min distance we will consider for volume changes
        MAX = 450

        MIN = 50

        if length > MAX:
            length = MAX
        elif length < MIN:
            length = 0
        
        vol_percent = (length / MAX) * 100

        curr_time = time.time()
        # update volume only if volume changed significantly (2%)
        if abs(vol_percent - self.last_vol) >= 0.5:
            # If length remain consistant for 3 seconds then change volume
            if abs(length - 30) > 10 and curr_time - self.last_update_time >= 3:
                subprocess.run(["osascript", "-e", f"set volume output volume {vol_percent}"])
                self.last_vol = vol_percent
                self.last_update_time = curr_time

        
        return int(self.last_vol)