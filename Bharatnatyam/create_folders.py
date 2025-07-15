import os

# Destination path where folders should be created
base_path = r'C:\Users\purba\OneDrive\Desktop\Bharatnatyam\ADAVUS'

# Create folders P1 to P184
for i in range(1, 185):
    folder_name = f'P{i}'
    folder_path = os.path.join(base_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

print("✅ Folders P1 to P184 created successfully.")
