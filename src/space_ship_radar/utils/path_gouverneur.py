"""Path Gouverneur"""

import os
from dotenv import load_dotenv


class PathGouverneur:
    """Path Gouverneur"""

    load_dotenv()
    image_folder_path = os.getenv('ImageFolder_PATH')

    @staticmethod
    def get_path() -> str:
        """returns the path to the img folder of this repo"""
        return PathGouverneur.image_folder_path


if __name__ == "__main__":
    print(PathGouverneur.get_path())
