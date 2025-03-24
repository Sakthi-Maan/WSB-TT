import os
import mysql.connector

# MySQL connection setup
db_connection = mysql.connector.connect(
    host="localhost",  # e.g., "localhost"
    user="root",  # your MySQL username
    password="root",  # your MySQL password
    database="timebase_sys"  # your database name
)

cursor = db_connection.cursor()

# Directory path where your audio files are located
filecheck = "thirukkuralaudio/"
audio_dir = "."
count = 1

# Get sorted list of audio files with ".mp3" extension
files = sorted([f for f in os.listdir(audio_dir) if f.endswith(
    ".mp3")], key=lambda x: int(x.split('_')[1].split('.')[0]))

for file_name in files:
    # Construct the full path to the audio file
    var = f"{count:04}"
    audio_path = os.path.join(filecheck, file_name)

    # Corrected SQL query to match your table schema
    sql_query = "INSERT INTO bcd (bcdnumber, audiopath) VALUES (%s, %s)"
    values = (var, audio_path)

    try:
        cursor.execute(sql_query, values)
        count += 1
        db_connection.commit()  # Commit the changes
        print(f"Inserted {file_name} into the database successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db_connection.rollback()  # Rollback in case of error

# Close the database connection
cursor.close()
db_connection.close()
