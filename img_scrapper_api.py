from bs4 import BeautifulSoup
import requests
import urllib3

from db import ImagesDatabase

# Disable SSL warnings
urllib3.disable_warnings()


class ImageScrapperApi:
    BASE_URL = "https://www.freeimages.com"
    SEARCH_URL = f"{BASE_URL}/search"

    def __init__(self):
        self.images_db = ImagesDatabase("images_db.db")

    def _get_page(self, search_input, page):
        url = f"{self.SEARCH_URL}/{search_input}/{page}"
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def save_image(self, image):
        self.images_db.save_image(image)

    def download_image(self, image_url):
        try:
            response = requests.get(image_url, verify=False)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    def get_images_urls(self, search_input, max_number_of_images):
        page = 1
        images_url_list = []
        while len(images_url_list) < max_number_of_images:
            html_content = self._get_page(search_input, page)
            if html_content is None:
                break  # Stop if there's an error fetching the page
            soup = BeautifulSoup(html_content, "html.parser")
            response = soup.select(
                ".grid-container .grid-item:not(.istock-random) .grid-article a figure picture img"
            )
            image_urls = list(map(lambda x: x.get("src"), response))
            images_url_list.extend(image_urls)

            if len(images_url_list) >= max_number_of_images:
                break  # Stop if we have enough images

            page += 1
        return images_url_list[:max_number_of_images]
