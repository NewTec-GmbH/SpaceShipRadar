"""Interface for Image-Getting Protocol

Adapter to get a image for different devices

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import pickle
import keyboard
import numpy as np
import cv2

import controller  # type: ignore # pylint: disable=import-error

from utils.path_governor import PathGovernor

# Variables ********************************************************************

# Classes **********************************************************************


class ImageGetter():
    """Image Getter"""

    with open(f"{PathGovernor.get_path()}/calibration.pkl", "rb") as file:
        camera_matrix, dist = pickle.load(file)

    @staticmethod
    def get_image(device) -> np.array:
        """returns the current image from the webots camera or a video for testing"""

        if isinstance(device, controller.camera.Camera):
            return ImageGetter.__get_image_webots_camera(device)

        if isinstance(device, cv2.VideoCapture):
            return ImageGetter.__get_image_video(device)

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
    def __get_image_video(device) -> np.array:

        ok, frame = device.read()
        if ok:
            h,  w = frame.shape[:2]
            new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
                ImageGetter.camera_matrix, ImageGetter.dist, (w, h), 1, (w, h))

            # Undistort with Remapping
            map_x, map_y = cv2.initUndistortRectifyMap(
                ImageGetter.camera_matrix, ImageGetter.dist, None, new_camera_matrix, (w, h), 5)
            dst = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]

            return dst
        return None

    @staticmethod
    def record_video(camera, step, time_step, width=1920, height=1440):
        """records a video for the webots camera"""
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_output_file_name = 'video_output' + '.mp4'
        video_out = cv2.VideoWriter(
            video_output_file_name, fourcc, 40, (width, height))

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
