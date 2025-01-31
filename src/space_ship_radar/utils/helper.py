"""Helper Functions"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import numpy as np
import keyboard
from numba import jit
import controller  # type: ignore # pylint: disable=import-error
from utils.path_gouverneur import PathGouverneur
from utils.video_chef import VideoChef

# Classes **********************************************************************


class ColorGenerator:
    """Manages random colors"""

    def __init__(self):
        self.previous_colors = []

    def random_color(self):
        """returns a random color which is different from the previous random colors"""

        new_color: np.ndarray = np.random.randint(50, 200, (1, 3))[0]

        # Check for maximum distance from previous colors
        i: int = 0
        while self.previous_colors:
            distances = [np.linalg.norm(new_color - np.array(color))
                         for color in self.previous_colors]
            if min(distances) < 100 or i > 3:
                new_color = np.random.randint(0, 200, (1, 3))[
                    0]  # Regenerate if too close
            else:
                i += 1
                break

        # Store the new color
        self.previous_colors.append(new_color.tolist())

        return new_color.tolist()

    def foos(self):
        """this function exists to make pylint happy"""

# Functions ********************************************************************


def get_image(camera):
    """returns the current image from the webots camera or a video for testing"""

    if isinstance(camera, controller.camera.Camera):
        image = camera.getImage()
        width = camera.getWidth()
        height = camera.getHeight()

        image_array = np.frombuffer(
            image, dtype=np.uint8).reshape((height, width, 4))
        image_bgr = image_array[:, :, :3]

        return image_bgr

    if isinstance(camera, cv2.VideoCapture):
        ok, frame = VideoChef.get_video().read()
        if ok:
            return frame
        return None

    raise TypeError("Unsupported type")


def get_contours(image: np.ndarray, background: np.ndarray) -> np.array:
    """get the contours from an images"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("Background: ", cv2.WINDOW_NORMAL)
    cv2.imshow("Background: ", background)

    dframe = cv2.absdiff(background, gray_image)
    cv2.namedWindow("Dframe: ", cv2.WINDOW_NORMAL)
    cv2.imshow("Dframe: ", dframe)

    # blurred number has to be uneven
    blurred = cv2.GaussianBlur(dframe, (41, 41), 0)
    cv2.namedWindow("GaussianBlur: ", cv2.WINDOW_NORMAL)
    cv2.imshow("GaussianBlur: ", blurred)
    cv2.waitKey(1)

    ret, tframe = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    if ret:
        (contours, _) = cv2.findContours(tframe.copy(),
                                         cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    return np.array([])


color_generator = ColorGenerator()


def random_color() -> tuple[int, int, int]:
    """returns a random color"""
    return color_generator.random_color()


def record_video(camera, step, time_step, width=1920, height=1440):
    """records a video for the webots camera"""
    video_output_file_name = 'video_output' + '.mp4'
    video_out = cv2.VideoWriter(
        video_output_file_name, -1, 40, (width, height))

    while step(time_step) != -1:
        frame = get_image(camera)

        video_out.write(frame)

        if keyboard.is_pressed('q'):
            break

    video_out.release()


@jit
def calculate_speed(points: np.ndarray) -> tuple[int, int]:
    """calculates the speed based on previous points"""
    if len(points) < 2:
        return (0, 0)  # Not enough points to calculate speed

    # Calculate differences in x and y coordinates
    dx = np.empty(len(points) - 1, dtype=np.int32)
    dy = np.empty(len(points) - 1, dtype=np.int32)

    for i in range(1, len(points)):
        dx[i - 1] = points[i][0] - points[i - 1][0]
        dy[i - 1] = points[i][1] - points[i - 1][1]

    # Calculate median of differences using np.median
    median_dx = int(np.median(dx))
    median_dy = int(np.median(dy))

    return (median_dx, median_dy)


# from: https://docs.opencv.org/3.4/d8/dbc/tutorial_histogram_calculation.html
def get_hist(image):
    """returns a histogram for an image"""
    bgr_planes = cv2.split(image)
    hist_size = 16

    # filter bright colors
    # because the background is white
    hist_range = (0, 129)
    accumulate = False

    g_hist = cv2.calcHist(bgr_planes, [1], None, [
        hist_size], hist_range, accumulate=accumulate)

    hist_h = 400

    cv2.normalize(g_hist, g_hist, alpha=0, beta=hist_h,
                  norm_type=cv2.NORM_MINMAX)

    return g_hist


def get_robo_hist():
    """returns a histogram from a picture of the robot"""
    image = cv2.imread(PathGouverneur.get_path() + "just_robo.png")

    return get_hist(image)
