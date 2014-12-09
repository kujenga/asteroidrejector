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
        self.det_dtypes = np.dtype([("uniq_id", int), ("det_num", int), ("frame_num", int),
                                    ("sexnum", int), ("time", float), ("ra", float), ("dec", float),
                                    ("x", float), ("y", float), ("magnitude", float),
                                    ("fwhm", float), ("elong", float), ("theta", float),
                                    ("rmse", float), ("deltamu", float), ("rejected", int)])
        self.detect_images = []
        self.reject_imgaes = []

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(self, imageData, detections):
        detections = self.convert_detections(detections)  # eliminates erroneous first element
        imageData = self.convert_time_series(imageData)
        accepted = 0
        rejected = 0
        # plt.imshow(imageData[0], interpolation='nearest')
        # plt.show()
        # toimage(imageData[0]).show()
        for index, detection in enumerate(detections):

            if detection["rejected"] == 1:
                rejected += 1
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
        stderr.write("testing_data not yet implemented\n")
        return 0

    # Method:	getAnswer
    # Parameters:
    # Returns:	int[]
    # Method signature:	int[] getAnswer()
    def get_answer(self):
        stderr.write("get_answer not yet implemented\n")
        return []

    # converts the strings readin from the detection files into numpy arrays
    def convert_detections(self, detection_strs):
        detections = []
        for index, det_str in enumerate(detection_strs):
            det = np.loadtxt(StringIO(det_str), dtype=self.det_dtypes)
            detections.append(det)
        return np.array(detections)

    # converts the raw image data into array of 1D arrays of the 4 images in a time series
    def convert_time_series(self, raw):
        num_series = len(raw) / (64*64*4)
        print(num_series)
        num_series = int(num_series)
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

# if __name__ == "__main__":
#     astRejector = AsteroidRejector()
#
#     for i in range(1000):
#         N = int(stdin.readline())
#         imageData = []
#         for j in range(N):
#             imageData.append(int(stdin.readline()))
#         imageData = np.array(imageData)
#
#         M = int(stdin.readline())
#         detections = []
#         for j in range(M):
#             detect_str = stdin.readline()
#             det = np.loadtxt(StringIO(detect_str), dtype=det_list_dtypes)
#             detections.append(det)
#         detections = np.array(detections)
#
#         result = astRejector.training_data(imageData, detections)
#         stdout.write(str(result))
#         stdout.flush()
#
#     for i in range(200):
#         N = int(stdin.readline())
#         imageData = []
#         for j in range(N):
#             imageData.append(int(stdin.readline()))
#         imageData = np.array(imageData)
#
#         M = int(stdin.readline())
#         detect_str = stdin.readline()
#         detections = np.loadtxt(StringIO(detect_str), dtype=det_list_dtypes)
#
#         result = astRejector.testing_data(imageData, detections)
#         stdout.write(result)
#         stdout.flush()
#
#     results = astRejector.get_answer
#     stdout.write(len(results))
#     for i in range(len(results)):
#         stdout.write(results[i])
#     stdout.flush()
