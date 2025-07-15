import os
from rembg import remove
import cv2

# Input and Output folder paths
input_folder = 'C:/Users/purba/OneDrive/Desktop/internship/background_removal_project/input_images/3'
output_folder = 'C:/Users/purba/OneDrive/Desktop/internship/background_removal_project/output_images/3'


# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

print("Reading from:", os.path.abspath(input_folder))
print("Saving to:", os.path.abspath(output_folder))

# Loop through all images in the input folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_nobg.png')

        print(f"Processing: {input_path}")

        # Read image with OpenCV
        image = cv2.imread(input_path)
        if image is None:
            print(f"❌ Cannot read image file: {file_name}, skipping.")
            continue

        # Convert image to bytes
        success, encoded_image = cv2.imencode('.png', image)
        if not success:
            print(f"❌ Encoding failed for: {file_name}, skipping.")
            continue

        try:
            # Remove background
            result = remove(encoded_image.tobytes())

            # Save result
            with open(output_path, 'wb') as out_file:
                out_file.write(result)

            print(f"✅ Saved: {output_path}")
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")
