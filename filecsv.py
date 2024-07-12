import sqlite3
import csv

# Define the CSV filename
csv_filename = 'csvfile.csv'

# Connect to SQLite database
db_connection = sqlite3.connect('data.db')
cursor = db_connection.cursor()

# Open CSV file for writing
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write headers
    cursor.execute("PRAGMA table_info(users)")
    headers = [description[1] for description in cursor.fetchall()]
    csv_writer.writerow(headers)
    
    # Select data and write rows one by one
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        csv_writer.writerow(row)

# Close cursor and connection
cursor.close()
db_connection.close()

print(f"Data exported successfully to {csv_filename}")
