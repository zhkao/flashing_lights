import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from flashing_lights import GenerateHeatMap


def test_GetFreqCounts():
    test_ret, test_img = cv2.imreadmulti('NP_test1.tif',
                                         flags=cv2.IMREAD_GRAYSCALE)
<<<<<<< HEAD
import GenerateHeatMap


def test_GetFreqCounts():
    test_ret, test_img = cv2.imreadmulti(
    'https://github.com/cmcalli716/flashing_lights/blob/master/\
flashing_lights/data/NP_collision_videos/NP_collision_array.tif',
                                            flags=cv2.IMREAD_GRAYSCALE)
=======
>>>>>>> master
    test_thresh = 2
    test_fn = GenerateHeatMap.GetFreqCounts(test_img[0], test_thresh)
    # Testing output size
    assert len(test_fn) == len(test_img[0]),\
        "Output is the wrong shape"
    # Testing output type
    assert type(test_fn) == np.ndarray,\
        "Output is the wrong type"
    assert np.mean(test_fn) > 0,\
        "No counts were found in test image"


def test_GetFreqArray():
<<<<<<< HEAD
    url = 'https://drive.google.com/open?id=1mJFNPfbdzfQ6NuFcVwRL8FVMmbw3L43K'
    req_test = requests.get(url)
    assert req_test.status_code == 200,\
        "Download failed"
    with open('test_video', 'wb') as f:
        f.write(req_test.content)
    test_ret, test_img = cv2.imreadmulti('test_video',
    test_video = 'https://github.com/cmcalli716/flashing_lights/blob/master/\
flashing_lights/data/NP_collision_videos/NP_collision_array_2.tif'
    test_ret, test_img = cv2.imreadmulti(test_video,
                                         flags=cv2.IMREAD_GRAYSCALE)
    test_fn = GenerateHeatMap.GetFreqArray('test_video')
=======
    test_ret, test_img = cv2.imreadmulti('NP_test1.tif')
    test_fn = GenerateHeatMap.GetFreqArray('NP_test1.tif')
>>>>>>> master
    # Testing output size
    assert len(test_fn) == len(test_img[0]),\
        "Output is the wrong shape"
    # Testing output type
    assert type(test_fn) == np.ndarray,\
        "Output is the wrong type"
    assert np.mean(test_fn) > 0,\
        "No counts were found in test video"


def test_Heatmap():
<<<<<<< HEAD
    url = 'https://drive.google.com/open?id=1mJFNPfbdzfQ6NuFcVwRL8FVMmbw3L43K'
    req_test = requests.get(url)
    assert req_test.status_code == 200,\
        "Download failed"
    with open('video', 'wb') as f:
        f.write(req_test.content)
    test_video = 'https://github.com/cmcalli716/flashing_lights/blob/master/\
flashing_lights/data/NP_collision_videos/NP_collision_array_2.tif'
=======
>>>>>>> master
    test_img_name = 'test'
    test_img_path = '/mnt/c/Users/'
    # Checking how many plots are made before and after function
    plot_before = plt.gcf().number
    test_fn = GenerateHeatMap.Heatmap('NP_test1.tif',
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
