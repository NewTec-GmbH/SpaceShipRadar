"""Histogram Star

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import numpy as np

from utils.path_governor import PathGovernor

# Variables ********************************************************************

# Classes **********************************************************************


class HistogramStar:
    """HistogramStar"""

    # from: https://docs.opencv.org/3.4/d8/dbc/tutorial_histogram_calculation.html
    @staticmethod
    def get_hist(image: np.array) -> np.array:
        """returns a histogram for an image"""
        bgr_planes = cv2.split(image)
        hist_size = 16

        # filter bright colors
        # because the background is white
        hist_range = (0, 129)
        accumulate = False

        g_hist = cv2.calcHist(bgr_planes, [1], None, [
            hist_size], hist_range, accumulate=accumulate)

        hist_height = 400

        cv2.normalize(g_hist, g_hist, alpha=0, beta=hist_height,
                      norm_type=cv2.NORM_MINMAX)

        return g_hist

    @staticmethod
    def get_robo_hist() -> np.array:
        """returns a histogram from a picture of the robot"""
        image = cv2.imread(PathGovernor.get_path() + "just_robo.png")

        return HistogramStar.get_hist(image)

# Functions ********************************************************************

# Main *************************************************************************
