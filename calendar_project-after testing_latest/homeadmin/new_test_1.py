import os
import signal
import RPi.GPIO as GPIO
import time
import pygame as pyg
import requests
import mysql.connector
from mysql.connector import pooling
import threading
import multiprocessing



import pygame as pyg
import requests
import mysql.connector
from mysql.connector import pooling
import time


class AudioPlayer:
    def __init__(self, dir_path, thirukkural_api):
        self.dir_path = dir_path
        self.thirukkural_url_api = thirukkural_api
        self.audio_running_status = 0
        self.pause_control = 0
        self.check = 0
        self.pool = None

        self.init_pygame()
        self.setup_database_pool()

    def play_audio(self, audio_path, check_api=True):
        """Plays a specified audio file using Pygame mixer with API control."""
        try:
            pyg.mixer.music.load(audio_path)
            pyg.mixer.music.play()
            print(f"Playing audio-path: {audio_path}")

            while pyg.mixer.music.get_busy():
                if check_api:
                    audio_status = self.get_audio_status_from_api()
                    if audio_status:
                        self.handle_audio_controls(audio_status)
        except Exception as e:
            print(f"Error playing audio: {audio_path}, {e}")
        finally:
            pyg.mixer.music.unload()

    def handle_audio_controls(self, audio_status):
        """Handles pause, resume, and stop controls based on API status."""
        pause_status = int(audio_status.get("audio_pause_status", 0))
        stop_status = int(audio_status.get("audio_stop_status", 0))

        if pause_status == 1 and not self.pause_control:
            pyg.mixer.music.pause()
            self.pause_control = 1
            print("Audio Paused by API")
        elif pause_status == 0 and self.pause_control:
            pyg.mixer.music.unpause()
            self.pause_control = 0
            print("Audio Resumed by API")

        if stop_status == 1:
            pyg.mixer.music.stop()
            print("Audio Stopped by API")

    def init_pygame(self):
        """Initializes Pygame and the mixer."""
        print("Pygame initialized.")
        pyg.init()
        pyg.mixer.init()

    def get_audio_status_from_api(self):
        """Fetches the current audio status from the API."""
        
        try:
            response = requests.get(self.thirukkural_url_api) 
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None

    def setup_database_pool(self):
        """Sets up a MySQL connection pool."""
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                pool_reset_session=True,
                host="localhost",
                user="root",
                password="root",
                database="timebase_sys"
            )
            print("Connection pool created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating connection pool: {err}")
            self.pool = None

    def update_audio_status(self, status: int):
        """Updates the audio running status in the database."""
        if not self.pool:
            print("No database connection pool available.")
            return

        try:
            with self.pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    update_query = "UPDATE thirukural_running_status SET audio_running_status = %s WHERE 1"
                    cursor.execute(update_query, (status,))
                    connection.commit()
                    print(f"Audio running status updated to: {status}")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def main(self):
        """Main loop for fetching and playing audio from the API."""
        while True:
            try:
                thirukkural_data = self.get_audio_status_from_api()
                if thirukkural_data:
                    for key, value in thirukkural_data.items():
                        if isinstance(value, dict) and "audio_path" in value:
                            file_path = f"{self.dir_path}/{value['audio_path']}".replace("\\", "/")
                            self.play_audio(file_path)
                            time.sleep(0.5)  # Ensure slight delay between tracks

                    # Update audio status after each playback
                    self.update_audio_status(0)
            except KeyboardInterrupt:
                print("Terminating process...")
                break


"-------------------------------------------------------------------------------------"


def run_worker2(dir_path, thirukkural_api):
    """Function to run the AudioPlayer worker process."""
    worker = AudioPlayer(dir_path, thirukkural_api)
    worker.main()




if __name__ == "__main__":
    api_url = 'http://localhost/calendar/fetchapi.php'
    dir_path = "/var/www/html/calendar/"
    thirukkural_api = "http://localhost/calendar/get_audio_api_test.php"

    # player = BCDThumbwheel(dir_path,api_url)
    # player.main()
    process1 = threading.Thread(target=run_worker2, args=(dir_path, thirukkural_api))
    process1.start()
    process1.join()

    # process2 = multiprocessing.Process(
    #     target=run_worker2, args=(dir_path, thirukkural_api))
    # process2.start()
    # try:
    #     # Wait for the processes to complete
    #     process2.join()
    # except KeyboardInterrupt:
    #     print("Received keyboard interrupt, terminating all processes...")
    #     process2.terminate()

    print("All processes have been terminated.")