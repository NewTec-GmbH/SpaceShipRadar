"""Path Gouverneur

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Variables ********************************************************************

# Classes **********************************************************************


@dataclass
class PathGouverneur:
    """Path Gouverneur"""

    load_dotenv()
    image_folder_path = os.getenv('ImageFolder_PATH')

    @staticmethod
    def get_path() -> str:
        """returns the path to the img folder of this repo"""
        return PathGouverneur.image_folder_path


# Functions ********************************************************************

# Main *************************************************************************

if __name__ == "__main__":
    print(PathGouverneur.get_path())
