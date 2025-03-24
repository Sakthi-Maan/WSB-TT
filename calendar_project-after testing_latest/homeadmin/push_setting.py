import RPi.GPIO as GPIO
import time
import pygame as pyg
import requests
from datetime import datetime,timedelta
import pyttsx3 as pk


class GpioButton:
    def __init__(self, button_pin,button_pin2,start_audio,api_url,update_api) -> None:
        ''' setup for button_pin and first audio and second audio'''
        self.button_pin = button_pin
        self.update_api = update_api
        self.second_interval = 30 
        self.first_audio = 0
        self.second_audio = 0
        self.middle_audio = None
        self.start_audio = start_audio
        self.button_pin2= button_pin2
        self.button_status = 0 
        self.timeInterval = 0
        self.timeout = 0
        self.flag=True
        self.count = 0
        self.set_volume = 0.8
        self.second_control = False
        self.Test = False
        self.api_url = api_url
        self.date_time_anno = True
        self.engine = 0
        self.init_gpio()
        self.init_pygame()
        self.init_pyttsx3()
    
    def init_gpio(self)  -> None:
        ''' set gpio pin '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_pin2, GPIO.OUT)
        
    def gpio_test(self):
        try:
            self.play_audio(self.first_audio)
        except Exception as Fr:
            print('Self Test Error Because',Fr)
            
    def init_pyttsx3(self):
        self.engine = pk.init()
        self.engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        self.engine.setProperty('volume', 1.0)  
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id) 
    
    def announce_audio(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def play_date_time(self):
        now = datetime.now()
        formatted_date = now.strftime("%B %d %Y")  # June 18 2024
        formatted_time = now.strftime("%H:%M")  # 06:00 (assuming 24-hour format)
        text = (f"Today is {formatted_date} and {formatted_time} clock")
        self.announce_audio(text)
            
    def check_api(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # This will raise an HTTPError for bad responses
            try:
                data = response.json()
                return data
            except ValueError as json_error:  # This catches JSON decoding errors
                print('Failed to parse JSON response:', json_error)
        except requests.exceptions.RequestException as request_error:  # This is a base class for all requests exceptions
            print("API request failed:", request_error)
            
            
    def update_audio(self):
        data = self.check_api()
        if data:
            self.first_audio = "/var/www/html/calendar/"+ data[0]['start_audio']
            self.second_audio = "/var/www/html/calendar/" + data[0]['end_audio']
            self.middle_audio = "/var/www/html/calendar/" + data[0]['middle_audio']
            self.button_status = int(data[0]['button_status'])
            self.timeInterval = int(data[0]['time_interval'])
            self.Test = int(data[0]['selftest'])
            if int(self.Test) == 1:
                self.gpio_test()
        else:
            self.first_audio = "/var/www/html/calendar/upload/audioBell/664b204854b73.mp3"
            self.second_audio = "/var/www/html/calendar/upload/audioBell/664b204854b73.mp3"
            self.middle_audio = "/var/www/html/calendar/upload/audioBell/664b204854b73.mp3"
            self.button_status = 0
            self.timeInterval = 5
            self.Test = 0
    
    def init_pygame(self)  -> None:
        ''' default init for pygame '''
        pyg.init()
        pyg.mixer.init()
    
    def play_audio(self, audio_path):
        try:
            pyg.mixer.music.load(audio_path)
            GPIO.output(self.button_pin2, GPIO.LOW)
            pyg.mixer.music.play()
            pyg.mixer.music.set_volume(self.set_volume)
            print("Playing audio:", audio_path)
            while pyg.mixer.music.get_busy():
                pyg.time.wait(100)
            time.sleep(2)
            GPIO.output(self.button_pin2, GPIO.HIGH)
        except Exception as e:
            print("Error playing audio:", audio_path, e)
    
    def main(self)  -> None:
        try:
            self.play_audio(self.start_audio)
            while True:
                now = datetime.now()
                current_time = now.strftime("%H:%M")  # Format current time as h:m
                self.update_audio()
                print(current_time,current_time=="5:15")
                # if current_time == "05:15" or current_time == "18:15":
                #     print("starting auto")
                #     self.play_date_time()
                #     time.sleep(60)
                if str(self.timeout) == current_time:
                    print('finallly audio for finish')
                    self.play_audio(self.second_audio)
                    self.flag = True
                    self.second_control = False
                    self.timeout = 0
                    print('finaalyy is finsish and next')
                if GPIO.input(self.button_pin) == False:
                    print("Playing is audio. First Time")
                    if self.flag:
                        self.play_audio(self.first_audio)
                        self.flag = False
                        self.second_control = True
                        self.count = (int(self.timeInterval)*2)-2
                        new_time = datetime.now() + timedelta(minutes=int(self.timeInterval))
                        formatted_new_time = new_time.strftime("%H:%M")
                        self.timeout = str(formatted_new_time)
                        print(f"self count is {self.count} and time interval {self.timeInterval}")
                if self.second_control and self.button_status:
                    while self.count:
                        print('30 second start and playing')
                        start = time.perf_counter()  # High-resolution timer
                        while time.perf_counter() - start < 30.0:  
                            pass                      #for every second the maintain the record
                        print(self.middle_audio)
                        self.play_audio(self.middle_audio)
                        print("30 second count is playing",self.count)
                        self.count-=1
                    self.second_control = False
                    
        except Exception as K:
            print("Audio not playing error:", K)
        finally:
            pyg.quit()  # Quit Pygame
            GPIO.cleanup()

if __name__ == "__main__":
    button_pin = 17  # Pin for push button
    button_pin2 = 14 # Pin for led
    start_audio = "/var/www/html/calendar/upload/booting_audio.mp3"
    api_url = "http://localhost/calendar/gpio_api.php"
    update_api = "http://localhost/calendar/gpio.php"
    Worker1 = GpioButton(button_pin,button_pin2,start_audio,api_url,update_api)
    Worker1.main()