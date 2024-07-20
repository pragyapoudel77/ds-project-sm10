# import sqlite3
# import csv

# # Define the CSV filename
# csv_filename = 'csvfile.csv'

# # Connect to SQLite database
# db_connection = sqlite3.connect('data.db')
# cursor = db_connection.cursor()

# # Open CSV file for writing
# with open(csv_filename, 'w', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)
    
#     # Write headers
#     cursor.execute("PRAGMA table_info(users)")
#     headers = []
#     while True:
#         header = cursor.fetchmany(1)
#         if not header:
#             break
#         headers.append(header[0][1])
#     csv_writer.writerow(headers)
    
#     # Select data and write only the first 10 rows
#     cursor.execute("SELECT * FROM users")
#     rows = cursor.fetchmany(10)  # Fetch only the first 10 rows
#     csv_writer.writerows(rows)

# # Close cursor and connection
# cursor.close()
# db_connection.close()

# print(f"First 10 rows of data exported successfully to {csv_filename}")
import sqlite3
import csv

# Define the SQLite database filename
db_filename = 'data.db'
# Define the CSV filename
csv_filename = 'csvfile.csv'

# Connect to SQLite database
db_connection = sqlite3.connect(db_filename)
cursor = db_connection.cursor()

# Open CSV file for writing
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write headers
    cursor.execute("PRAGMA table_info(users)")
    headers = []
    while True:
        header = cursor.fetchmany(1)
        if not header:
            break
        headers.append(header[0][1])
    csv_writer.writerow(headers)
    
    # Select data and write only the first 10 rows to CSV
    cursor.execute("SELECT * FROM users LIMIT 10")
    while True:
        rows = cursor.fetchmany(10)  # Fetch 10 rows at a time
        if not rows:
            break
        csv_writer.writerows(rows)

# Close cursor and connection
cursor.close()
db_connection.close()

print(f"First 10 rows of data exported successfully to {csv_filename}")
