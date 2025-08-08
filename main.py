import cv2
from face_detection_utils.detection import *
from face_detection_utils.get_photos import *
from face_detection_utils.encodings import get_encodings
from face_detection_utils.auto_login import auto_login
from user_data_utils.registration import *
from gesture_control.volume_controller import VolumeController
from gesture_control.hand_tracker import TrackHands
from gesture_control.gesture_utils import *
from user_flow.auth import reg_user
from gesture_control.gesture_main import gestures

def main():
    reg_user()
    gestures()




if __name__ == '__main__':
    print('Welcome to realtime face recognition')
    main()