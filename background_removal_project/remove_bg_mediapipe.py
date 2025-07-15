
import os
import cv2
import mediapipe as mp
import numpy as np

# Create folders if not exist
input_folder = 'input_images/5'
output_folder = 'output_images/5'
os.makedirs(output_folder, exist_ok=True)

# Initialize MediaPipe Selfie Segmentation
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentor = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# Function to remove background and return transparent image
def remove_background(image):
    h, w = image.shape[:2]

    # Convert image to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = segmentor.process(rgb)

    mask = result.segmentation_mask
    condition = mask > 0.5  # Higher = tighter mask, Lower = looser

    # Convert to 4-channel (BGRA)
    image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Set background pixels to transparent
    image_bgra[~condition] = (0, 0, 0, 0)

    return image_bgra

# Loop through all images in the input folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '_nobg.png')

        print(f"Processing: {file_name}")
        image = cv2.imread(input_path)

        if image is None:
            print(f"❌ Failed to read {file_name}, skipping.")
            continue

        output = remove_background(image)
        cv2.imwrite(output_path, output)
        print(f"✅ Saved: {output_path}")
