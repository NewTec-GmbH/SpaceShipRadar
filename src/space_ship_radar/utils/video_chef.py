"""Video Chef Currently not used

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

# Variables ********************************************************************

# Classes **********************************************************************


class VideoChef:
    """manages a test video"""
    path = "path/to/video.mp4"
    video = cv2.VideoCapture(path)

    @staticmethod
    def get_video():
        """returns a test video"""
        return VideoChef.video

    @staticmethod
    def get_video_path():
        """returns the path of the video"""
        return VideoChef.path

# Functions ********************************************************************

# Main *************************************************************************
