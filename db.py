import sqlite3


class ImagesDatabase:
    """
    A class to interact with an SQLite database for storing images.

    Attributes:
    path (str): The file path to the SQLite database.

    Methods:
    save_image(image: bytes) -> None:
        Saves the given image data to the database.

        Args:
        image (bytes): The binary image data to be saved.

        Returns:
        None
    """

    def __init__(self, path: str):
        """
        Initializes the ImagesDatabase object with the specified database file path.

        Args:
        path (str): The file path to the SQLite database.
        """
        self.path = path

    def save_image(self, image: bytes) -> None:
        """
        Saves the given image data to the database.

        Args:
        image (bytes): The binary image data to be saved.

        Returns:
        None
        """
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO images(image) VALUES(?)", (image,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving image to database: {e}")
        finally:
            if conn:
                conn.close()
