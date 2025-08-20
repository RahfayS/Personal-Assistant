import cv2
import math
import subprocess
import time
from collections import deque
from utils.draw_text import put_text_top_right


class VolumeController():

    PINCH_THRESHOLD = 50
    MIN_DISTANCE = 50
    MAX_DISTANCE = 450

    def __init__(self,maxlen = 30, last_pinch_time = 0, display_until = 0):

        self.last_vol = -1
        self.state = "WAITING_FOR_PINCH"
        self.maxlen = maxlen
        self.avg_len = deque(maxlen=maxlen)
        self.last_pinch_time = last_pinch_time
        self.display_message = None
        self.display_until = display_until

    def change_volume(self, frame, landmarks):
        '''
        Detects a pinch, if a pinch is detected an average distance is calculated serving as the slider for volume control
        '''

        if landmarks is None:
            return frame


        distance = self.get_distance(frame, landmarks)

        if self.state == "WAITING_FOR_PINCH":
            if distance < self.PINCH_THRESHOLD and (time.time() - self.last_pinch_time) > 3.5:
                self.state = "COLLECTING_FRAMES"
                self.avg_len.clear()
                self.last_pinch_time = time.time()
                self.show_msg('Raise fingers to Adjust Volume', duration=1)


        elif self.state == "COLLECTING_FRAMES":
            self.avg_len.append(distance)
            current_vol = self.get_current_volume(distance)
            self.show_msg(f'CURRENT VOL:{int(current_vol)} %', duration=1)
            if len(self.avg_len) >= self.maxlen:
                recent_len = list(self.avg_len)[-5:] # Get the last 20 lengths in the deque
                avg_len = sum(recent_len) / len(recent_len)
                vol = self.set_volume(avg_len)
                self.show_msg(f'VOLUME SET: {vol}', duration=3)
                self.state = "WAITING_FOR_RELEASE"

        elif self.state == "WAITING_FOR_RELEASE":
            if distance > self.PINCH_THRESHOLD:
                self.state = "WAITING_FOR_PINCH"
        if self.display_message and time.time() < self.display_until:
            put_text_top_right(frame, self.display_message)

        return frame

    def get_distance(self, frame, landmarks, draw=True):
        '''
        Takes landmarks array and return distance between index tip and thumb tip
        '''
        lm_1, lm_2 = landmarks[4], landmarks[8]
        _, x1, y1 = lm_1
        _, x2, y2 = lm_2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        distance = math.hypot(x2 - x1, y2 - y1)

        if self.state == 'COLLECTING_FRAMES':
            cv2.circle(frame, (x1, y1), 10, (255, 255, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (255, 255, 255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 125, 125), 2)
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
            if distance < self.MIN_DISTANCE:
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                
        return distance

    def get_current_volume(self,length):
        '''
        Takes the current length and returns the volume percentage
        '''

        length = 0 if length < self.MIN_DISTANCE else min(length,self.MAX_DISTANCE)
        vol_percent = (length / self.MAX_DISTANCE) * 100
        # Ensure volume is with [0,100]
        vol_percent = max(0,min(vol_percent, 100))

        return vol_percent

    def set_volume(self, length):
        '''
        Takes the current length and sets the volume
        '''
        vol_percent = self.get_current_volume(length)

        # Update volume only if change in volume is significant
        if abs(vol_percent - self.last_vol) > 1:
            subprocess.run(["osascript", "-e", f"set volume output volume {vol_percent}"])
            self.last_vol = vol_percent
        return int(self.last_vol)

    def show_msg(self, message, duration = 2):
        self.display_message = message
        self.display_until = time.time() + duration