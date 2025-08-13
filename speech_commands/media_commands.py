from .channel_commands import SpeechCommands
import wikipedia
import webbrowser

class MediaCommands(SpeechCommands):

    def __init__(self, pause_threshold=1):
        super().__init__(pause_threshold)

    def media_commands(self):
        query = self.take_commands()

        # Ensure we got a real string
        if not query or not isinstance(query, str):
            return  # No command detected

        query = query.lower()

        if 'wikipedia' in query:
            self.speak('Searching Wikipedia')
            query = query.replace('wikipedia', '').strip()
            if not query:
                self.speak("Please tell me what to search on Wikipedia.")
                return

            try:
                results = wikipedia.summary(query, sentences=2)
                self.speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                self.speak(f"Your query is too vague. Did you mean: {e.options[0]}?")
            except wikipedia.exceptions.PageError:
                self.speak("Sorry, I couldn't find anything on Wikipedia.")
            except Exception as e:
                print("Wikipedia error:", e)
                self.speak("An error occurred while searching Wikipedia.")

        elif 'youtube' in query:
            self.speak('Launching YouTube')
            webbrowser.open('https://youtube.com')
        elif 'white people playlist' in query:
            self.speak('Loading white people playlist')
            webbrowser.open('https://open.spotify.com/playlist/4IXEi7PbuVqKJHJOmPRrCv')
        elif 'spotify dj' in query:
            self.speak('Loading Spotify df')
            webbrowser.open('https://open.spotify.com/search/dj')
        elif 'puppy tail' in query:
            webbrowser.open('https://www.youtube.com/watch?v=-pNGrPhuZ6M')