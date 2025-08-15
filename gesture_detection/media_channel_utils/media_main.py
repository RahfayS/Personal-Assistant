import cv2
import threading
from .volume_controller import VolumeController
from .mute_control import MuteControl
from ..gestures.base import TrackHands
from ..gestures.detect_fist import DetectFist
from ..gestures.detect_palm import DetectPalm
from ..gestures.detect_pose import DetectPose
from .playback_control import toggle_play_pause
from frame_utils.preprocess import *
from frame_utils.draw_text import *
from speech_commands.media_commands import MediaCommands

def media_main():

    vc = VolumeController()
    fist_tracker = DetectFist()
    media_speech = MediaCommands()
    palm = DetectPalm()
    hand_tracker = TrackHands()

    pose = DetectPose()
    mute_control = MuteControl()

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

        # Get the hand landmarks for all gestures
        hand_landmarks, hand_label = hand_tracker.detect_hands(frame_rgb)

        # Detect a fist, if a fist is detected break from webcam
        display_frame, closed_fist = fist_tracker.is_fist_closed(display_frame,hand_landmarks,hand_label)
        if closed_fist:
            break

        # Using index and thumb landmarks, control volume
        display_frame = vc.change_volume(display_frame,hand_landmarks)

        # Detect if a palm is open, if open pause/play
        display_frame, palm_open = palm.is_palm_open(display_frame,hand_landmarks)
        if palm_open and (time.time() - last_trigger_time) > 1:
            toggle_play_pause()
            last_trigger_time = time.time()
        
        # Detect the pose of the user, to identify some key facial landmarks to mute system volume
        pose_landmarks = pose.detect_pose(frame)
        mute_control.mute_app(frame, hand_landmarks, pose_landmarks)
        
        # Calculate FPS and display
        fps, prev_time = get_fps(prev_time)
        display_frame = put_text_top_left(display_frame, f'FPS: {int(fps)}')

        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_RGB2BGR)
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
