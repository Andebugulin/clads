import os
import cv2




############# used #################################################################

image_directory = 'images'
correct_images_directory = 'images/correct_images'

# Create the "correct_images" directory if it doesn't exist
os.makedirs(correct_images_directory, exist_ok=True)

# Get the list of image file names in the directory
image_files = os.listdir(image_directory)

for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)

    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Display the image
        cv2.imshow('Image', image)

        # Wait for key press
        key = cv2.waitKey(0)

        if key == ord('f'):
            # Move the image to the "correct_images" directory
            new_image_path = os.path.join(correct_images_directory, image_file)
            os.rename(image_path, new_image_path)
            print(f'Moved {image_file} to the "correct_images" directory.')
        elif key == ord('d'):
            # Delete the image
            os.remove(image_path)
            print(f'Deleted {image_file}.')

    except Exception as e:
        # Skip the image and continue to the next one
        print(f"Error processing {image_file}: {str(e)}")

    # Close the image window
    cv2.destroyAllWindows()
