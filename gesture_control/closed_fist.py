import cv2
import mediapipe as mp
import math
import subprocess
import time
from frame_utils.draw_text import put_text_top_right

class ClosedFist():

    def __init__(self):
        self.last_update_time = 0
        self.count = 0
        self.last_detection_time = 0
    
    def closed_fist(self,angles,frame):

        # Range of angles the will be accepted for mcp/pip relative angle
        MIN = 70
        MAX = 95

        curr = time.time()

        if self.count != 0:
            cv2.putText(frame,f'Exiting... {self.count}/3',(150,70), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 2)

        if curr - self.last_detection_time > 3:
            self.count = 0

        for detected in angles:
            for angle in detected:
                if MIN < angle < MAX and (curr - self.last_update_time >= 1.5):
                    self.count += 1
                    self.last_update_time = curr
                    self.last_detection_time = curr


                    # If angle is maintained for 3 frames we wil then exit
                    if self.count == 3:
                        return True, self.last_update_time,self.count
        return False,self.last_update_time,self.count