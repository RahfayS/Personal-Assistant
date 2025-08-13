import cv2
from .volume_controller import VolumeController
from ..gestures.base import TrackHands
from ..gestures.detect_fist import DetectFist
from ..gestures.detect_palm import DetectPalm
from .playback_control import toggle_play_pause
from frame_utils.preprocess import *
from frame_utils.draw_text import *
from speech_commands.media_commands import MediaCommands
import threading

def media_channel():

    vc = VolumeController()
    fist_tracker = DetectFist()
    media_speech = MediaCommands()
    palm = DetectPalm()
    hand_tracker = TrackHands()

    last_trigger_time = 0


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

        display_frame = frame_rgb.copy()

        landmarks, hand_label = hand_tracker.detect_hands(frame_rgb)

        display_frame, closed_fist = fist_tracker.is_fist_closed(display_frame,landmarks,hand_label)

        if closed_fist:
            break

        display_frame = vc.change_volume(display_frame,landmarks)

        display_frame, palm_open = palm.is_palm_open(display_frame,landmarks)

        if palm_open and (time.time() - last_trigger_time) > 1:
            toggle_play_pause()
            last_trigger_time = time.time()
        

        # Calculate FPS and display
        fps, prev_time = get_fps(prev_time)
        display_frame = put_text_top_left(display_frame, f'FPS: {int(fps)}')

        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_RGB2BGR)
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
