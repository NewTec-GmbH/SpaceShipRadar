"""Interface for Image-Getting Protocol

Adapter to get a image for different devices

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************


import numpy as np
import cv2
from utils.video_chef import VideoChef
import controller  # type: ignore # pylint: disable=import-error

# Variables ********************************************************************

# Classes **********************************************************************


class ImageGetter():
    """Image Getter"""

    @staticmethod
    def get_image(device) -> np.array:
        """returns the current image from the webots camera or a video for testing"""

        if isinstance(device, controller.camera.Camera):
            return ImageGetter.__get_image_webots_camera(device)

        if isinstance(device, cv2.VideoCapture):
            return ImageGetter.__get_image_video()

        raise TypeError("Unsupported type")

    @staticmethod
    def __get_image_webots_camera(device: controller.camera.Camera) -> np.array:
        image = device.getImage()
        width = device.getWidth()
        height = device.getHeight()

        image_array = np.frombuffer(
            image, dtype=np.uint8).reshape((height, width, 4))
        image_bgr = image_array[:, :, :3]

        return image_bgr

    @staticmethod
    def __get_image_video() -> np.array:
        ok, frame = VideoChef.get_video().read()
        if ok:
            return frame
        return None

    # Functions ********************************************************************

    # Main *************************************************************************
if __name__ == "__main__":
    pass
