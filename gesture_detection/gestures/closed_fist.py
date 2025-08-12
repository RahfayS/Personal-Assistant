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
    
        
    def close_app(self,frame,landmarks,hand_label):

        # Use the width of the palm as a standard unit of measurement

        wrist, pinky_mcp = landmarks[0], landmarks[17]

            # Get the coords of the landmarks
        wrist_x, wrist_y = wrist[1], wrist[2]
        pinky_x, pinky_y = pinky_mcp[1], pinky_mcp[2]

        # We will use for standard unit of measurement
        width_x = (pinky_x - wrist_x)
        width_y = (pinky_y - wrist_y)

        width_angle = math.atan2(width_y, width_x)

        # Now lets compare some key landmarks relative to palm width
        index_mcp, middle_mcp, ring_mcp, pinky_mcp, = landmarks[5], landmarks[9], landmarks[13], landmarks[17]
        index_pip, middle_pip, ring_pip, pinky_pip = landmarks[6], landmarks[10], landmarks[14], landmarks[19]

        # Find the arc tangent of index_mcp and index_pip

        index_angle = self.calculate_atan(index_mcp,index_pip,width_angle,hand_label)
        middle_angle = self.calculate_atan(middle_mcp,middle_pip,width_angle,hand_label)
        ring_angle = self.calculate_atan(ring_mcp,ring_pip,width_angle,hand_label)
        pinky_angle = self.calculate_atan(pinky_mcp,pinky_pip,width_angle,hand_label)

        angles = [index_angle, middle_angle, ring_angle, pinky_angle]

        isClosed,prev,count = self.closed_fist(angles,frame)

        return isClosed
    
    def calculate_atan(self,lm_1, lm_2,width_angle,hand_label):
        angle = math.atan2(lm_1[2] - lm_2[2], lm_1[1] - lm_2[1])
        angle = math.degrees(angle - width_angle)

        # Noramlize the angle so that it is within [0-360)
        angle = (angle + 360) % 360

        # Convert the angle if the left hand is in frame
        if hand_label == 'Left':
            angle = (360 - angle) % angle
        
        return angle

    def closed_fist(self,angles,frame):

        # Range of angles the will be accepted for mcp/pip relative angle
        MIN = 70
        MAX = 95

        curr = time.time()

        if self.count != 0:
            cv2.putText(frame,f'Exiting... {self.count}/3',(150,70), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255), 2)

        if curr - self.last_detection_time > 3:
            self.count = 0

        for angle in angles:
            if MIN < angle < MAX and (curr - self.last_update_time >= 1.5):
                self.count += 1
                self.last_update_time = curr
                self.last_detection_time = curr


                # If angle is maintained for 3 frames we wil then exit
                if self.count == 3:
                    return True, self.last_update_time,self.count
        return False,self.last_update_time,self.count

