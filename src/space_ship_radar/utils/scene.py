"""Scene

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

from dataclasses import dataclass

from utils.found_object_master import FoundObjectMaster
from utils.background_manager import BackgroundManager
from utils.ar_authority import ArAuthority

# Variables ********************************************************************

# Classes **********************************************************************


@dataclass
class Scene():
    """Defines the Setup (pre_main) and the Tracking (main_loop)"""
    # save_index is used as a file suffix for saved images
    save_index = 0
    found_object_master = FoundObjectMaster()
    background_manager = BackgroundManager()
    ar_authority = ArAuthority()

    def __init__(self):
        self.save_index: int = 0


# Functions ********************************************************************

# Main *************************************************************************


if __name__ == "__main__":
    pass
