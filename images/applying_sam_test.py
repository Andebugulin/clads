import os
import cv2
from segment_anything import SamPredictor
import torch
from segment_anything import sam_model_registry
import numpy as np
import csv
import matplotlib.pyplot as plt

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MODEL_TYPE = "vit_h"

CHECKPOINT_PATH = r'C:/Users/gulin/PycharmProjects/Clothes_Project/clads/sam_vit_h_4b8939.pth'

sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
sam.to(device=DEVICE)
mask_predictor = SamPredictor(sam)


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))


csv_file = r'C:/Users/gulin/PycharmProjects/Clothes_Project/clads/bounding_boxes.csv'
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    for row in reader:
        first_column_value = row[0]
        left, top, right, bottom = map(int, row[1:5])

        IMAGE_PATH = r'C:\Users\gulin\PycharmProjects\Clothes_Project\clads\images\correct_images\\' + first_column_value

        if not os.path.exists(IMAGE_PATH):
            print("Image file does not exist at path:", IMAGE_PATH)
            continue

        image_bgr = cv2.imread(IMAGE_PATH)
        if image_bgr is None:
            print("Failed to read the image at path:", IMAGE_PATH)
            continue

        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        mask_predictor.set_image(image_rgb)

        box = np.array([left, top, right, bottom])
        masks, scores, logits = mask_predictor.predict(
            box=box,
            multimask_output=True
        )

        # Display the results

        plt.figure(figsize=(10, 10))
        plt.imshow(image_rgb)
        show_mask(masks[0], plt.gca())
        show_box(box, plt.gca())
        plt.axis('off')
        plt.show()

        # Break the loop if you only want to process the first row that has a valid image
        break
