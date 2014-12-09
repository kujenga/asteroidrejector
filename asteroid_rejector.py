#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor

from sys import stderr

import numpy as np
from io import StringIO

from matplotlib import pyplot as plt
# from scipy.misc import toimage

from matplotlib import mlab
import sklearn.decomposition as deco


class AsteroidRejector:

    def __init__(self):
        # sets up datatype definitions for the detection lists
        self.trn_dtypes = np.dtype([("uniq_id", int), ("det_num", int), ("frame_num", int),
                                    ("sexnum", int), ("time", float), ("ra", float), ("dec", float),
                                    ("x", float), ("y", float), ("magnitude", float),
                                    ("fwhm", float), ("elong", float), ("theta", float),
                                    ("rmse", float), ("deltamu", float), ("rejected", int)])

        # sets up datatype definitions for the detection lists
        self.tst_dtypes = np.dtype([("uniq_id", int), ("det_num", int), ("frame_num", int),
                                    ("sexnum", int), ("time", float), ("ra", float), ("dec", float),
                                    ("x", float), ("y", float), ("magnitude", float),
                                    ("fwhm", float), ("elong", float), ("theta", float),
                                    ("rmse", float), ("deltamu", float)])
        self.detect_images = []
        self.reject_images = []

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(self, imageData, detections):
        detections = self.convert_detections(detections, False)
        imageData = self.convert_time_series(imageData)
        accepted = 0
        rejected = 0
        # plt.imshow(imageData[0], interpolation='nearest')
        # plt.show()
        # toimage(imageData[0]).show()
        for index, detection in enumerate(detections):

            if detection["rejected"] == 1:
                rejected += 1
                if index % 4 == 0:
                    self.reject_images.append(imageData[int(index/4)])
            else:
                # when the first detection in a set of 4 is found, store it in the running array
                if index % 4 == 0:
                    self.detect_images.append(imageData[int(index/4)])
                # toimage(imageData[0]).show()
                accepted += 1
        print("done training with {} rejected and {} accepted".format(rejected/4, accepted/4))
        return 0

    # Method:	testingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int testingData(int[] imageData, String[] detections)
    def testing_data(self, imageData, detections):
        detections = self.convert_detections(detections, testing=True)
        imageData = self.convert_time_series(imageData)
        stderr.write("testing_data not yet implemented\n")
        return 0

    # Method:	getAnswer
    # Parameters:
    # Returns:	int[]
    # Method signature:	int[] getAnswer()
    def get_answer(self):
        arr = [1]*(len(self.reject_images) + len(self.detect_images))
        print(self.reject_images[0].shape)
        return arr

    #######################################################
    #                                                     #
    #     Conversion Utility Methods for Input Data       #
    #                                                     #
    #######################################################

    # converts the strings readin from the detection files into numpy arrays
    def convert_detections(self, detection_strs, testing=False):
        detections = []
        # removes class from data types for testing
        dt = self.tst_dtypes if testing else self.trn_dtypes
        for index, det_str in enumerate(detection_strs):
            det = np.loadtxt(StringIO(det_str), dtype=dt)
            detections.append(det)
        return np.array(detections)

    # converts the raw image data into array of 1D arrays of the 4 images in a time series
    def convert_time_series(self, raw):
        num_series = int(len(raw) / (64*64*4))
        ts_array = np.ndarray(shape=(num_series, 64*64*4), dtype=np.uint16)
        for raw_index, val in enumerate(raw):
            series_num = raw_index / (64*64*4)
            series_index = raw_index % (64*64*4)
            ts_array[series_num][series_index] = raw[raw_index]
        return ts_array

    # converts the raw image data into an array of 2D arrays in the form of the images
    def convert_image(self, image_data):
        num_images = int(len(image_data)/4096)
        image_array = np.ndarray(shape=(num_images, 64, 64), dtype=np.uint16)
        for index, val in enumerate(image_data):
            image_number = int(index / 4096)
            if image_number >= image_array.shape[0]:
                break
            pixel_number = index % 4096
            pixel_x = int(pixel_number / 64)
            pixel_y = pixel_number % 64
            image_array[image_number][pixel_x][pixel_y] = image_data[index]
        return image_array
