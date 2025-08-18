import cv2
import time
from gestures.detect_swipes import DetectSwipes
from utils.preprocess import preprocess
from utils.draw_text import channel_overlay

class ChangeModes():

    def __init__(self,channels,swipe_thresh = 2.5, cooldown = 2):
        self.channels = channels
        self.channel_idx = 0
        self.last_detection_time = 0
        self.swipe_thresh = swipe_thresh
        self.cooldown = cooldown
    
    def switch_mode(self,dx,palm_width,hand_label):

        curr = time.time()

        if abs(dx) > palm_width * self.swipe_thresh and (curr - self.last_detection_time) >= self.cooldown:
            self.last_detection_time = time.time()
            if hand_label == 'Right':
                self.channel_idx = (self.channel_idx - 1) % len(self.channels)
                print('RIGHT HAND SWIPE DETECTED')
            elif hand_label == 'Left':
                self.channel_idx = (self.channel_idx + 1) % len(self.channels)
                print('LEFT HAND SWIPE DETECTED') 

        return self.channels[self.channel_idx], self.channel_idx



def get_channel():

    channels = ['Idle','Study','Media']

    current_idx = 0
    current_channel = channels[current_idx]

    swiper_detector = DetectSwipes()
    change_modes = ChangeModes(channels)

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = preprocess(frame)
        landmarks, hand_label = swiper_detector.detect_hands(frame)
        swipe_detected ,dx,palm_width = swiper_detector.detect_swipe(frame,landmarks, hand_label)
        if dx is not None:
            current_channel, current_idx = change_modes.switch_mode(dx,palm_width,hand_label)
        
        channel_overlay(frame,channels,current_idx, current_channel)

        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        cv2.imshow('Mode Selection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    return current_channel