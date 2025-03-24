import mysql.connector
from mysql.connector import Error
import pygame as pyg
import time
import RPi.GPIO as GPIO
import time


dir_path = "/var/www/html/calendar/"

a = str(dir_path)


# def play_audio(audio_path):
#     try:
#         pyg.init()
#         pyg.mixer.init()
#         pyg.mixer.music.load(audio_path)
#         pyg.mixer.music.play()
#         print("Playing audio:", audio_path)
#         while pyg.mixer.music.get_busy():
#             pyg.time.wait(100)
#         time.sleep(2)
#     except Exception as e:
#         print("Error playing audio:", audio_path, e)


# def get_data(bcd_number):
#     try:
#         # Establish a connection to the database
#         connection = mysql.connector.connect(
#             host="localhost",   # Replace with your host
#             user="root",        # Replace with your MySQL username
#             password="root",    # Replace with your MySQL password
#             database="timebase_sys"  # Replace with your database name
#         )
#         if connection.is_connected():
#             cursor = connection.cursor()
#             # Define the SQL query
#             query = "SELECT a_path,p_path,audiopath FROM bcd1 WHERE bcdnumber = %s"
#             # Execute the query with parameter
#             cursor.execute(query, (bcd_number,))

#             # Fetch all results
#             results = cursor.fetchall()

#             # Print each row in the result set
#             for row in results:
#                 for j in row:
#                     play_audio(a+j)

#     except Error as e:
#         print(f"Error: {e}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()


# # Call the function with the desired bcdnumber
# get_data(110)


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
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

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


if __name__ == "__main__":
    BCDThumbwheel().main()
