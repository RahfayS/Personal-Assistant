import cv2
from face_detection_utils.detection import *
from face_detection_utils.get_photos import *
from user_data_utils.registration import *
from gesture_control.volume_controller import VolumeController
from gesture_control.hand_tracker import TrackHands
from gesture_control.gesture_utils import *
from frame_utils.preprocess import *
from frame_utils.draw_text import *


def gestures():
    vc = VolumeController()
    hand_tracker = TrackHands()

    prev_time = 0
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            print('Warn empty frame')
            continue

        frame_rgb = preprocess(frame)
        frame_detect, landmarks = hand_tracker.detect_hands(frame_rgb, draw=False)

        # Start with the frame to display
        display_frame = frame_detect

        if len(landmarks) != 0:
            thumb_tip_lm, index_tip_lm = landmarks[4], landmarks[8]
            display_frame, vol = change_volume(display_frame, thumb_tip_lm, index_tip_lm, vc)
            display_frame = put_text_top_right(display_frame, f'VOLUME: {vol}')

        # Calculate FPS
        fps, prev_time = get_fps(prev_time)
        display_frame = put_text_top_left(display_frame, f'FPS: {int(fps)}')
        # Show frame
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
