from gtts import gTTS
from playsound import playsound
import os

# Text to be converted to audio
text = "Hello, this is a test of text to speech conversion."

# Convert text to speech
tts = gTTS(text, lang='en')

# Save the audio file
audio_file = 'output.mp3'
tts.save(audio_file)

# Play the audio file
playsound(audio_file)

# Optionally, remove the audio file after playing
os.remove(audio_file)
