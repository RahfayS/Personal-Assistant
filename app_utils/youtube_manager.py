from googleapiclient.discovery import build
from app_utils.app_manager import AppManager
from dotenv import load_dotenv
import webbrowser
import re
import os
import logging
import subprocess

class YoutubeManager(AppManager):

    def __init__(self):

        load_dotenv()

        self._api_key = os.getenv('YOUTUBE_API')
        self.youtube = build('youtube','v3',developerKey=self._api_key)

    def search_video(self,query,max_result = 1):
        '''Takes every word after user says "search" and uses it to search youtube video'''
        
        # Get the search term
        search_term = self.search(query)

        # Get request object, that searches the search term, returning a list of videos
        request = self.youtube.search().list(
            q = search_term,
            part = 'id,snippet',
            maxResults = max_result,
            type = 'video'
        )
        # Get the search, and get important info for the search
        response = request.execute()
        for item in response.get('items',[]):
            video_title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            logging.info(f"Launching {video_title} → {video_url}")
            webbrowser.open(video_url)
    
    def play_back(self):
        script = '''
        tell application "Google Chrome" to activate
        delay 0.1
        tell application "System Events" to keystroke " "  -- spacebar
        '''
        subprocess.call(['osascript', '-e', script])


    def youtube_commands(self,query):
        '''Process the users query and preform commands'''

        try:
            if 'pause' in query:
                self.play_back()
            elif 'resume' in query or 'unpause' in query or 'play' in query:
                self.play_back()
            elif 'search' in query:
                self.search_video(query)
        except Exception as e:
            logging.info(f'Youtube command failed: {e}')