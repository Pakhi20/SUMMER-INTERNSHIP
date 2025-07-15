import csv
import mysql.connector

# === Step 1: Connect to MySQL ===
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Pakhi@20',
    database='db1'  # replace with your DB name
)
cursor = connection.cursor()

# === Step 2: Open and Read the CSV File ===
csv_file_path = r'C:\Users\purba\OneDrive\Desktop\Bharatnatyam\Combine KP Annotations V2 (1)\Combine KP Annotations V2\Uttsanga\Uttsanga_1\Uttsanga_1_D1_S1.csv'  # replace with your actual path

with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)

    # Skip header if present
    next(reader)  # remove this line if your CSV doesn't have a header

    for row in reader:
        kp_id = row[0]
        start_frame = int(row[1])
        end_frame = int(row[2])

        # Insert into MySQL table
        insert_query = "INSERT INTO adavu_table (kp_id, start_frame, end_frame) VALUES (%s, %s, %s)"
        data = (kp_id, start_frame, end_frame)

        cursor.execute(insert_query, data)

# === Step 3: Commit and Close ===
connection.commit()
print("✅ Data inserted from CSV successfully.")

cursor.close()
connection.close()
