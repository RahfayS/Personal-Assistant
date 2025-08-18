import cv2
import threading
from media.volume_controller import VolumeController
from media.mute_control import MuteControl
from gestures.base import TrackHands
from gestures.detect_fist import DetectFist
from gestures.detect_palm import DetectPalm
from gestures.detect_pose import DetectPose
from gestures.detect_swipes import DetectSwipes
from .playback_control import toggle_play_pause,youtube_skip
from utils.preprocess import *
from utils.draw_text import *
from speech.media_commands import MediaCommands

def media_main():

    vc = VolumeController()
    fist_tracker = DetectFist()
    media_speech = MediaCommands()
    palm = DetectPalm()
    hand_tracker = TrackHands()
    swipe = DetectSwipes()
    pose = DetectPose()
    mute_control = MuteControl()

    last_trigger_time = 0

    last_call = 0
    
    off_screen = False


    FIRST_IGNORE_TIME = 1

    
    '''
    def listen_for_speech():
        while True:
            media_speech.media_commands()
            time.sleep(1)

    threading.Thread(target=listen_for_speech,daemon=True).start()

    '''

    def get_context():
        app = media_speech.get_active_app()
        if 'spotify' in app:
            context = 'spotify'
        elif 'youtube' in app:
            context = 'youtube'
        else:
            context = 'generic'

        return context
    
    prev_time = 0
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            print('Warn empty frame')
            continue

        frame_rgb = preprocess(frame)

        if frame_rgb is None:
            break

        display_frame = frame_rgb.copy()

        # Get the hand landmarks for all gestures
        hand_landmarks, hand_label = hand_tracker.detect_hands(frame_rgb)

        current_time = time.time()

        # Detect a fist, if a fist is detected break from webcam
        closed_fist, fist_detected = fist_tracker.is_fist_closed(display_frame,hand_landmarks,hand_label)
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
        pose_landmarks = pose.detect_pose(display_frame,draw = False)

        if pose_landmarks is None:
            if not off_screen:
                off_screen = True
                toggle_play_pause()
        else:
            if off_screen:
                toggle_play_pause()
            off_screen = False

        if time.time() - last_call >= 10:
            context = get_context()
            last_call = time.time()
            print(context)

        if context == 'youtube':
            swipe_detected,dx, hand_label = swipe.detect_swipe(frame,hand_landmarks,hand_label)
            if swipe_detected:
                print('SWIPE DETECTED')
                youtube_skip(hand_label)
                
        mute_control.mute_app(display_frame, hand_landmarks, pose_landmarks,draw=False)

        # Calculate FPS and display
        fps, prev_time = get_fps(prev_time)
        put_text_top_left(display_frame, f'FPS: {int(fps)}')

        display_frame = cv2.cvtColor(display_frame,cv2.COLOR_RGB2BGR)
        cv2.imshow('Gesture Detection', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
