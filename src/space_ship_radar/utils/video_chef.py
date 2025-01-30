"""Video Chef Currently not used"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2

# Classes **********************************************************************


class VideoChef:
    """manages a test video"""
    video = cv2.VideoCapture("path/to/video.mp4")

    @staticmethod
    def get_video():
        """returns a test video"""
        return VideoChef.video
