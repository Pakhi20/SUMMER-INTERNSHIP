import mysql.connector
import os
import csv

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    port=3306,               # use 3306 if you're not on XAMPP
    user="root",
    password="",             # fill in your MySQL password if needed
    database="adavu_internship"
)

cursor = conn.cursor()

# Step 2: Create parent folder 'P_ID'
parent_folder = "P_ID"
os.makedirs(parent_folder, exist_ok=True)

# Step 3: Loop through P01 to P184
for i in range(1, 185):  # 1 to 184 inclusive
    p_id = f'P{i:02d}' if i < 100 else f'P{i}'  # Format: P01 to P099, then P100+

    # Query data for this p_id
    query = """
    SELECT kp_id, startf, endf
    FROM extracted_frames
    WHERE p_id = %s
    """
    cursor.execute(query, (p_id,))
    rows = cursor.fetchall()

    # Skip if no data
    if not rows:
        continue

    # Create subfolder inside P_ID
    subfolder_path = os.path.join(parent_folder, p_id)
    os.makedirs(subfolder_path, exist_ok=True)

    # CSV file path
    csv_file = os.path.join(subfolder_path, f"{p_id.lower()}_data.csv")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["kp_id", "startf", "endf"])
        writer.writerows(rows)

    print(f"✅ Saved {len(rows)} rows to {csv_file}")

# Step 4: Close connections
cursor.close()
conn.close()
