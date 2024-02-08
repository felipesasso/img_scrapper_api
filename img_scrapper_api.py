from bs4 import BeautifulSoup
import requests
import urllib3

from db import ImagesDatabase

# Disable SSL warnings
urllib3.disable_warnings()


class ImageScrapperApi:
    """A class for scraping images from the web and managing them in a database.

    Attributes:
        BASE_URL (str): The base URL of the website to scrape images from.
        SEARCH_URL (str): The URL for conducting search queries.
        images_db (ImagesDatabase): An instance of the ImagesDatabase class for managing images in the database.

    Methods:
        _get_page: Fetches a page with search results for a given query.
        save_image: Saves an image to the database.
        download_image: Downloads an image from a given URL.
        get_images_urls: Retrieves a list of image URLs related to a search query.

    """

    BASE_URL = "https://www.freeimages.com"
    SEARCH_URL = f"{BASE_URL}/search"

    def __init__(self):
        """Initializes an ImageScrapperApi object."""
        self.images_db = ImagesDatabase("images_db.db")

    def _get_page(self, search_input, page):
        """Fetches a page with the results of a search for the given input.

        Args:
            search_input (str): The string to be searched.
            page (int): The page number of the search results.

        Returns:
            str: The HTML content of the page, or None if an error occurs.

        """
        url = f"{self.SEARCH_URL}/{search_input}/{page}"
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def save_image(self, image):
        """Saves the given image to the database.

        Args:
            image (bytes): The image data to be saved.

        Returns:
            None

        """
        self.images_db.save_image(image)

    def download_image(self, image_url):
        """Downloads an image from the given URL.

        Args:
            image_url (str): The URL of the image to be downloaded.

        Returns:
            bytes: The image data, or None if an error occurs.

        """
        try:
            response = requests.get(image_url, verify=False)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    def get_images_urls(self, search_input, max_number_of_images):
        """Returns a list of URLs to images related to the given search input.

        Args:
            search_input (str): The string to be searched.
            max_number_of_images (int): The maximum number of image URLs to be returned.

        Returns:
            List[str]: A list of URLs to images.

        """
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
