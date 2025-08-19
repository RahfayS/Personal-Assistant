import time
from speech.media_commands import MediaCommands


class ContextManager:
    def __init__(self, refresh_rate = 10):
        self.media_speech = MediaCommands()
        self.last_call = 0
        self.context = 'generic' # Default context
        self.refresh_rate = refresh_rate

    def update(self):
        if (time.time() - self.last_call) > self.refresh_rate:
            app = self.media_speech.get_active_app().lower().strip() # Get the foremost chrome tab
            if 'spotify' == app:
                self.context = 'spotify'
            elif 'youtube' == app:
                self.context = 'youtube'
            self.last_call = time.time()
        
        return self.context