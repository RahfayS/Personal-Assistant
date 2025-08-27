import logging
import numpy as np
import speech_recognition as sr
import subprocess
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpotifyManager():

    def __init__(self):

        self.__scope = os.getenv('SPOTIPY_SCOPE')
        self.sp = Spotify(auth_manager=SpotifyOAuth(
            client_id= os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret= os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri= os.getenv('SPOTIPY_REDIRECT_URI'),
            scope=self.__scope
        ))
        # --- Retrieve User ID ---
        self.user_id = self.sp.current_user()['id']

        # --- Exit Flag ---
        self.exit = False
    
    def get_active_devices(self):
        devices = self.sp.devices()['devices']
        if not devices:
            logging.info('No Active Device Found')
            return None
        else:
            devices_id = devices[0]['id']
            return devices_id
    
    def spotify_commands(self,query):
        '''Process the users query and preform commands'''

        # Check if any spotify devices are avaliable
        device_id = self.get_active_devices()
        if device_id is None:
            logging.info("Please open Spotify and start a track to control playback.")
            return False
    
        try:
            if 'pause' in query:
                self.sp.pause_playback(device_id=device_id)
                print("Playback paused")
            elif 'resume' in query or 'play' in query:
                self.sp.start_playback(device_id=device_id)
                print("Playback resumed")
            elif 'skip' in query or 'next' in query:
                self.sp.next_track(device_id=device_id)
                print("Skipped to next track")
            elif 'previous' in query:
                self.sp.previous_track(device_id=device_id)
                print("Went to previous track")
            elif 'exit' in query or 'close spotify' in query:
                print('Exiting Spotify mode')
                subprocess.call(["osascript", "-e", 'quit app "Spotify"'])
                return True
            return False
        except Exception as e:
            print(f"Spotify command failed: {e}")
            return False