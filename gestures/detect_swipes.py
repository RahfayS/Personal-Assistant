from gestures.base import TrackHands
from collections import deque
import time
import numpy as np

class DetectSwipes(TrackHands):

    def __init__(self,mode=False, complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1,swipe_threshold = 2.5, window = 5, maxlen = 15, cooldown = 2):
        super().__init__(mode, complexity, min_detection_confidence, min_tracking_confidence, max_num_hands)

        self.cords = deque(maxlen=maxlen)
        self.swipe_thresh = swipe_threshold
        self.cooldown = cooldown
        self.frame_window = window
        self.swipe_detected = False

  
    def detect_swipe(self, landmarks, hand_label, draw=False):
        if landmarks is None:
            return None, None, None

        index_tip = landmarks[8]
        pinky_mcp, index_mcp = landmarks[17], landmarks[5]

        palm_width = abs(np.mean(pinky_mcp[1] - index_mcp[1]))
        print(palm_width)

        index_pos = [index_tip[1], index_tip[2]]
        self.cords.append(index_pos)

        if len(self.cords) < self.frame_window * 2:
            return None, None, None

        start_points = list(self.cords)[:self.frame_window]
        end_points   = list(self.cords)[-self.frame_window:]

        x_start = np.mean([p[0] for p in start_points])
        x_end   = np.mean([p[0] for p in end_points])

        dx = (x_end - x_start) if hand_label == 'Right' else (x_start - x_end)

        curr = time.time()
        if abs(dx) > palm_width * self.swipe_thresh and (curr - self.last_detection_time) >= self.cooldown:
            self.last_detection_time = curr
            self.swipe_detected = True
            self.cords.clear()
        else:
            self.swipe_detected = False

        return self.swipe_detected, dx, palm_width

from gestures.base import TrackHands
from collections import deque
import time

class DetectSwipes(TrackHands):

    def __init__(self,mode=False, complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1,swipe_threshold = 2.5, window = 5, maxlen = 15, cooldown = 2):
        super().__init__(mode, complexity, min_detection_confidence, min_tracking_confidence, max_num_hands)

        self.cords = deque(maxlen=maxlen)
        self.swipe_thresh = swipe_threshold
        self.cooldown = cooldown
        self.frame_window = window
        self.swipe_detected = False

    def detect_swipe(self, frame,landmarks, hand_label, draw = False):
        
        if landmarks is None:
            return None,None,None
        
        index_tip = landmarks[8]
        pinky_mcp, index_mcp = landmarks[17], landmarks[5]

        palm_width = abs(pinky_mcp[1] - index_mcp[1])

        index_pos = [index_tip[1], index_tip[2]]

        self.cords.append(index_pos)

        if len(self.cords) < self.frame_window * 2:
            return None,None,None
        
        x_start, x_end = 0,0

        # Get the cords of the index_tip for the first 5 frame
        start_points = list(self.cords)[:self.frame_window]
        end_points = list(self.cords)[-self.frame_window:]  

        # Get the average position of the starting point of the index finger
        x_start = int(sum(p[0] for p in start_points) / self.frame_window)

        x_end = int(sum(p[0] for p in end_points) / self.frame_window)

        # Get the difference between the points
        dx = x_end - x_start if hand_label == 'Right' else x_start - x_end

        curr = time.time()

        if abs(dx) > palm_width * self.swipe_thresh and (curr - self.last_detection_time) >= self.cooldown:
            self.last_detection_time = time.time()
            self.swipe_detected = True
            self.cords.clear()
                 
        return self.swipe_detected, dx, palm_width

