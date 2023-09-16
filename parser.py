from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

### used already
################################
################################
################################

IMAGE_COUNTER = 0
IMAGE_FOLDER_PATH = r'images/'

# Configure Selenium webdriver options
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (without opening a browser window)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Path to your Chrome webdriver executable

def parse_images(url):
    # Instantiate Chrome webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Access the URL and let the page load
    driver.get(url)
    time.sleep(5)  # Adjust the delay as needed to allow the initial page to load completely

    images = driver.find_elements_by_tag_name('img')

    num_images_downloaded = 0
    while num_images_downloaded < 10000:
        prev_num_images = len(images)

        # Scroll down to trigger loading more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the delay as needed to allow new images to load

        images = driver.find_elements_by_tag_name('img')

        # Check if new images were loaded
        if len(images) == prev_num_images:
            break

        with tqdm(total=len(images) - num_images_downloaded, desc="Downloading Images") as pbar:
            for i in range(num_images_downloaded, len(images)):
                image = images[i]
                image_url = image.get_attribute('src')
                if image_url:
                    download_image(image_url)
                    num_images_downloaded += 1
                    pbar.update(1)
                time.sleep(0.5)  # Add a delay of 0.5 seconds between requests

        # Break if the maximum number of images has been reached
        if num_images_downloaded >= 10000:
            break

    # Quit the webdriver after scraping
    driver.quit()


import re


def sanitize_filename(filename):
    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename


def download_image(url):
    global IMAGE_COUNTER
    response = requests.get(url)
    content_type = response.headers.get('content-type')

    # Extract the file extension from the content type
    if 'jpeg' in content_type:
        extension = 'jpg'
    elif 'png' in content_type:
        extension = 'png'
    else:
        # If the content type is unknown, use the 'jpg' extension as a fallback
        extension = 'jpg'

    filename = url.split('/')[-1]  # Extract filename from URL
    filename = sanitize_filename(filename)

    with open(IMAGE_FOLDER_PATH + filename + '_' + (8 - len(str(IMAGE_COUNTER))) * '0' + str(
            IMAGE_COUNTER) + '.' + extension, 'wb') as f:
        f.write(response.content)

    IMAGE_COUNTER += 1
    print(f"Downloaded: {filename}.{extension}")


# Usage example
parse_images('https://www.pexels.com/search/person%20in%20shoes/')
