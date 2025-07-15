import os
from rembg import remove
from PIL import Image
import mysql.connector

# ---------- CONFIGURATION ----------
input_folder = r"C:\Users\purba\OneDrive\Desktop\internship\output_frames"
output_folder = r"C:\Users\purba\OneDrive\Desktop\internship\bg_removed"

# Database config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your password if needed
    'database': 'adavu_internship',  # Replace with your database
    'port': 3306  # Change if using XAMPP or custom port
}
# -----------------------------------

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Connect to the database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("✅ Connected to the database.")
except mysql.connector.Error as err:
    print("❌ Database connection failed:", err)
    exit()

# Loop through all images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"no_bg_{filename}")

        try:
            with open(input_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)

            with open(output_path, 'wb') as o:
                o.write(output_data)

            print(f"✅ Background removed and saved: {output_path}")

            # Save to database (optional)
            query = "INSERT INTO processed_images (filename, output_path) VALUES (%s, %s)"
            cursor.execute(query, (filename, output_path))
            conn.commit()

        except Exception as e:
            print(f"❌ Error processing {filename}:", e)

# Close DB connection
cursor.close()
conn.close()
print("✅ All done!")
