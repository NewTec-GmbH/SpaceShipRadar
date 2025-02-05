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
import keyboard
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

    @staticmethod
    def record_video(camera, step, time_step, width=1920, height=1440):
        """records a video for the webots camera"""
        video_output_file_name = 'video_output' + '.mp4'
        video_out = cv2.VideoWriter(
            video_output_file_name, -1, 40, (width, height))

        while step(time_step) != -1:
            frame = ImageGetter.get_image(camera)

            video_out.write(frame)

            if keyboard.is_pressed('q'):
                break

        video_out.release()

    # Functions ********************************************************************

    # Main *************************************************************************
if __name__ == "__main__":
    pass
