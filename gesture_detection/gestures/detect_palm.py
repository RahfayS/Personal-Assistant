from ..gestures.base import TrackHands
import time
import math
import cv2


class DetectPalm(TrackHands):

    MIN_ANGLE_THRESH = 70
    MAX_ANGLE_THRESH = 100

    FRAME_CAP = 10

    def __init__(self, mode=False, complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1,last_detection_time = 0):
        super().__init__(
            mode=mode,
            complexity=complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            max_num_hands=max_num_hands,
            last_detection_time = last_detection_time
        )

        self.palm_open = False
        self.count = 0
    
        

    def is_palm_open(self,frame,landmarks):
        '''
        Take a frame and detect if a palm is open
        '''

        if landmarks is None:
            return frame, None

        # Access the coords of the landmarks representing finger tips and mcps
        finger_tips = [landmarks[8],landmarks[12],landmarks[16],landmarks[20]]
        finger_mcps = [landmarks[5],landmarks[9],landmarks[13], landmarks[17]]
        finger_pips = [landmarks[6],landmarks[10],landmarks[14],landmarks[18]]


        # Get the angle between each finger tip and their corresponding mcp
        angles = self.find_angle(finger_mcps, finger_pips)
         
        if angles is None:
            return frame, self.palm_open
    
        # If all angles meet the thresholds, a palm is detected
        if all(self.MIN_ANGLE_THRESH <=angle<= self.MAX_ANGLE_THRESH for angle in angles) and  all(tip[2] < mcp[2] for tip,mcp in zip(finger_tips,finger_mcps)):
            self.last_detection_time = time.time()
            self.count += 1

            if self.count == self.FRAME_CAP:
                cv2.putText(frame,f'PALM OPEN',(30,30),cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (255,255,255),2)
                self.palm_open = True
        else:
            self.count = 0
            self.palm_open = False

        return frame, self.palm_open
    
    def find_angle(self,mcps,pips):
        '''
        Takes the finger landmarks, calculates the arctan of two landmarks, returning the angle in degrees
        '''
        angles = []
        for pip,mcp in zip(pips, mcps):
            angle = (math.degrees(math.atan2(pip[2] - mcp[2],pip[1] - mcp[1]))) # The difference of tip_y - mcp_y, tip_x - mcp_x
            # Normalize the angle to be within [0-360)
            angle = (360 - angle) % 360
            angles.append(angle)

        return angles



