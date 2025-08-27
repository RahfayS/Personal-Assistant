import time
import threading
from media.volume_controller import VolumeController
from media.mute_control import MuteControl
from media.playback_control import toggle_play_pause
from speech.media_commands import MediaCommands
import logging

class MediaController:

    PALM_COOLDOWN = 1  # seconds

    def __init__(self):

        # --- Media Manager Controls ---
        self.vc = VolumeController()
        self.mute_control = MuteControl()
        self.media_manager = MediaCommands()

        self.last_trigger_time = 0
        self.off_screen = False

        # --- Threading Controls ('Hey Jarivs') ---
        self.voice_thread = threading.Thread(target=self.voice_controls)
        self.voice_thread.daemon = True  # so it won’t block exit
        self.voice_thread.start()

        self.command_lock = threading.Lock()

        
    def apply(self, frame, gestures):

        # --- Voice Control ('Hey Jarivs') ---
        if gestures.get('hand_landmarks') is not None:

            if gestures and gestures.get('fist'):
                print("Closed Fist detected, exiting...")
                return
            # --- Volume Control ---
            frame = self.vc.change_volume(frame, gestures['hand_landmarks'])

            # --- Palm (Play/Pause) ---
            if gestures.get('palm') and (time.time() - self.last_trigger_time) >= self.PALM_COOLDOWN:
                toggle_play_pause()
                self.last_trigger_time = time.time()

            # --- Mute (Shush Gesture) ---
            self.mute_control.mute_app(frame, gestures['hand_landmarks'], gestures.get('pose_landmarks'), draw=False)

        # --- Pose (Off-Screen Play/Pause) ---
        if gestures.get('pose_landmarks') is None:
            if not self.off_screen:
                with self.command_lock:
                    toggle_play_pause()
                self.off_screen = True
        else:
            if self.off_screen:
                with self.command_lock:
                    toggle_play_pause()
            self.off_screen = False

        return frame

    def voice_controls(self):
        # --- Voice Control ('Hey Jarivs') ---
        try:
            while True:
                # self.media_manager.on_wake_word()
                if self.media_manager.wake_word_detected:
                    print("Wake word detected! Listening for command...")
                    self.media_manager.perform_commands()
                time.sleep(0.1)  # Small sleep to prevent busy waiting
                    
        except KeyboardInterrupt:
            print("Shutting down...")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            # Clean up resources
            self.media_manager.cleanup()
