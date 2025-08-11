from .hand_tracker import TrackHands
from collections import deque
import time

class DetectSwipes(TrackHands):

    def __init__(self, channels, mode=False, complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1,threshold = 300):
        super().__init__(mode, complexity, min_detection_confidence, min_tracking_confidence, max_num_hands)

        self.channels = channels
        self.cords = deque(maxlen=15)
        self.frame_window = 5
        self.channel_idx = 0
        self.last_detection_time = 0
        self.swipe_thresh = threshold

    def detect_swipe(self, frame, draw = False, cooldown = 3):
        
        frame, landmarks, hand_label = self.detect_hands(frame, draw)

        if len(landmarks) == 0:
            return self.channels[self.channel_idx], self.channel_idx
        
        index = landmarks[8]

        index_pos = [index[1], index[2]]

        self.cords.append(index_pos)

        if len(self.cords) < self.frame_window * 2:
            return self.channels[self.channel_idx], self.channel_idx
        
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

        if abs(dx) > self.swipe_thresh and (curr - self.last_detection_time) >= cooldown:
            self.last_detection_time = time.time()
            if hand_label == 'Right':
                self.channel_idx = (self.channel_idx - 1) % len(self.channels)
                print('RIGHT HAND SWIPE DETECTED')
            elif hand_label == 'Left':
                self.channel_idx = (self.channel_idx + 1) % len(self.channels)
                print('LEFT HAND SWIPE DETECTED')
            self.cords.clear()       
    
        return self.channels[self.channel_idx], self.channel_idx