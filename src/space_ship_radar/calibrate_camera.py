"""Camera Calibration

Author: Marc Trosch (marc.trosch@newtec.de)
"""

# *******************************************************************************
# Copyright (c) NewTec GmbH 2025   -   www.newtec.de
# *******************************************************************************

# original from: https://github.com/niconielsen32/CameraCalibration/blob/main/calibration.py

# Imports **********************************************************************

from typing import List, Tuple
import glob
import pickle
import numpy as np
import cv2

from utils.path_governor import PathGovernor

# Variables ********************************************************************

# Classes **********************************************************************

# Functions ********************************************************************

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################


def find_chessboard(path: str) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """finds the chessboard pattern in the images provided by the path and calculates the objpoints and imgpoints

    Args:
        path (str): path to calculation images

    Returns:
        objpoints (List[np.ndarray]): 3d point in real world space
        imgpoints (List[np.ndarray]): 2d points in image plane
    """
    chessboard_size = (9, 6)

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    # pylint: disable=no-member
    objp[:, :2] = np.mgrid[0:chessboard_size[0],
                           0: chessboard_size[1]].T.reshape(-1, 2)

    size_of_chessboard_squares_mm = 17
    objp = objp * size_of_chessboard_squares_mm

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(path + '/cali_img/*.png')

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    for image in images:

        img = cv2.imread(image)
        print(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)

            cv2.imshow('img', img)
            cv2.waitKey(1000)

    cv2.destroyAllWindows()
    return objpoints, imgpoints


############## CALIBRATION #######################################################

def calibration(path: str, objpoints: List[np.ndarray],
                imgpoints: List[np.ndarray], frame_size: tuple[int, int]) -> None:
    """saves a calibration2.pkl file at the specified path and prints the reprojection error

    Args:
        path (str): path to the save location
        objpoints (List[np.ndarray]): 3d point in real world space
        imgpoints (List[np.ndarray]): 2d points in image plane
        frame_size (tuple[int, int]): size of the calibration images
    """
    ret, camera_matrix, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, frame_size, None, None)

    # Save the camera calibration result for later use
    if ret:
        with open(path + "/calibration2.pkl", "wb") as file:
            pickle.dump((camera_matrix, dist), file)

    # Reprojection Error
    mean_error = 0

    for i, objpoint in enumerate(objpoints):
        imgpoints2, _ = cv2.projectPoints(
            objpoint, rvecs[i], tvecs[i], camera_matrix, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    print(f"total error: {mean_error/len(objpoints)}")


# Main *************************************************************************
if __name__ == "__main__":
    frame__size = (1920, 1440)

    obj_points, img_points = find_chessboard(PathGovernor.get_path())
    calibration(PathGovernor.get_path(), obj_points, img_points, frame__size)
