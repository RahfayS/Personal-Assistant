import os
import time
import struct
import logging
import numpy as np
import pyttsx3
import pyaudio
import pvporcupine
import speech_recognition as sr
from dotenv import load_dotenv
import threading

class SpeechCommands:

    COMMAND_BUFFER_SECONDS = 5  # seconds to capture after wake word
    COOLDOWN = 2                # seconds before re-trigger allowed

    def __init__(self, pause_threshold=1, keywords="jarvis", voice_index=1):
        load_dotenv()

        # --- Initialize Speech engine (TTS) --
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        # Set the voice for tts
        if voice_index < len(voices):
            self.engine.setProperty("voice", voices[voice_index].id)

        # --- Initialize Speech recognition ---
        self.r = sr.Recognizer()
        self.pause_threshold = pause_threshold

        # --- Wake Word Initialzation ---
        if isinstance(keywords, str):
            self.keywords = [keywords]
        elif isinstance(keywords, list) and all(isinstance(k, str) for k in keywords):
            self.keywords = keywords
        else:
            raise ValueError("keywords must be a string or list of strings")
        self.wake_word_detected = False
        self.running = True

        # Get Porcupine API key
        self._ACCESS_KEY = os.getenv("PVPORCUPINE_API")
        if not self._ACCESS_KEY:
            raise RuntimeError("Missing Porcupine API key. Set PVPORCUPINE_API in your .env file.")

        # -- Initialize Porcupine Wake Word Detection ---
        self.porcupine = pvporcupine.create(
            access_key=self._ACCESS_KEY,
            keywords=self.keywords
        )
        # --- Initialize PyAudio input ---
        self.pa = pyaudio.PyAudio()
        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length
        

        # We'll create the stream when needed instead of at initialization
        self.stream = None

        # --- Pause / command flags ---
        self.paused_for_command = False
        self.last_trigger_time = 0  # also needed for COOLDOWN
        
        # --- Pause Flag ---
        self.pause_flag = threading.Event()
        self.pause_flag.set()
    
        # --- Start Detecting Wake Word ---
        self.wake_word_thread = threading.Thread(target=self.on_wake_word, daemon=True)
        self.wake_word_thread.start()


        logging.basicConfig(level=logging.INFO)

    # ---------- Text-to-Speech ----------
    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    # ---------- Audio Stream Creation ----------
    def create_stream(self):
        '''Create a new audio stream'''

        # If a stream exits, close it
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        # Create audio stream
        self.stream = self.pa.open(
            rate = self.sample_rate,
            channels=1,
            format = pyaudio.paInt16,
            input = True,
            frames_per_buffer=self.frame_length
        )

        return self.stream


    # ---------- Passive listening ----------
    def listen(self) -> str:
        """Listen for voice input via microphone."""
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            logging.info("Listening...")
            self.r.pause_threshold = self.pause_threshold
            try:
                audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                logging.info("Listening timed out")
                return ""

        try:
            logging.info("Recognizing...")
            query = self.r.recognize_google(audio, language="en-in")
            logging.info(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logging.error(f"Request error: {e}")
            return ""


    # ---------- Buffer recognition ----------
    def recognize_from_buffer(self, audio_buffer, sample_rate):
        """Convert raw PCM buffer into text."""
        audio_data = sr.AudioData(audio_buffer.tobytes(), sample_rate, 2)
        try:
            text = self.r.recognize_google(audio_data, language="en-in")
            logging.info(f"User said: {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logging.error(f"Speech API error: {e}")
            return None

    # ---------- Wake word loop ----------
    def on_wake_word(self, greeting="Hello, what can I do for you?"):
        """Continuously listen for wake word, then buffer command."""
        
        logging.info('Waiting for Jarvis Wake Word')

        # Create the stream for wake word detection
        stream = self.create_stream()
        stream.start_stream()

        while self.running:
            if not self.pause_flag.is_set():
                time.sleep(0.1)  # Small sleep to prevent busy waiting
                continue
            try:
                pcm = stream.read(self.frame_length, exception_on_overflow=False)
                pcm_unpacked = struct.unpack_from("h" * self.frame_length, pcm)
                keyword_index = self.porcupine.process(pcm_unpacked)

                # Wake word detected
                if keyword_index >= 0 and (time.time() - self.last_trigger_time) > self.COOLDOWN:
                    self.last_trigger_time = time.time()
                    logging.info("Wake word detected")
                    self.speak(greeting)
                    self.wake_word_detected = True
                    break
            except Exception as e:
                print(f"Error in wake word detection: {e}")
                # Try to recreate the stream if there's an error
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
                stream = self.create_stream()
                stream.start_stream()
                time.sleep(0.1)  # Prevent tight loop on error
    
        # Clean up the stream when done
        try:
            stream.stop_stream()
            stream.close()
        except:
            pass

