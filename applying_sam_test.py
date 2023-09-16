import os
import cv2
from segment_anything import SamPredictor
import torch
from segment_anything import sam_model_registry
import numpy as np
import csv
import matplotlib.pyplot as plt
from tqdm import tqdm

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MODEL_TYPE = "vit_h"

CHECKPOINT_PATH = r'sam_vit_h_4b8939.pth'

sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
sam.to(device=DEVICE)
mask_predictor = SamPredictor(sam)


def show_mask(mask, ax, image_name, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    mask_path = 'masks\\' + image_name.replace('.jpg', '').replace('.png', '')
    np.save(mask_path, mask_image)
    # ax.imshow(mask_image)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))


def resize_image(image, width, height):
    resized_image = cv2.resize(image, (width, height))
    return resized_image


def resize_box(box, original_width, original_height, new_width, new_height):
    ratio_x = new_width / original_width
    ratio_y = new_height / original_height
    resized_box = box * np.array([ratio_x, ratio_y, ratio_x, ratio_y])
    return resized_box.astype(int)


def process_image_with_resizing(image_path, box, target_width, target_height, image_name):
    print(image_path)
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print("Failed to read the image at path:", image_path)
        return

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    resized_image = resize_image(image_rgb, target_width, target_height)
    mask_predictor.set_image(resized_image)

    resized_box = resize_box(box, image_rgb.shape[1], image_rgb.shape[0], target_width, target_height)
    masks, scores, logits = mask_predictor.predict(
        box=resized_box,
        multimask_output=True
    )

    # Display the results

    # plt.figure(figsize=(10, 10))
    # plt.imshow(resized_image)
    show_mask(masks[0], plt.gca(), image_name)
    # show_box(resized_box, plt.gca())
    # plt.axis('off')
    # plt.show()


csv_file = r'bounding_boxes.csv'
with open(csv_file, "r") as file:
    reader = list(csv.reader(file))
    header = reader.pop(0)  # Remove the header row

    # Use tqdm without total argument
    with tqdm() as pbar:
        for row in reader:
            try:
                first_column_value = row[0]
                left, top, right, bottom = map(int, row[1:5])

                IMAGE_PATH = r'images\correct_images\\' + first_column_value

                if not os.path.exists(IMAGE_PATH):
                    print("Image file does not exist at path:", IMAGE_PATH)
                    continue

                print('process_starts')
                target_width = 400  # Set the desired width
                target_height = 400  # Set the desired height

                process_image_with_resizing(IMAGE_PATH, [left, top, right, bottom], target_width, target_height,
                                            first_column_value)

                # Break the loop if you only want to process the first row that has a valid image
                # break
                pbar.update(1)
            except:
                pbar.update(1)
                continue
