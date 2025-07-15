import os
import cv2
from rembg import remove, new_session

# Use ISNET model for better detail preservation (hair, fingers, etc.)
session = new_session(model_name="isnet-general-use")

# Define folders
input_folder = 'input_images/5'
output_folder = 'output_images/5'

os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_nobg.png')

        print(f"Processing: {file_name}")

        image = cv2.imread(input_path)
        if image is None:
            print(f"❌ Could not read {file_name}")
            continue

        success, encoded = cv2.imencode('.png', image)
        if not success:
            print(f"❌ Failed to encode {file_name}")
            continue

        try:
            output = remove(encoded.tobytes(), session=session)
            with open(output_path, 'wb') as f:
                f.write(output)
            print(f"✅ Saved: {output_path}")
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
