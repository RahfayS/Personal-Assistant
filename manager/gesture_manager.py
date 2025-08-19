from gestures.base import TrackHands
from gestures.detect_fist import DetectFist
from gestures.detect_palm import DetectPalm
from gestures.detect_pose import DetectPose
from gestures.detect_swipes import DetectSwipes

class GestureManager:
    def __init__(self):
        self.hand_tracker = TrackHands()
        self.fist = DetectFist()
        self.palm = DetectPalm()
        self.swipe = DetectSwipes()
        self.pose = DetectPose()
    
    def process(self, frame):

        hand_landmarks, hand_label = self.hand_tracker.detect_hands(frame)
        pose_landmarks = self.pose.detect_pose(frame)

        closed_fist = self.fist.is_fist_closed(frame,hand_landmarks, hand_label)
        palm_open = self.palm.is_palm_open(frame,hand_landmarks)
        swipe_detected, dx, swipe_label = self.swipe.detect_swipe(frame, hand_landmarks,hand_label)

        return {
            'hand_landmarks':hand_landmarks,
            'hand_label':hand_label,
            'pose_landmarks': pose_landmarks,
            'fist': closed_fist,
            'palm': palm_open,
            'swipe':(swipe_detected,dx,swipe_label)
        }


