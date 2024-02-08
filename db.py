import sqlite3


class ImagesDatabase:
    def __init__(self, path):
        self.path = path

    def save_image(self, image):
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
