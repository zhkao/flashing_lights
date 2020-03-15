import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from flashing_lights import GenerateIntensityMap


def test_GetIntensityValues():
    test_ret, test_img = cv2.imreadmulti('NP_test1.tif',
                                         flags=cv2.IMREAD_GRAYSCALE)
    test_thresh = 2
    test_fn = GenerateIntensityMap.GetIntensityValues(test_img[0], test_thresh)
    # Testing output size
    assert len(test_fn) == len(test_img[0]),\
        "Output is the wrong shape"
    # Testing output type
    assert type(test_fn) == np.ndarray,\
        "Output is the wrong type"
    assert np.mean(test_fn) > 0,\
        "No counts were found in test image"


def test_GetIntensityArray():
    test_ret, test_img = cv2.imreadmulti('NP_test1.tif')
    test_fn = GenerateIntensityMap.GetIntensityArray('NP_test1.tif', 1, 100)
    # Testing output size
    assert len(test_fn) == len(test_img[0]),\
        "Output is the wrong shape"
    # Testing output type
    assert type(test_fn) == np.ndarray,\
        "Output is the wrong type"
    assert np.mean(test_fn) > 0,\
        "No counts were found in test video"


def test_IntensityMap():
    test_img_name = 'test'
    test_img_path = '/mnt/c/Users/'
    # Checking how many plots are made before and after function
    plot_before = plt.gcf().number
    test_fn = GenerateIntensityMap.IntensityMap('NP_test1.tif', 1, 100,
                                      test_img_path, test_img_name)
    plot_after = plt.gcf().number
    assert plot_before < plot_after,\
        "You have nothing plotted"
    # Checking to see if array used for plotting is multidimensional
    assert test_fn.ndim > 0,\
        "Wrong dimensional array used for plotting"
    # Checking to see if file is empty or not
    assert os.path.getsize(test_img_path + '/' + test_img_name) > 0,\
        "Saved file is empty."
