## Usage

To utilize the `ImageScraperApi`, first instantiate an object, then call `get_images_urls()` to retrieve URLs based on your search criteria and the maximum number of images desired. Here's an example:

```python
from image_scraper_api import ImageScraperApi

scraper = ImageScraperApi()
# Retrieve a list of URLs
urls = scraper.get_images_urls(search_input="dog", max_number_of_images=10)
```

You can download an image using `download_image()`:

```python
image = scraper.download_image(url)
```

And save it to the database with:

```python
scraper.save_image(image)
```

## Requirements

After creating your [virtual environment](https://docs.python.org/3/library/venv.html), install the required packages by running:

```sh
$ pip install -r requirements.txt
```

## Migrations

Perform migrations by executing:

```sh
$ alembic upgrade head
``` 

## Testing

To run the tests, execute:

```sh
pytest -v
```
