from speech.channel_commands import SpeechCommands
from app_utils.spotify_manager import SpotifyManager
from app_utils.youtube_manager import YoutubeManager
import subprocess
import webbrowser
import threading
import logging

class MediaCommands(SpeechCommands):
    """
    Voice-controlled media controller using Playwright.
    Supports YouTube and Spotify with persistent Chrome profile.
    """
    def __init__(self, pause_threshold=1):
        super().__init__(pause_threshold)

        # --- App Managers ---
        self.spotify_manager = SpotifyManager()
        self.youtube_manager = YoutubeManager()
        
        # --- Exit Flag ---
        self.should_exit = False

        # --- Current App Mode ---
        self.mode = None

    def media_commands(self,query):
        """Process voice commands"""

        # If no mode is present, get user to launch one
        if self.mode is None:
            if 'launch youtube' in query:
                self.speak('Launching Youtube')
                self.mode = 'youtube'
                webbrowser.open("https://www.youtube.com")
                return False
            elif 'launch spotify' in query:
                self.speak('Launching Spotify')
                self.mode = 'spotify'
                subprocess.run(['open', '-a', 'Spotify'])
                return False

            elif 'exit' in query or 'stop' in query or 'wrap it up' in query:
                self.speak('Shutting Down Sir')
                return True
            else:
                self.speak("I didn't understand that command. Please try again.")
                return False
        
        # If mode is not none, by pass getting user input
        elif self.mode == 'youtube':
            return self.youtube_manager.youtube_commands(query)
        elif self.mode == 'spotify':
            return self.spotify_manager.spotify_commands(query)

        return False

    def perform_commands(self):

        self.speak('Hello Rahfay What can i get started for you today')

        # Pause wake-word detection
        self.pause_flag.clear()

        exit_program = False
        command_count = 0
        max_commands = 5 # Limit commands per session to prevent infinite loops

        while not exit_program and command_count < max_commands:
            query = self.listen()
            if query:
                exit_program = self.media_commands(query)
                command_count += 1
                # Reset for next wake word detection
        self.pause_flag.set()
        self.wake_word_detected = False
        self.mode = None
        
        # Restart the wake word detection
        self.wake_word_thread = threading.Thread(target=self.on_wake_word, daemon=True)
        self.wake_word_thread.start()

    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()
        if hasattr(self, 'stream'):
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        if hasattr(self, 'pa'):
            self.pa.terminate()


