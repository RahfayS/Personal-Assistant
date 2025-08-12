import cv2
import math
import subprocess
import time
from frame_utils.draw_text import put_text_top_right

class VolumeController:
    def __init__(self):
        self.last_vol = -1
        self.last_update_time = 0

    def change_volume(self, frame,landmarks, draw = True):

        lm_1, lm_2 = landmarks[4], landmarks[8]

        # Get the coords of the landmarks representing the thumb and index finger

        x1, y1 = lm_1[1], lm_1[2]
        x2, y2 = lm_2[1], lm_2[2]

        # Get the cords of the center of the landmarks

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Calculate the length between the circles/landmarks
        length = math.hypot(x2 - x1, y2 - y1)

        # Draw circles on the landmarks, then measure the length between the circles, which we will use to control the volume
        if draw:
            cv2.circle(frame, (x1,y1),10,(255,255,255), cv2.FILLED)
            cv2.circle(frame, (x2,y2),10,(255,255,255), cv2.FILLED)
            cv2.line(frame, (x1,y1), (x2,y2), (0,125,125), 2)
            cv2.circle(frame, (cx,cy),10,(0,255,00), cv2.FILLED)

            if length < 50:
                cv2.circle(frame, (cx,cy),15, (0,0,255), cv2.FILLED)

        vol = self.set_volume(length)

        frame = put_text_top_right(frame, f'VOLUME: {vol}')

        return frame


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

