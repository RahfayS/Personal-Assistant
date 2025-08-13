import speech_recognition as sr
import pyttsx3

class SpeechCommands():

    def __init__(self,pause_threshold = 1):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

        self.r = sr.Recognizer()
        self.pause_threshold = pause_threshold
    
    def speak(self,audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_commands(self):
        '''
        Takes microphone input from user returning a string output.
        Returns "None" if no voice recognized.
        '''
        try:
            with sr.Microphone() as source:
                print('Listening to User...')
                self.r.pause_threshold = self.pause_threshold
                audio = self.r.listen(source, timeout=5, phrase_time_limit=7)
        except Exception as e:
            print(f"Microphone error: {e}")
            return "None"

        try:
            print('Recognizing...')
            query = self.r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Could not understand audio. Please say that again...")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return "None"

        return query
    