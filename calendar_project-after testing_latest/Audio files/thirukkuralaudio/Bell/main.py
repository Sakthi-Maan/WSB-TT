import os
import mysql.connector
import time

# MySQL connection setup
db_connection = mysql.connector.connect(
    host="localhost",       # e.g., "localhost"
    user="root",   # your MySQL username
    password="root",  # your MySQL password
    database="timebase_sys"  # your database name
)

cursor = db_connection.cursor()

# Directory path where your audio files are located
filecheck = "thirukkuralaudio/Bell/"
audio_dir = "."

# Start bid at 4001 (BCD-like numbering starting point)
bcd_count = 4001

# Get the list of audio files from the directory
files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".wav")])

for file_name in files:
    # Construct the full path to the audio file
    audio_path = os.path.join(filecheck, file_name)
    
    # Print the audio path and file name
    print(f"Inserting {audio_path} with bid: {bcd_count}")

    # SQL query to insert new records into the bell_audio table
    sql_query = "INSERT INTO bell_audio (bid, bellAudio, bell_path) VALUES (%s, %s, %s)"
    values = (bcd_count, file_name, audio_path)

    try:
        time.sleep(0.5)  # Pause for a short duration between inserts
        cursor.execute(sql_query, values)
        db_connection.commit()  # Commit the changes
        print(f"Inserted {file_name} with bid {bcd_count} successfully.")
    except mysql.connector.Error as err:
        print("---------------------------------------------")
        print(f"Error: {err}")
        db_connection.rollback()  # Rollback in case of error
    
    # Increment the BCD count
    bcd_count += 1

# Close the database connection
cursor.close()
db_connection.close()
