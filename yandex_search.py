from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request

# Set the path to your Yandex Browser executable
yandex_browser_path = r"C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe"

# Specify the URL of the Yandex search page
yandex_search_url = "https://yandex.ru/images/search?source=landing&rpt=imageview"

# Set the path to the image you want to upload
image_path = r"C:\Users\gulin\PycharmProjects\Clothes_Project\clads\images\correct_images\pexels-photo-90365jpegautocompresscstinysrgbdpr1w500_00000416.jpg"

# Configure the Yandex Browser options
options = webdriver.ChromeOptions()
options.binary_location = yandex_browser_path

# Create a WebDriver instance using the ChromeDriver and Yandex Browser options
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open Yandex search page
driver.get(yandex_search_url)
time.sleep(2)
# Find the search input field, type your request, and submit the form
# Find the "Загрузить изображение" button
upload_button = driver.find_element("css selector", "button.Button2_view_action")

# Click on the button to trigger the file upload dialog
upload_button.click()

# Wait for the file upload dialog to appear (you may need to adjust the wait time)
time.sleep(4)

# Type the image path in the file upload dialog and press Enter
container_element = driver.find_element("css selector", "div.CbirPanel-FileControlsBackground")

# Move the mouse cursor to the container element
actions = ActionChains(driver)
actions.move_to_element(container_element).perform()

# Click on the container element to trigger the file upload dialog
container_element.click()

# Wait for the file upload dialog to appear (you may need to adjust the wait time)
time.sleep(2)

# Type the image path in the file upload dialog and press Enter
upload_input = driver.find_element("css selector", "input[type='file']")
upload_input.send_keys(image_path)

# Wait for the image to be uploaded and processed (you may need to adjust the wait time)
time.sleep(4)

# Close the file manager dialog
button_element = driver.find_element("css selector", "button.CropMarkerShape")

# Click on the button
button_element.click()

# Wait for the file manager to close (you may need to adjust the wait time)
time.sleep(5)
div_selector = "div.JustifierRowLayout-Item"
div_element = driver.find_element("css selector", div_selector)
image_url = div_element.find_element("css selector", "a.CbirSimilar-ThumbImage").get_attribute("href")
time.sleep(1)
div_element.find_element("css selector", "a.CbirSimilar-ThumbImage").click()
time.sleep(5)
# Get the image URL from the div element


print(image_url)
# Download the image

file_path =  r"C:\Users\gulin\PycharmProjects\Clothes_Project\clads\items\image.jpg"

time.sleep(3)
# Right-click on the image and save it manually
import pyautogui

# Capture a screenshot of the entire screen


# Right-click on the image and save it manually

time.sleep(1)  # Add a short delay to allow the right-click menu to appear
screenshot = pyautogui.screenshot()

download_link = driver.find_element("link text", "Открыть")


# Click on the download link
download_link.click()
time.sleep(3)

# Switch to the newly opened tab
driver.switch_to.window(driver.window_handles[-1])

# Wait for the image to load (you may need to adjust the wait time)
time.sleep(3)

# Find the image element
image_element = driver.find_element("css selector", "img.MMImage-Origin")

# Get the image source URL
image_url = image_element.get_attribute("src")
print(image_url)

# Close the browser
driver.quit()

