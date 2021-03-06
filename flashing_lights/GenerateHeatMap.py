"""Group of functions which produce heatmap of accumulated frequency counts.
To run these functions the user will need a videofile (.tif format).

WARNING: Extremely large video files (>1500 frames) or videos with
high pixel resolution (512x512 array or greater) may take a couple of
minutes to run depending on your computer's processing power."""
import numpy as np
import matplotlib.pyplot as plt
import cv2


def GetFreqCounts(frame, threshold):
    """Searches through an image to find greyscale pixels above a certain
    brightness threshold. If counts of sufficient brightness are present
    within the image, a frequency counter of 1 is added to an empty array.

    Inputs:

    - frame: ndarray of pixels (image file or video frame)
    - threshold: minimum brightness for an event detection

    Output: an ndarray of boolean values describing which
    pixels were above the brightness threshold in the frame

    """
    # Generating empty matrix for coordinate assignment
    frequency = np.zeros((len(frame), len(frame)))
    # Generating index lists to keep track of ROI coordinates
    index_count_row = []
    index_count_col = []
    # Looks through matrix for points above a brightness threshold
    if len(np.where(frame == threshold)) > 0:
        # Finding coordinates of brightness events
        row, col = np.where(frame >= threshold)
        for i in range(len(row)):
            for j in range(len(col)):
                # Adds intensity value in the position of the
                # given brightness event
                frequency[row[i], col[j]] = frame[row[i], col[j]]
                # Adds a value of 1 to the frequency output in the position of
                # the given brightness event
                frequency[row[i], col[i]] = 1
                index_count_row.append(row[i])
                index_count_col.append(col[j])
    else:
        pass
    return frequency


def GetFreqArray(videofile, threshold, scale_percent, outliers=True):
    """Finds pixel coordinates within a videofile (.tif, .mp4) for pixels
    that are above a calculated brightness threshold, then accumulates the
    brightness event count for each coordinate,
    outputting it as a 2-D array in the same size as the video frames

    Input:
    -videofile: file containing an image stack of fluorescent events
    -threshold: minimum brightness value for event detection
    -scale_percent: size of image you would like to resize to (% value)
    -outliers: If True, tests for outliers in the data

    Output: 2-d Array of frequency values for each pixel above
    a calculated brightness threshold in the video"""
    # Reading video file and convert to grayscale
    ret, img = cv2.imreadmulti(videofile, flags=cv2.IMREAD_GRAYSCALE)
    # Setting Resizing Dimensions
    width = int(img[0].shape[1] * scale_percent / 100)
    height = int(img[0].shape[0] * scale_percent / 100)
    dim = (width, height)
    img_resized = cv2.resize(img[0], dim, interpolation=cv2.INTER_AREA)
    # Creating empty array to add intensity values to
    freq_array = np.zeros(np.shape(img_resized))
    # Looking through each frame to get the frequency counts
    for frame in range(len(img)):
        # Resize Frame
        frame_resized = cv2.resize(img[frame],
                                   dim, interpolation=cv2.INTER_AREA)
        freq = GetFreqCounts(frame_resized, threshold)
        if len(np.where(freq == 1)) > 0:
            # Get coordinates of the single pixel counts
            row, col = np.where(freq == 1)
            for i in range(len(row)):
                for j in range(len(col)):
                    # Add single count to freq_array in location of event
                    freq_array[row[i], col[j]] += 1
        else:
            pass
    if outliers is True:
        # Videos may contain points with extremely high frequency
        # relative to other pixels. This can affect the quality
        # of the heatmap produced. So, this part of the code determines a
        # max frequency from the freq distribution, then sets all points above
        # the max frequency to the max frequency.
        # This is solely for heatmap quality, it can be commented out.
        #
        # Creating empty frequency list for determining outliers
        freq_list = []
        # finding points where the frequency is greater than 0
        freq_row, freq_col = np.where(freq_array >= 1)
        for i in range(len(freq_row)):
            # Appending frequency values above 0 to freq_list
            freq_list.append(freq_array[freq_row[i], freq_col[i]])
        # Sorting the list to calculate its distribution
        sort_list = sorted(freq_list)
        # Calculating the distribution
        q1, q3 = np.percentile(sort_list, 25), np.percentile(sort_list, 75)
        iqr = q3 - q1
        upper_lim = q3 + 1.5*iqr
        # Finding Outliers
        if len(np.where(freq_array >= upper_lim)) > 0:
            outlier_row, outlier_col = np.where(freq_array >= upper_lim)
            for i in range(len(outlier_row)):
                for j in range(len(outlier_col)):
                    # Replacing outlier frequency with upper limit
                    freq_array[outlier_row[i], outlier_col[j]] = upper_lim
        else:
            pass
    else:
        pass
    return freq_array


def Heatmap(videofile, threshold, scale_percent, img_path, img_name,
            outliers=True):
    """Takes frequency accumulation array from
    GenerateHeatMap.GetFreqArray() and plots it as
    a colored meshgrid.

    Yellow pixels are at max frequency, blue pixels are
    minimum frequency (cmap = 'plasma')"""
    # Reading video file
    ret, img = cv2.imreadmulti(videofile, flags=cv2.IMREAD_GRAYSCALE)
    # obtaining frequency array
    if outliers is True:
        z = GetFreqArray(videofile, threshold, scale_percent)
    else:
        z = GetFreqArray(videofile, threshold, scale_percent, outliers=False)
    # Generating x and y axes in shape of image frame
    width = int(img[0].shape[1] * scale_percent / 100)
    height = int(img[0].shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    frame_resized = cv2.resize(img[0], dim, interpolation=cv2.INTER_AREA)
    pixel_X = np.arange(0, frame_resized.shape[1])
    pixel_Y = np.arange(0, frame_resized.shape[0])
    # Mapping frequency array onto the x and y axes
    fig = plt.pcolormesh(pixel_X, pixel_Y, z, cmap='plasma')
    plt.xlabel('Pixel Count')
    plt.ylabel('Pixel Count')
    plt.title('Frequency Heat Map')
    # picture is saved in file location designated by user
    plt.savefig(img_path + '/' + img_name + '.png', bbox_inches='tight')
    return fig
