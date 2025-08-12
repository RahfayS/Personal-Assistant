import cv2
from face_detection_utils import face_detection, get_photos
from .gestures.volume_controller import VolumeController
from .gestures.hand_tracker import TrackHands
from .gestures.closed_fist import ClosedFist
from frame_utils.preprocess import *
from frame_utils.draw_text import *

def gestures():
    vc = VolumeController()
    hand_tracker = TrackHands()
    fist_tracker = ClosedFist()

    prev_time = 0
    cap = cv2.VideoCapture(1)


    while True:
        ret, frame = cap.read()
        if not ret or frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            print('Warn empty frame')
            continue

        frame_rgb = preprocess(frame)
        frame_detect, landmarks, hand_label = hand_tracker.detect_hands(frame_rgb, draw=False)

        # Start with the frame to display
        display_frame = frame_detect

        if len(landmarks) != 0:
            # Control volume gestures
            display_frame = vc.change_volume(display_frame,landmarks)
            # Gesture to close application
            isClosed = fist_tracker.close_app(display_frame,landmarks,hand_label)

            if isClosed:
                print('CLOSE APP')
                break

        # Calculate FPS
        fps, prev_time = get_fps(prev_time)
        display_frame = put_text_top_left(display_frame, f'FPS: {int(fps)}')
        # Show frame
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
