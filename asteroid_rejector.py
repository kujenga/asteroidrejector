#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor

from sys import stderr

import numpy as np
from io import StringIO


class AsteroidRejector:

    def __init__(self):
        # sets up datatype definitions for the detection lists
        self.det_dtypes = np.dtype([("uniq_id", int), ("det_num", int), ("frame_num", int),
                                    ("sexnum", int), ("time", float), ("ra", float), ("dec", float),
                                    ("x", float), ("y", float), ("magnitude", float),
                                    ("fwhm", float), ("elong", float), ("theta", float),
                                    ("rmse", float), ("deltamu", float), ("rejected", int)])

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(self, imageData, detections):
        detections = self.convert_detections(detections)  # eliminates erroneous first element
        imageData = self.convert_image(imageData)
        print(detections.dtype)
        print(imageData.shape)
        # for d in detections[0]:
        #     stdout.write(str(type(d)) + " ")
        print("done")
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

    def convert_detections(self, detection_strs):
        detections = []
        for det_str in detection_strs:
            det = np.loadtxt(StringIO(det_str), dtype=self.det_dtypes)
            detections.append(det)
        return np.array(detections)

    def convert_image(self, image_data):
        return np.array(image_data)

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
