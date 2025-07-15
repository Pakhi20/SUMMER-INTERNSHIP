import os
import cv2
import numpy as np
import torch
import torchvision.transforms as T
from torchvision import models

# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load pre-trained DeepLabV3+ model
model = models.segmentation.deeplabv3_resnet101(pretrained=True).to(device).eval()

# Folders
input_folder = 'input_images/5'
output_folder = 'output_images/5'
os.makedirs(output_folder, exist_ok=True)

# Image preprocessing
transform = T.Compose([
    T.ToPILImage(),
    T.Resize((520, 520)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

def remove_background(image):
    original_size = image.shape[:2][::-1]

    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)['out'][0]
    output_predictions = output.argmax(0).byte().cpu().numpy()

    # DeepLab class 15 = person
    mask = (output_predictions == 15).astype(np.uint8) * 255
    mask = cv2.resize(mask, original_size)

    # Make transparent image
    b, g, r = cv2.split(image)
    alpha = mask
    result = cv2.merge([b, g, r, alpha])

    return result

# Process all images
for file in os.listdir(input_folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '_clean.png')

        image = cv2.imread(input_path)
        if image is None:
            print(f"❌ Could not read {file}")
            continue

        result = remove_background(image)
        cv2.imwrite(output_path, result)
        print(f"✅ Saved: {output_path}")
