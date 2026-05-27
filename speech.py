"""Offline text-to-speech plus microphone speech recognition."""

from __future__ import annotations

import pyttsx3
import speech_recognition as sr


class Speech:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self._prefer_female_voice()

    def _prefer_female_voice(self) -> None:
        voices = self.engine.getProperty("voices") or []
        for voice in voices:
            name = f"{voice.name} {voice.id}".lower()
            if any(label in name for label in ("zira", "female", "woman")):
                self.engine.setProperty("voice", voice.id)
                break

    def say(self, text: str) -> None:
        print(f"Professor: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 8) -> str:
        """Listen to the microphone and return lower-case recognized text."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            print("Listening...")
            audio = self.recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
