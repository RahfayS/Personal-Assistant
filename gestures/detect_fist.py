import math
from gestures.base import TrackHands
import cv2
import time
class DetectFist(TrackHands):

    MIN_ANGLE_THRESHOLD = 165
    MAX_ANGLE_THRESHOLD = 185

    MIN_DISTANCE_THRESHOLD = 0.5
    MAX_DISTANCE_THRESHOLD = 0.75

    def __init__(self, mode=False, complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1,last_detection_time = 0):
        super().__init__(
            mode=mode,
            complexity=complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            max_num_hands=max_num_hands,
            last_detection_time = last_detection_time
        )

        self.fist_closed = False
        self.count = 0
    
    def is_fist_closed(self,frame,landmarks,hand_label):
        '''
        Take a frame and detect if a fist is closed
        '''
        if landmarks is None:
            return None
        
        # get the landmarks for pip, mcps
        finger_pips = [landmarks[6], landmarks[10], landmarks[14]]
        finger_mcps = [landmarks[5], landmarks[9], landmarks[13]]

        # Calculate the width of the palm, to normalize the distances between landmarks
        wrist,pinky_mcp = landmarks[0],landmarks[17]
        palm_width = math.hypot(wrist[1] - pinky_mcp[1],wrist[2] - pinky_mcp[2])
        

        angles,distances = self.find_distances_angles(finger_mcps,finger_pips,palm_width,hand_label)


        if all(self.MIN_ANGLE_THRESHOLD < angle < self.MAX_ANGLE_THRESHOLD for angle in angles) and all(self.MIN_DISTANCE_THRESHOLD < distance < self.MAX_DISTANCE_THRESHOLD for distance in distances):
            self.count += 1
            self.fist_detected = True
            cv2.putText(frame, f'Exiting... {self.count} / 5', (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)


            # If the 10 consecutive frames meet the thesholds, the fist is closed
            if self.count == 5:
                self.fist_closed = True
        else:
            self.count = 0
            self.fist_closed = False
        
        return self.fist_closed
    
    def find_distances_angles(self,mcps,pips,width,hand_label):
        '''
        Takes the finger landmarks, calculates the arctan of two landmarks, returning the angle in degrees and getting the normalized distance between landmarks
        '''
        angles = []
        distances = []
        for pip, mcp in zip(pips, mcps):

            pip_x, pip_y = pip[1], pip[2]
            mcp_x, mcp_y = mcp[1], mcp[2]

            if hand_label == 'Left':
                pip_x = -pip_x
                mcp_x = -mcp_x
            
            angle = math.degrees(math.atan2(pip_y - mcp_y, pip_x - mcp_x))
            angle = (angle + 360) % 360  # normalize to 0–360
            angles.append(angle)

            distances.append((math.hypot(mcp_x - pip_x, mcp_y - pip_y)/width)) # normalize relative to palm widths


        return angles,distances

    



