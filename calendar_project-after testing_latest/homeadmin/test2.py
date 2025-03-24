import pyttsx3
from gtts import gTTS
import socket
import os
import tempfile
import pygame as pyg

class IPAddressAudio:

    def __init__(self):
        self.init_pygame()
        self.engine = pyttsx3.init()  # Initialize pyttsx3 engine

    def init_pygame(self) -> None:
        ''' Default init for pygame '''
        pyg.init()
        pyg.mixer.init()

    def is_online(self):
        """
        Check if the machine is connected to the internet by trying to connect to a public DNS server.
        Returns:
            bool: True if online, False otherwise.
        """
        try:
            # Try connecting to a well-known public DNS server (Google's DNS server)
            socket.create_connection(("8.8.8.8", 80), timeout=2)
            return True
        except OSError:
            return False

    def play_audio(self, audio_path):
        """ Plays the audio file using pygame """
        try:
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print("Playing audio:", audio_path)
            while pyg.mixer.music.get_busy():
                pyg.time.wait(100)
            time.sleep(2)
        except Exception as e:
            print("Error playing audio:", audio_path, e)

    def get_ip_address(self):
        """
        Retrieves the IP address of the local machine.
        Returns:
            str: The IP address in dotted-decimal notation.
        """
        # Use the actual IP address retrieval logic here
        return "200.172.1.0"

    def play_ip_address_as_audio(self, ip_address):
        """
        Converts the IP address to speech and plays it using either gTTS (online) or pyttsx3 (offline).
        Args:
            ip_address (str): The IP address to be spoken.
        """
        if self.is_online():
            # Online: Use gTTS to convert the IP address to speech
            try:
                tts = gTTS(text=f"My IP address is {ip_address}", lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    tts.save(temp_file.name)
                    temp_file_path = temp_file.name
                self.play_audio(temp_file_path)
                os.remove(temp_file_path)
                print("Played audio using gTTS (online)")
            except Exception as e:
                print("Error using gTTS:", e)
        else:
            # Offline: Use pyttsx3 to convert the IP address to speech
            try:
                self.engine.say(f"My IP address is {ip_address}")
                self.engine.runAndWait()  # Speak the text
                print("Played audio using pyttsx3 (offline)")
            except Exception as e:
                print("Error using pyttsx3:", e)

    def main(self):
        ip_address = self.get_ip_address()  # Fetch the IP address
        self.play_ip_address_as_audio(ip_address)  # Play IP address audio


if __name__ == "__main__":
    Worker0 = IPAddressAudio()
    Worker0.main()
