import os
import csv
import cv2

data_dir = "images/correct_images"
output_file = "bounding_boxes.csv"

# Create an empty list to store the bounding box coordinates and filenames
bounding_boxes = []

# Iterate through the images in the directory
for filename in os.listdir(data_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Adjust the file extensions if necessary
        image_path = os.path.join(data_dir, filename)

        # Open the image
        image = cv2.imread(image_path)

        # Display the image and allow the user to select bounding boxes

        cv2.imshow("Image", image)

        key = cv2.waitKey(0)
        if key == ord("p"):
            os.remove(image_path)
            continue
        elif key != ord('p'):

            bounding_box = cv2.selectROI("Image", image)
            cv2.destroyAllWindows()

            # Get the coordinates of the bounding box
            left, top, width, height = bounding_box
            right = left + width
            bottom = top + height

            # Add the coordinates and filename to the list
            bounding_boxes.append({
                "filename": filename,
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom
            })

            print(left, top, right, bottom)





# Write the bounding boxes to a CSV file
with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["filename", "left", "top", "right", "bottom"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(bounding_boxes)
