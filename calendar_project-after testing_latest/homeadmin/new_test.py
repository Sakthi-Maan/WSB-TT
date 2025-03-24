import RPi.GPIO as GPIO
import time
import pygame as pyg
import multiprocessing as mp
import requests

class GpioButton:
    def __init__(self, button_pin, first_audio, second_audio) -> None:
        ''' setup for button_pin and first audio and second audio'''
        self.button_pin = button_pin
        self.first_audio = first_audio
        self.second_audio = second_audio
        self.init_gpio()
        self.init_pygame()
    
    def init_gpio(self)  -> None:
        ''' set gpio pin '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def init_pygame(self)  -> None:
        ''' default init for pygame '''
        pyg.init()
        pyg.mixer.init()
    
    def play_audio(self, audio_path):
        try:
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print("Playing audio:", audio_path)
            while pyg.mixer.music.get_busy():
                pyg.time.wait(100)
            time.sleep(2)
        except Exception as e:
            print("Error playing audio:", audio_path, e)
    
    def main(self)  -> None:
        try:
            while True:
                if GPIO.input(self.button_pin) == False:
                    self.play_audio(self.first_audio)
                    time.sleep(300)
                    self.play_audio(self.second_audio)
        except Exception as K:
            print("Audio not playing error:", K)
        finally:
            pyg.quit()  # Quit Pygame
            GPIO.cleanup()

class ApiWorker:
    def __init__(self,dir_path,url) -> None:
        self.dir_path = dir_path
        self.elapsed_time=0
        self.start_time = 0
        self.end_time = 0
        self.url = url
        self.time_delay=0
        self.init_pygame()
    
    def init_pygame(self)  -> None:
        ''' default init for pygame '''
        pyg.init()
        pyg.mixer.init()
    
    def get_data_from_api(self):
        ''' this localhost api for playing audio in raspberry-pi '''
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except ValueError:
                return None
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            
    def play_audio(self,audio_path):
        """Plays a specified audio file using Pygame mixer."""
        try:
            self.start_time = time.time()
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print("Playing audio:", audio_path)
            while pyg.mixer.music.get_busy():
                pyg.time.wait(100)
                elapsed_time = time.time() - self.start_time
            return elapsed_time
        except Exception as e:
            print("Error playing audio:", audio_path, e)
            
    def main(self):
        try:
            while True:
                # Check for API data
                audio_data = self.get_data_from_api()

                # Play audio from API response
                if audio_data:
                    audio_paths = [audio_item['audio'] for audio_item in audio_data]
                    self.start_time = time.time()
                    for audio_path in audio_paths:
                        self.time_delay += self.play_audio(str(self.dir_path)+audio_path)
                    self.end_time = time.time()
                    print('Song played Time: ',self.end_time - self.start_time)
                    if round(self.end_time - self.start_time) < 60:
                        time.sleep(round( ( 60 - self.time_delay ) + 2))
                    else:
                        time.sleep(1)  # Delay after playing API audio

        except KeyboardInterrupt:  # Handle program termination gracefully
            pass  # No cleanup needed for pygame in this case

        finally:
            pyg.quit()  # Quit Pygame


if __name__ == "__main__":
    button_pin = 17  # Pin for push button
    first_audio = "/var/www/html/calendar/upload/school.mp3"
    second_audio = "/var/www/html/calendar/upload/school.mp3"
    dir_path="/var/www/html/calendar/"
    api_url='http://localhost/calendar/fetchapi.php'
    Worker1 = GpioButton(button_pin, first_audio, second_audio)
    Worker2 = ApiWorker(dir_path,api_url)
    p1 = mp.Process(target=Worker1.main)
    p2 = mp.Process(target=Worker2.main)

    p1.start()
    p2.start()

    # Optionally, join the processes if you want to wait for them to complete
    p1.join()
    p2.join()
