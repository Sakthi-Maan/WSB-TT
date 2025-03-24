import os
import mysql.connector

# MySQL connection setup
db_connection = mysql.connector.connect(
    host="localhost",       # e.g., "localhost"
    user="root",   # your MySQL username
    password="root",  # your MySQL password
    database="timebase_sys"  # your database name
)

cursor = db_connection.cursor()

# Directory path where your audio files are located
filecheck = "thirukkuralaudio/Paul/"
audio_dir = "."
count = 1

# files = sorted([f for f in os.listdir(audio_dir) if f.endswith(
#     ".mp3")], key=lambda x: int(x.split('_')[1].split('.')[0]))


count = 1
for file_name in os.listdir:
    # Construct the full path to the audio file
    audio_path = os.path.join(filecheck, file_name)

    # SQL query to update the database with file name and path
    # sql_query = "UPDATE thirukuralaudios SET fileName=%s, audio_path=%s WHERE tid=%s"
    print(f"Inserting {file_name} into the database...", audio_path)
#     sql_query = "INSERT INTO paal (fileName, audio_path) VALUES (%s, %s)"
#     values = (file_name, audio_path)

#     try:
#         cursor.execute(sql_query, values)
#         count += 1
#         db_connection.commit()  # Commit the changes
#         print(f"Inserted {file_name} into the database successfully.")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         db_connection.rollback()  # Rollback in case of error

# # Close the database connection
# cursor.close()
# db_connection.close()
