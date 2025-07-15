import os
import pandas as pd
import shutil

# Path where all P01-P184 folders with CSVs exist
pid_root = "P_ID"

# Path to the archive where all dance forms exist
root_archive_path = r"C:\Users\purba\OneDrive\Desktop\Bharatnatyam\archive (1)\bharatnatyam_adavu"

# Final output folder for extracted images

output_folder = r"C:\Users\purba\OneDrive\Desktop\Internship\output_frames"

os.makedirs(output_folder, exist_ok=True)

# Helper: find all Color folders under the archive
color_folders = []
for root, dirs, files in os.walk(root_archive_path):
    for dir_name in dirs:
        if dir_name.lower() == "color":
            color_folders.append(os.path.join(root, dir_name))

# Loop through P01 to P184 folders in P_ID
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('(\d+)', s)]

for pid_dir in sorted(os.listdir(pid_root), key=natural_sort_key):
    # Skip if not a Pxx folder
    if not re.match(r'^P\d{2,3}$', pid_dir):
        continue    
    # Construct full path for this Pxx folder   
    
    pid_path = os.path.join(pid_root, pid_dir)
    if not os.path.isdir(pid_path):
        continue

    # Look for CSV file in this Pxx folder
    for file in os.listdir(pid_path):
        if file.endswith(".csv"):
            csv_path = os.path.join(pid_path, file)
            df = pd.read_csv(csv_path)

            for _, row in df.iterrows():
                kp_id = row["kp_id"]
                startf = int(row["startf"])
                endf = int(row["endf"])

                # Destination folder for this kp_id
                kp_folder = os.path.join(output_folder, kp_id)
                os.makedirs(kp_folder, exist_ok=True)

                # Loop through all Color folders to find matching frames
                for color_folder in color_folders:
                    for frame in range(startf, endf + 1):
                        image_name = f"Color_{frame:06d}.png"
                        src_path = os.path.join(color_folder, image_name)
                        dst_path = os.path.join(kp_folder, image_name)

                        if os.path.exists(src_path):
                            shutil.copy(src_path, dst_path)
                            print(f"✅ Copied {image_name} to {kp_folder}")
