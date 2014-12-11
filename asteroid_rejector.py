#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor

# from sys import stderr

import numpy as np
import pandas as pd
from io import StringIO
import time

# from matplotlib import pyplot as plt
# from scipy.misc import toimage

# from sklearn.lda import LDA
# from sklearn.qda import QDA
from sklearn.linear_model import Perceptron
# from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
# from matplotlib import mlab
# import sklearn.decomposition as deco


class AsteroidRejector:

    def __init__(self):
        # sets up datatype definitions for the detection lists
        self.det_dtypes = np.dtype([("uniq_id", int), ("det_num", int), ("frame_num", int),
                                    ("sexnum", int), ("time", float), ("ra", float), ("dec", float),
                                    ("x", float), ("y", float), ("magnitude", float),
                                    ("fwhm", float), ("elong", float), ("theta", float),
                                    ("rmse", float), ("deltamu", float), ("rejected", int)])

        self.train_images = []
        self.train_rej_class = []

        self.test_images = []
        self.test_rej_class = []
        self.test_ids = []

        self.debug = False

        self.out_file = open('log/{}.log'.format(time.strftime("astrej_%Y%m%d%H%M%S")), 'w')

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(self, imageData, detections):
        detections = self.convert_detections(detections)
        imageData = self.convert_time_series(imageData)
        assert len(detections) == 4*len(imageData), "there should be 4 detections for each vector"

        rejected = 0
        detected = 0
        self.train_images.extend(imageData)
        for index in range(0, len(imageData)):
            # print("looping", len(detections), len(imageData), index)
            if detections[index*4]["rejected"] == 1:
                rejected += 1
                self.train_rej_class.append(1)
            else:
                detected += 1
                self.train_rej_class.append(0)

                # plt.imshow(self.ts_to_visualization(imageData[index]), interpolation='nearest')
                # plt.show()

                # plt.imshow(self.ts_to_visualization(self.normalize_time_series(imageData[index])), interpolation='nearest')
                # plt.show()
                # plt.savefig('{}.png'.format(detections[index]["uniq_id"]), bbox_inches='tight')

        assert len(self.train_images) == len(self.train_rej_class), "classes {} and images {} should have equal length".format(len(self.train_rej_class), len(self.train_images))

        self.printMsg("finished training round with {} rejected and {} accepted\n".format(rejected, detected))
        return 0

    # Method:	testingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int testingData(int[] imageData, String[] detections)
    def testing_data(self, imageData, detections):
        detections = self.convert_detections(detections)
        imageData = self.convert_time_series(imageData)
        self.test_images.extend(imageData)

        for index in range(0, len(detections), 4):
            self.test_ids.append(int(detections[index]["uniq_id"]))
            if detections[index]["rejected"] == 1:
                self.test_rej_class.append(1)
            else:
                self.test_rej_class.append(0)

        assert len(self.test_images) == len(self.test_rej_class), "classes and images should have equal length"

        self.printMsg("loaded testing data with {} records\n".format(len(imageData)))
        return 0

    # Method:	getAnswer
    # Parameters:
    # Returns:	int[]
    # Method signature:	int[] getAnswer()
    def get_answer(self):
        # uses pandas dataframe to create an np.ndarray of the class labels
        train_images = pd.DataFrame(self.train_images).values
        train_labels = np.array(self.train_rej_class)

        t = time.monotonic()
        self.normalize_time_series_array(train_images)
        print("finished image data normalization in {}".format(time.monotonic() - t))

        # LDA - Linear Discriminant Analyzer
        t = time.monotonic()
        classifier = Perceptron()
        # classifier.fit(train_images, train_labels)
        print("created base classifier in {}".format(time.monotonic() - t))

        t = time.monotonic()
        ensemble = AdaBoostClassifier(classifier, 
            n_estimators=200, 
            algorithm='SAMME')
        print("created ensemble in {}".format(time.monotonic() - t))

        t = time.monotonic()
        ensemble.fit(train_images, train_labels)
        print("fitted {} training records to classifier in {}".format(train_images.shape[0], time.monotonic() - t))

        # create properly formatted np.array objects for the different pieces of the dataset
        tst_images = pd.DataFrame(self.test_images).values
        self.normalize_time_series_array(tst_images)
        tst_labels = np.array(self.test_rej_class)
        tst_ids = np.array(self.test_ids)

        score = ensemble.score(tst_images, tst_labels)
        print("score on {} records: {}".format(tst_images.shape[0], score))

        results = ensemble.predict(tst_images)

        result_ids = tst_ids[results == 0]

        return result_ids

    #######################################################
    #                                                     #
    #     Conversion Utility Methods for Input Data       #
    #                                                     #
    #######################################################

    # converts the strings readin from the detection files into numpy arrays
    def convert_detections(self, detection_strs):
        detections = []
        for index, det_str in enumerate(detection_strs):
            det = np.loadtxt(StringIO(det_str), dtype=self.det_dtypes)
            detections.append(det)
        return pd.DataFrame(detections).values

    # converts the raw image data into array of 1D arrays of the 4 images in a time series
    def convert_time_series(self, raw):
        num_series = int(len(raw) / (64*64*4))
        ts_array = np.ndarray(shape=(num_series, 64*64*4), dtype=np.uint16)
        for raw_index, val in enumerate(raw):
            series_num = raw_index / (64*64*4)
            series_index = raw_index % (64*64*4)
            ts_array[series_num][series_index] = raw[raw_index]
        return ts_array

    def normalize_time_series_array(self, time_series):
        # iterate over each time series in the array
        for index, ts in enumerate(time_series):
            self.normalize_time_series(ts)

    def normalize_time_series(self, time_series):
        assert len(time_series) == 64*64*4, "Each time series must consist of 4 64x64 images"

        offset = 64*64  # offset between images in the time series
        # compute average pixel values across the time series and subtract them from each image
        # this should get rid of some data that is not in motion and that we don't care about
        for i in range(0, 64*64-1):
            px_avg = 0.0
            # compute average pixel value
            for j in range(0,4):
                px_avg += time_series[i + j*offset]
            px_avg /= 4.0
            # subtract   average from each of the 4 images
            for k in range(0,4):
                time_series[i + k*offset] -= px_avg
        return time_series

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

    def ts_to_visualization(self, ts):
        img_seq = np.zeros(shape=(64, (4*64)+(3*10)), dtype=np.uint16)  # 3x10 pixel spacers between images
        offset = 0
        for start in range(0, 64*64*4, 64*64):
            for x in range(64):
                for y in range(64):
                     img_seq[y][x+offset] = ts[x*64 + y + start]
            offset += 64 + 10
        return img_seq

    #############################
    # Printing utility method with debug support
    #############################

    def printMsg(self, *params):
        if self.debug:
            print(params)
        else:
            print(".", end="", flush=True)
            # self.out_file.write(*params)
