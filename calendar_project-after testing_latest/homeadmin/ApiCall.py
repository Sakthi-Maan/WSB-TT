import time
import pygame as pyg
import requests
from datetime import datetime, timedelta
import mysql.connector


'''
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)
for check tid and aid and audio playing song 
'''


class ApiWorker:
    def __init__(self, dir_path, url, thirukkural_url) -> None:
        self.dir_path = dir_path
        self.elapsed_time = 0
        self.start_time = 0
        self.end_time = 0
        self.url = url
        self.thirukkural_url_api = thirukkural_url
        self.time_delay = 0
        self.set_volume = 0.8
        self.timeout = 0
        self.connection = None
        self.pause_control = 0
        self.init_pygame()
        self.database_connect()

    def init_pygame(self) -> None:
        ''' Default initialization for pygame '''
        pyg.init()
        pyg.mixer.init(48000, -16, 1, 1024)

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

    def play_audio(self, audio_path, flag):
        """Plays a specified audio file using Pygame mixer."""
        try:
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.set_volume(self.set_volume)
            pyg.mixer.music.play()
            print("Playing audio-path:", audio_path)
            while True and flag:
                # get data from api and pause or stop audio
                audio_status = self.thirukkural_playing()
                pause_status = int(audio_status["audio_pause_status"])
                stop_status = int(audio_status["audio_stop_status"])
                if pause_status == 1:
                    pyg.mixer.music.pause()
                    self.pause_control = 1
                    print("Audio Paused by API status", self.pause_control)
                elif pause_status == 0 and self.pause_control:
                    pyg.mixer.music.unpause()
                    self.pause_control = 0
                    print("Audio Resumed by API status", self.pause_control)
                elif stop_status == 1:
                    pyg.mixer.music.stop()
                    break
                if not pyg.mixer.music.get_busy():
                    print("Audio finished playing.")
                    break  # Exit loop when the audio finishes
        except Exception as e:
            print("Error playing audio:", audio_path, e)

    def main(self):
        try:
            while True:
                # Check for API data
                audio_data = self.get_data_from_api()
                thirukkural_data = self.thirukkural_playing()
                # Play audio from API response
                if audio_data:
                    audio_paths = [audio_item['audio']
                                   for audio_item in audio_data]
                    print(
                        f"number of audio get from api is:  {len(audio_paths)}")
                    for audio_path in audio_paths:
                        self.play_audio(str(self.dir_path)+audio_path, False)
                        print(f"inside loop: {self.time_delay}")
                    time.sleep(60)

                # Check if thirukkural_data is not empty
                if thirukkural_data:
                    # Extract audio paths from thirukkural_data into a list
                    thirukkural_paths = [thirukkural_data[key]["audio_path"] for key in thirukkural_data if isinstance(
                        thirukkural_data[key], dict) and "audio_path" in thirukkural_data[key]]

                    # thirukkural_paths = [audio_item["audio_path"] for audio_item in thirukkural_data]

                    # Print the number of audio paths found
                    print("length of thirukkural is", len(thirukkural_paths))

                    # Iterate over each audio path in the list
                    for thirukkural in thirukkural_paths:
                        # Construct the full file path by combining the directory path with the audio path
                        file_path = str(self.dir_path) + thirukkural

                        # Replace backslashes with forward slashes for compatibility
                        corrected_path = file_path.replace("\\", "/")

                        # Play the audio file using the corrected file path
                        # true is for only for play audio pause and play and stop audio during running time
                        self.play_audio(corrected_path, True)

                        # Pause for 0.5 seconds between audio plays
                        time.sleep(0.5)

                    # Update the audio status to indicate playback has completed

                    self.update_audio_status(0)

        except KeyboardInterrupt:  # Handle program termination gracefully
            pass  # No cleanup needed for pygame in this case

        finally:
            pyg.quit()  # Quit Pygame


if __name__ == "__main__":
    dir_path = "/var/www/html/calendar/"
    api_url = 'http://localhost/calendar/fetchapi.php'
    thirukkural_api = "http://localhost/calendar/get_audio_api_test.php"
    Worker2 = ApiWorker(dir_path, api_url, thirukkural_api)
    Worker2.main()
