import time
from media.volume_controller import VolumeController
from media.mute_control import MuteControl
from media.playback_control import toggle_play_pause, youtube_skip


class MediaController:

    PALM_COOLDOWN = 1

    def __init__(self):
        self.vc = VolumeController()
        self.mute_control = MuteControl()
        self.last_trigger_time = 0
        self.off_screen = False

    def apply(self,frame,gestures,context):
        
        # --- Fist Detection (Close Webcam) ---
        if gestures['fist']:
            print('Closed Fist detected, exiting...')
            exit(0)
        
        if gestures['hand_landmarks'] is not None:
            # --- Volume Control (Volume Change) ---
            frame = self.vc.change_volume(frame,gestures['hand_landmarks'])
                
            # --- Palm (Play/Pause) ---
            if gestures['palm'] and (time.time() - self.last_trigger_time) >= self.PALM_COOLDOWN:
                toggle_play_pause()
                self.last_trigger_time = time.time()
            
            # --- Mute (Shush Gesture) ---
            self.mute_control.mute_app(frame, gestures['hand_landmarks'],gestures['pose_landmarks'], draw=False)
                
        # --- Pose (Off-Screen Play/Pause)
        if gestures['pose_landmarks'] is None:
            if not self.off_screen:
                print('Pausing')
                toggle_play_pause()
                self.off_screen = True
        else:
            if self.off_screen:
                print('Pausing 2')
                toggle_play_pause()
            self.off_screen = False

        # --- Youtube Gestures --- 
        if context == 'youtube':
            swipe_detected, _, hand_label = gestures['swipe']
            if swipe_detected:
                youtube_skip(hand_label)
        

        return frame