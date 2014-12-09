#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor

from sys import stderr

import numpy as np
import pandas as pd
from io import StringIO

from matplotlib import pyplot as plt
# from scipy.misc import toimage

from sklearn.lda import LDA
# from matplotlib import mlab
# import sklearn.decomposition as deco


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

        self.test_images = []

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
        print("finished training round with {} rejected and {} accepted".format(rejected/4, accepted/4))
        return 0

    # Method:	testingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int testingData(int[] imageData, String[] detections)
    def testing_data(self, imageData, detections):
        detections = self.convert_detections(detections, testing=True)
        imageData = self.convert_time_series(imageData)
        self.test_images.append(imageData)
        print("loaded testing data with {} records".format(len(imageData)))
        return 0

    # Method:	getAnswer
    # Parameters:
    # Returns:	int[]
    # Method signature:	int[] getAnswer()
    def get_answer(self):
        rej_num = len(self.reject_images)
        det_num = len(self.detect_images)

        # uses pandas dataframe to create an np.ndarray of the class labels
        images = pd.DataFrame(self.reject_images + self.detect_images).values
        labels = pd.DataFrame([0]*rej_num + [1]*det_num).values.reshape(1, images.shape[0])[0]

        # LDA
        sklearn_lda = LDA(n_components=2)
        X_lda_sklearn = sklearn_lda.fit_transform(images, labels)

        result = self.LDA(images, labels)
        print("LDA result: {}".format(result))
        return list(labels)

    # implementation followed from: http://sebastianraschka.com/Articles/2014_python_lda.html#step-1-computing-the-d-dimensional-mean-vectors
    def LDA(self, X, y):
        n_series = X.shape[0]
        n_dim = X.shape[1]
        print("n_series: {} n_dim: {}".format(n_series, n_dim))
        # y = y.reshape(1, n_series)[0]

        label_dict = {0: "rejected", 1: "detected"}

        # Step 1:
        # calculate mean vectors
        mean_vectors = []
        print("computing mean vectors...")
        for class_label in range(0, 2):
            mean_vectors.append(np.mean(X[y == class_label], axis=0))
            print('Mean Vector class {}: {}\n'.format(class_label, mean_vectors[class_label]))

        # Step 2:
        # computing the scatter matricies

        # 2.1: within-class scatter matrix
        S_W = np.zeros((n_dim, n_dim))
        for cl, mv in zip(range(0, 2), mean_vectors):
            class_sc_mat = np.zeros((n_dim, n_dim))    # scatter matrix for every class
            print(X[y == cl].shape)
            print(mv)
            for index, row in enumerate(X[y == cl]):
                print("within-class: class {} for row {}".format(cl, index))
                row, mv = row.reshape(n_dim, 1), mv.reshape(n_dim, 1)  # make column vectors
                class_sc_mat += (row-mv).dot((row-mv).T)
            S_W += class_sc_mat                             # sum class scatter matrices
        print('within-class Scatter Matrix shape: ', S_W.shape)

        # 2.2: between-class scatter matrix
        overall_mean = np.mean(mean_vectors, axis=0)
        S_B = np.zeros((n_dim, n_dim))
        for i, mean_vec in enumerate(mean_vectors):
            print("between-class: class {} for row {}".format(cl, index))
            n = X[y == i, :].shape[0]
            mean_vec = mean_vec.reshape(n_dim, 1)  # make column vector
            S_B += n * (mean_vec - overall_mean).dot((mean_vec - overall_mean).T)
        print('between-class Scatter Matrix shape: ', S_B.shape)

        # Step 3:
        # Solving the generalized eigenvalue problem for the matrix SW-1SB
        eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(S_W).dot(S_B))
        for i in range(len(eig_vals)):
            eigvec_sc = eig_vecs[:, i].reshape(n_dim, 1)
            print('\nEigenvector {}: \n{}'.format(i+1, eigvec_sc.real))
            print('Eigenvalue {:}: {:.2e}'.format(i+1, eig_vals[i].real))

        # Checking the eigenvector-eigenvalue calculation
        for i in range(len(eig_vals)):
            eigv = eig_vecs[:, i].reshape(4, 1)
            np.testing.assert_array_almost_equal(np.linalg.inv(S_W).dot(S_B).dot(eigv),
                                                 eig_vals[i] * eigv,
                                                 decimal=6, err_msg='', verbose=True)
        print('ok')

        # Step 4:
        # Selecting linear discriminants for the new feature subspace

        # 4.1. Sorting the eigenvectors by decreasing eigenvalues
        # Make a list of (eigenvalue, eigenvector) tuples
        eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]

        # Sort the (eigenvalue, eigenvector) tuples from high to low
        eig_pairs = sorted(eig_pairs, key=lambda k: k[0], reverse=True)

        # Visually confirm that the list is correctly sorted by decreasing eigenvalues

        print('Eigenvalues in decreasing order:\n')
        for i in eig_pairs:
            print(i[0])

        print('Variance explained:\n')
        eigv_sum = sum(eig_vals)
        for i, j in enumerate(eig_pairs):
            print('eigenvalue {0:}: {1:.2%}'.format(i+1, (j[0]/eigv_sum).real))

        # 4.2. Choosing k eigenvectors with the largest eigenvalues
        W = np.hstack((eig_pairs[0][1].reshape(n_dim, 1), eig_pairs[1][1].reshape(n_dim, 1)))
        print('Matrix W:\n', W.real.T)

        # Step 5:
        # Transforming the samples onto the new subspace
        X_lda = W.T.dot(X.T).T
        print(X_lda.shape)
        # assert X_lda.shape == (150, 2), "The matrix is not 2x150 dimensional."

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
