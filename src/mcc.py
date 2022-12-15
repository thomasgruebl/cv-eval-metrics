import math
from ctypes import cdll, c_longdouble, c_char_p, create_string_buffer

import cv2 as cv
import numpy as np
from numpy.typing import NDArray


def mcc_cpp_fast(test_image_path: str, ground_truth_path: str) -> float:
    """
    C++ library implementation
    :param test_image_path: The path to the test image
    :type test_image_path: str
    :param ground_truth_path: The path to the ground truth image
    :type: ground_truth_path: str
    :return: Matthews correlation coefficient [-1; 1]
    :rtype: float
    """
    lib = cdll.LoadLibrary('./libmcc.so')

    lib.mcc.argtypes = [c_char_p, c_char_p]
    lib.mcc.restype = c_longdouble

    test_image_path = create_string_buffer(test_image_path.encode("UTF-8"))
    ground_truth_path = create_string_buffer(ground_truth_path.encode("UTF-8"))

    mcc = lib.mcc(test_image_path, ground_truth_path)

    return mcc


def mcc_numpy_fast(test_image: NDArray, ground_truth: NDArray) -> float:
    """
    Numpy implementation
    :param test_image: A thresholded greyscale image -> all pixel values must equal 0 or 255
    :type test_image: NDArray
    :param ground_truth: A thresholded greyscale image -> all pixel values must equal 0 or 255
    :type: ground_truth: NDArray
    :return: Matthews correlation coefficient [-1; 1]
    :rtype: float
    """
    assert (test_image.shape == ground_truth.shape)

    test_image[test_image == 0] = 1
    ground_truth[ground_truth == 0] = 2
    test_image = test_image.astype(np.uint16)
    ground_truth = ground_truth.astype(np.uint16)
    values = test_image * ground_truth

    TP = np.count_nonzero(values == 65025)
    FP = np.count_nonzero(values == 255)
    TN = np.count_nonzero(values == 2)
    FN = np.count_nonzero(values == 510)

    # identical images
    if FP == 0 and FN == 0:
        return 1.0
    # no pixels matching
    elif TP == 0 and TN == 0:
        return -1.0

    assert ((TP + FP + TN + FN) == (test_image.shape[0] * test_image.shape[1]))

    return ((TP * TN) - (FP * FN)) / (math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)))


def mcc_list_comprehension(test_image: NDArray, ground_truth: NDArray) -> float:
    TP, FP, TN, FN = 0, 0, 0, 0
    pixels = ['TP' if pixelGT == 255 and pixelTest == pixelGT else
              'TN' if pixelTest == pixelGT else
              'FP' if pixelGT == 255 else 'FN'
              for rowTest, rowGT in zip(test_image, ground_truth) for pixelTest, pixelGT in zip(rowTest, rowGT)]

    TP = pixels.count('TP')
    FP = pixels.count('FP')
    TN = pixels.count('TN')
    FN = pixels.count('FN')

    # identical images
    if FP == 0 and FN == 0:
        return 1.0
    # no pixels matching
    elif TP == 0 and TN == 0:
        return -1.0

    return ((TP * TN) - (FP * FN)) / (math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)))


def mcc_readable_slow(test_image: NDArray, ground_truth: NDArray) -> float:
    TP, FP, TN, FN = 0, 0, 0, 0
    for rowTest, rowGT in zip(test_image, ground_truth):
        for pixelTest, pixelGT in zip(rowTest, rowGT):
            # foreground pixel
            if pixelGT == 255:
                # True positive if foreground pixel has been correctly segmented
                if pixelTest == pixelGT:
                    TP += 1
                # else false positive
                else:
                    FP += 1
            # background pixel
            if pixelGT == 0:
                # True negative if background pixel has been correctly segmented
                if pixelTest == pixelGT:
                    TN += 1
                # else false negative
                else:
                    FN += 1

    # identical images
    if FP == 0 and FN == 0:
        return 1.0
    # no pixels matching
    elif TP == 0 and TN == 0:
        return -1.0

    return ((TP * TN) - (FP * FN)) / (math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)))


def main():

    """
    C++ library solution
    """
    mcc = mcc_cpp_fast('test_image_path', 'ground_truth_image_path')

    """
    Numpy solution
    """
    test_image = cv.imread('test_image_path', cv.IMREAD_GRAYSCALE)
    ground_truth = cv.imread('ground_truth_image_path', cv.IMREAD_GRAYSCALE)

    # threshold any leftover greyscale values to 0 or 255
    ret, test_image = cv.threshold(test_image, 127, 255, cv.THRESH_BINARY)
    ret, ground_truth = cv.threshold(ground_truth, 127, 255, cv.THRESH_BINARY)

    mcc = mcc_numpy_fast(test_image, ground_truth)

    print('MCC: ', mcc)


if __name__ == '__main__':
    main()
