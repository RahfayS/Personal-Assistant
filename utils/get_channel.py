import cv2
from gestures.detect_swipes import DetectSwipes
from utils.preprocess import preprocess
from utils.draw_text import channel_overlay
def get_channel():

    channels = ['Idle','Study','Media']

    swiper_detector = DetectSwipes(channels)

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = preprocess(frame)

        current_channel, current_idx = swiper_detector.detect_swipe(frame,draw = False)
        
        channel_overlay(frame,channels,current_idx, current_channel)

        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        cv2.imshow('Mode Selection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    return current_channel