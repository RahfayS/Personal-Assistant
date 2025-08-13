import cv2
from .gestures.volume_controller import VolumeController
from .gestures.hand_tracker import TrackHands
from .gestures.closed_fist import ClosedFist
from frame_utils.preprocess import *
from frame_utils.draw_text import *
from speech_commands.media_commands import MediaCommands
import threading

def media_channel():

    vc = VolumeController()
    hand_tracker = TrackHands()
    fist_tracker = ClosedFist()
    media_speech = MediaCommands()

    def listen_for_speech():
        while True:
            media_speech.media_commands()
            time.sleep(0.5)
    
    threading.Thread(target=listen_for_speech,daemon=True).start()

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
            isPaused,app = fist_tracker.closed_fist(display_frame,landmarks,hand_label)

            if isPaused and app is not None:
                print(f'{app} Paused')

        # Calculate FPS
        fps, prev_time = get_fps(prev_time)
        display_frame = put_text_top_left(display_frame, f'FPS: {int(fps)}')
        # Show frame
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
