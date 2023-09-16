import requests

def download_image(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there was an error with the request

        with open(file_path, "wb") as file:
            file.write(response.content)

        print("Image downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")

# Example usage
image_url = "https://yandex.ru/images/search?url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F1012387%2Fi4gtmH4LLZfGmokO_4-y6A6438%2Forig&img_url=https%3A%2F%2Fs3-eu-west-1.amazonaws.com%2Fprod-ecs-service-image-api-media%2Fmedia%2Fimages%2Fmodified%2F2%2Faed3c43e89852ef5e113e85fbaf517269e4034ae43fc9e1cddcad97222e671bb.jpg&lr=10493&rpt=imageview&crop_id=0&cbir_id=9567704%2FsVEZToqpkk__ZO6EQGAyGw6442&cbir_page=similar"

save_path = "image.jpg"
download_image(image_url, save_path)
