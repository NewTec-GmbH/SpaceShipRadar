"""Tests Transformer
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# Imports **********************************************************************

import cv2
import numpy as np

# pylint: disable=import-error
from transformer import Transformer

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************


def test_transformer_simple():
    """tests if Transformer correctly transforms a simple image (not_transformed_simple.png)
        based on the edge_corners
    """
    # 1. Arrange
    image = cv2.imread("tests/data/not_transformed_simple.png")
    expected_transformed_image = cv2.imread(
        "tests/data/transformed_simple.png")

    assert image is not None
    assert expected_transformed_image is not None

    # edge_corners are the green pixels in not_transformed_simple.png
    edge_corners = [[315, 255], [1487, 255], [1487, 1283], [315, 1283]]

    # 2. Act
    transformed_image = Transformer.perspective_transform(image, edge_corners)

    # 3. Assert
    assert transformed_image.shape == expected_transformed_image.shape
    assert np.array_equal(transformed_image, expected_transformed_image)


def test_transformer_webots():
    """tests if Transformer correctly transforms a webots image 
        (not_transformed_webots.png) based on the edge_corners
    """
    # 1. Arrange
    image = cv2.imread("tests/data/not_transformed_webots.png")
    expected_transformed_image = cv2.imread(
        "tests/data/transformed_webots.png")

    assert image is not None
    assert expected_transformed_image is not None

    # edge_corners are the outside corners in not_transformed_webots.png
    corners = [[413, 173], [1506, 173], [1506, 1267], [413, 1267]]

    # 2. Act
    transformed_image = Transformer.perspective_transform(image, corners)

    # 3. Assert
    assert transformed_image.shape == expected_transformed_image.shape
    assert np.array_equal(transformed_image, expected_transformed_image)

# Main *************************************************************************
