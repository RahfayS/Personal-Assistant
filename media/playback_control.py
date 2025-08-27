import subprocess
import pyautogui
from spotipy.exceptions import SpotifyException



def toggle_play_pause(media_manager):

    context = media_manager.mode
    if context == 'spotify':

        devices = media_manager.spotify_manager.sp.devices()['devices']
        active_devices = [d for d in devices if d['is_active']]

        if active_devices:
            device_id = active_devices[0]['id']
            try:
                state = media_manager.spotify_manager.sp.current_playback()
                if state and state['is_playing']:
                    media_manager.spotify_manager.sp.pause_playback(device_id=device_id)
                else:
                    media_manager.spotify_manager.sp.start_playback(device_id=device_id)
            except SpotifyException as e:
                print(f"Error pausing Spotify: {e}")
        else:
            print("No active Spotify devices to control.")

    elif context == 'youtube':
        pass
    else:

        '''
        Pauses any google chrome application
        '''
        script = '''
        tell application "Google Chrome" to activate
        delay 0.1
        tell application "System Events" to keystroke " "  -- spacebar
        '''
        subprocess.call(['osascript', '-e', script])
