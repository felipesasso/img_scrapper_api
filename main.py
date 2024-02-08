from concurrent.futures import ThreadPoolExecutor
from img_scrapper_api import ImageScrapperApi


def main():
    scrapper = ImageScrapperApi()
    urls = scrapper.get_images_urls(search_input="dog", max_number_of_images=10)

    def save_images(url):
        image = scrapper.download_image(url)
        scrapper.save_image(image)

    with ThreadPoolExecutor() as executor:
        executor.map(save_images, urls)


if __name__ == "__main__":
    main()
