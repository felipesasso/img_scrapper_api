import pytest
import sqlite3
from unittest.mock import MagicMock, patch
from img_scrapper_api import ImageScrapperApi
from db import ImagesDatabase

# Sample test data
sample_image_url = "https://www.example.com/image.jpg"
sample_image_data = b"sample_image_data"


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        mock_get.return_value.content = sample_image_data
        yield mock_get


@pytest.fixture
def mock_soup_select():
    urls = [
        "https://www.example.com/image1.jpg",
        "https://www.example.com/image2.jpg",
        "https://www.example.com/image3.jpg",
        "https://www.example.com/image4.jpg",
        "https://www.example.com/image5.jpg",
    ]
    with patch("bs4.BeautifulSoup.select") as mock_select:

        def get_next_url(x):
            return urls.pop(0)

        mock_select.return_value = [MagicMock(get=get_next_url)]
        yield mock_select


@pytest.fixture
def images_db(tmp_path):
    db_path = tmp_path / "test_images_db.db"
    yield ImagesDatabase(str(db_path))


def test_download_image(mock_requests_get):
    api = ImageScrapperApi()
    image_data = api.download_image(sample_image_url)
    assert image_data == sample_image_data


def test_get_images_urls(mock_soup_select):
    api = ImageScrapperApi()
    urls = api.get_images_urls("dog", 5)
    assert len(urls) == 5
    assert urls == [
        "https://www.example.com/image1.jpg",
        "https://www.example.com/image2.jpg",
        "https://www.example.com/image3.jpg",
        "https://www.example.com/image4.jpg",
        "https://www.example.com/image5.jpg",
    ]


def test_save_image(images_db):
    with patch("sqlite3.connect") as mock_connect:
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        images_db.save_image(sample_image_data)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO images(image) VALUES(?)", (sample_image_data,)
        )
