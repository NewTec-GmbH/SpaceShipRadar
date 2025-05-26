"""Path Governor

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
class PathGovernor:
    """Path Governor"""

    load_dotenv()
    image_folder_path = os.getenv('CalibrationFolder_PATH')

    @staticmethod
    def get_path() -> str:
        """returns the path to the img folder of this repo"""
        return PathGovernor.image_folder_path


# Functions ********************************************************************

# Main *************************************************************************

if __name__ == "__main__":
    print(PathGovernor.get_path())
