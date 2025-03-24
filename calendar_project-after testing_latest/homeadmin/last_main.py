import os
import signal
import RPi.GPIO as GPIO
import time
import pygame as pyg
import time
import requests
import mysql.connector
from mysql.connector import Error
import threading
import multiprocessing


"--------------------BCD THUMBWHEEL CODE------------------------------"

API_URL = 'http://localhost/calendar/fetchapi.php'
BASE_DIR = '/var/www/html/calendar/'
BOOT_AUDIO_PATH = BASE_DIR + 'upload/booting_audio.mp3'

AUDIO_QUEUE = True


class BCDThumbwheel:
    def __init__(self):
        self.arr1 = [6, 13, 19, 26]
        self.arr2 = [12, 16, 20, 21]
        self.arr3 = [24, 25, 8, 7]
        self.arr4 = [4, 17, 27, 22]
        self.diff = 15
        self.pushbutton = 5
        self.running = True
        self.dir_path = "/var/www/html/calendar/"

    def setup_pins(self):
        """Sets up GPIO pins as inputs with pull-up resistors."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pushbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in self.arr1 + self.arr2 + self.arr3 + self.arr4:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        time.sleep(0.5)  # Ensure all pins are properly set up

    def read_array(self, arr):
        """Reads the GPIO input values for a given array of pins and calculates the total."""
        total = 0
        for i, pin in enumerate(arr):
            if GPIO.input(pin) == GPIO.HIGH:
                total += 2**i
        return total

    def read_switches(self):
        """Reads all switch arrays and returns the calculated string based on the 'diff' value."""
        total1 = self.read_array(self.arr1)
        total2 = self.read_array(self.arr2)
        total3 = self.read_array(self.arr3)
        total4 = self.read_array(self.arr4)
        return f"{abs(total1 - self.diff)}{abs(total2 - self.diff)}{abs(total3 - self.diff)}{abs(total4 - self.diff)}"

    def handle(self, value):
        if value >= 1 and value <= 1330:
            return value
        elif value >= 2001 and value <= 2133:
            return value
        elif value >= 3001 and value <= 3003:
            return value
        elif value >= 4001 and value <= 4085:
            return value
        else:
            return None

    def get_data(self, bcd_number):
        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(
                host="localhost",   # Replace with your host
                user="root",        # Replace with your MySQL username
                password="root",    # Replace with your MySQL password
                database="timebase_sys"  # Replace with your database name
            )
            if connection.is_connected():
                cursor = connection.cursor()
                # Define the SQL query
                query = "SELECT p_path,a_path,audiopath,t_path FROM bcd1 WHERE bcdnumber = %s"
                # Execute the query with parameter
                cursor.execute(query, (str(bcd_number),))

                # Fetch all results
                results = cursor.fetchall()
                return results

        except Error as e:
            print(f"Error: {e}")

    def play_audio(self, audio_path):
        try:
            pyg.init()
            pyg.mixer.init()
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print("Playing audio:", audio_path)
            while pyg.mixer.music.get_busy():
                pyg.time.wait(100)
            time.sleep(2)
        except Exception as e:
            print("Error playing audio:", audio_path, e)

    def main(self):
        self.setup_pins()
        try:
            while True:
                # Simulate button press
                if GPIO.input(self.pushbutton) == False:
                    switch_value = self.handle(int(self.read_switches()))
                    print("----------------------", switch_value)
                    if isinstance(switch_value, int):
                        data = self.get_data(switch_value)
                        for row in data:
                            p_path, a_path, audiopath, t_path = row
                            paths_to_play = [
                                p_path, a_path, audiopath] + t_path.split(',')

                            for audio_file in paths_to_play:
                                audio_file = audio_file.strip()  # Remove any extra spaces
                                if audio_file:
                                    full_path = f"{dir_path}{audio_file}"
                                    print(switch_value, full_path)
                                    self.play_audio(full_path)
                        time.sleep(0.5)  # Adjust delay for stability
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("GPIO cleanup complete.")


"------------------------------------------------------------------------"


class AudioPlayer:

    def __init__(self, dir_path, thirukkural_api):
        self.dir_path = dir_path
        self.thirukkural_url_api = thirukkural_api
        self.audio_running_status = 0
        self.pause_control = 0
        self.check = 0
        self.init_pygame()
        self.database_connect()

    def play_audio(self, audio_path, flag):
        """Plays a specified audio file using Pygame mixer."""
        try:
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print("Playing audio-path:", audio_path)
            while pyg.mixer.music.get_busy():
                self.check = 1
                while True and flag and self.check:
                    # get data from api and pause or stop audio
                    audio_status = self.thirukkural_playing()
                    if audio_status:
                        pause_status = int(audio_status["audio_pause_status"])
                        stop_status = int(audio_status["audio_stop_status"])
                        if pause_status == 1:
                            pyg.mixer.music.pause()
                            self.pause_control = 1
                            print("Audio Paused by API status",
                                  self.pause_control)
                        elif pause_status == 0 and self.pause_control:
                            pyg.mixer.music.unpause()
                            self.pause_control = 0
                            print("Audio Resumed by API status",
                                  self.pause_control)
                        elif stop_status == 1:
                            pyg.mixer.music.stop()
                            print("Audio stop by API status",
                                  self.pause_control)
                            break
                        elif not pyg.mixer.music.get_busy() and pause_status == 0:
                            self.check = 0
                            print("Audio Finished by API status",
                                  self.pause_control)
        except Exception as e:
            print("Error playing audio:", audio_path, e)

    def init_pygame(self) -> None:
        ''' Default initialization for pygame '''
        print("Pygame is Import")
        pyg.init()
        pyg.mixer.init()

    def thirukkural_playing(self):
        try:
            response = requests.get(self.thirukkural_url_api)
            response.raise_for_status()
            try:
                data = response.json()
                return data
            except ValueError:
                return None
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

    def database_connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",   # Replace with your host
                user="root",        # Replace with your MySQL username
                password="root",    # Replace with your MySQL password
                database="timebase_sys"  # Replace with your database name
            )
            print("Database connection established")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None  # Handle connection failure

    def update_audio_status(self, status: int) -> None:
        ''' Updates the audio_running_status in the database '''
        if self.connection is None:
            print("No database connection available")
            return
        try:
            cursor = self.connection.cursor()

            # Update audio_running_status in the table
            update_query = "UPDATE thirukural_running_status SET audio_running_status = %s WHERE 1"
            cursor.execute(update_query, (status,))
            self.connection.commit()

            print(f"Audio running status updated to: {status}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def main(self):
        while True:
            try:
                thirukkural_data = self.thirukkural_playing()
                if thirukkural_data:
                    thirukkural_paths = [thirukkural_data[key]["audio_path"] for key in thirukkural_data if isinstance(
                        thirukkural_data[key], dict) and "audio_path" in thirukkural_data[key]]
                    for thirukkural in thirukkural_paths:
                        file_path = str(self.dir_path) + thirukkural
                        corrected_path = file_path.replace("\\", "/")
                        self.play_audio(corrected_path, True)
                        time.sleep(0.5)
                    self.update_audio_status(0)
            except KeyboardInterrupt:  # Handle program termination gracefully
                pass  # No cleanup needed for pygame in this case


"------------------------------------------------------------------------"


class ApiManager:

    def __init__(self, url):
        self.init_pygame()
        self.url = url
        self.dir_path = '/var/www/html/calendar/'

    def init_pygame(self) -> None:
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

    def play_audio(self, audio_path):
        if audio_path is None:
            print("No audio data received from API")
            return
        try:
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print("Playing audio:", audio_path)
            while pyg.mixer.music.get_busy():
                pyg.time.wait(100)
            time.sleep(2)
        except Exception as e:
            print("Error playing audio:", audio_path, e)

    def main(self):
        self.play_audio(BOOT_AUDIO_PATH)
        try:
            while True:
                # Check for API data
                audio_data = self.get_data_from_api()

                # Play audio from API response
                if audio_data:
                    for audio_item in audio_data:
                        bell_path = audio_item.get('bell_path',     None)
                        paalpath = audio_item.get('paalpath',   None)
                        adhikaram_path = audio_item.get('adhikaram_path',None)
                        thirukkural_path = audio_item.get(
                            'thirukkural_path', '')
                        new_audio = audio_item.get('audio', '')

                        # Create a list of audio paths that are not empty
                        audio_paths = [path for path in [
                            bell_path, paalpath, adhikaram_path, thirukkural_path,new_audio] if path]
                        

                        print(
                            f"Number of audio files received from API: {audio_paths}")

                        # Play each audio file in the list
                        for audio_path in audio_paths:
                            full_audio_path = str(self.dir_path) + audio_path
                            self.play_audio(full_audio_path)
                        # Sleep after playing all the audio files
                        time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")


"------------------------------------------------------------------------"


def run_worker1():
    Worker1 = BCDThumbwheel()
    Worker1.main()


def run_worker2(dir_path, thirukkural_api):
    Worker2 = AudioPlayer(dir_path, thirukkural_api)
    Worker2.main()


def run_worker0(api_url):
    Worker0 = ApiManager(api_url)
    Worker0.main()


if __name__ == "__main__":
    # Define any parameters you need
    dir_path = "/var/www/html/calendar/"
    thirukkural_api = "http://localhost/calendar/get_audio_api_test.php"
    api_url = 'http://localhost/calendar/fetchapi.php'

    # Create processes for the workers
    process1 = threading.Thread(target=run_worker1)
    process2 = multiprocessing.Process(
        target=run_worker2, args=(dir_path, thirukkural_api))
    thread3 = threading.Thread(target=run_worker0, args=(api_url,))
    # Start the processes
    process1.start()
    process2.start()
    thread3.start()
    # thread3.join()

    try:
        # Wait for the processes to complete
        process1.join()
        process2.join()
        thread3.join()
    except KeyboardInterrupt:
        print("Received keyboard interrupt, terminating all processes...")
        process2.terminate()

    print("All processes have been terminated.")
