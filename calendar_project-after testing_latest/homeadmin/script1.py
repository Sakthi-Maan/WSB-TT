import socket
import pygame
from gtts import gTTS
import tempfile
import os


def get_ip_address():
    """
    Retrieves the IP address of the local machine.

    Returns:
        str: The IP address in dotted-decimal notation.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to a public DNS server
        ip_address = s.getsockname()[0]
        s.close()
    except socket.error:
        ip_address = "Unable to determine IP address"

    return ip_address


def play_ip_address_as_audio(ip_address):
    """
    Converts the IP address to speech and plays it using Pygame.

    Args:
        ip_address (str): The IP address to be spoken.
    """
    # Convert IP address to speech
    tts = gTTS(text=f"My IP address is {ip_address}", lang='en')

    # Save the speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        temp_file_path = temp_file.name

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(temp_file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up and delete the temporary file
    pygame.mixer.quit()
    os.remove(temp_file_path)


if __name__ == "__main__":
    ip = get_ip_address()
    print("IP Address:", ip)

    # Play the IP address as audio
    play_ip_address_as_audio(ip)
