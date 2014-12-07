#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor

from sys import stderr

import numpy as np
from io import StringIO   # StringIO behaves like a file object


class AsteroidRejector:

    def __init__(self):
        self.det_list_dtypes = {"names": ("det_num", "frame_num", "sexnum", "time", "ra", "dec", "x", "y", "magnitude", "fwhm", "elong", "theta", "rmse", "deltamu", "rejected"),
                                "formats": (int, int, int, float, float, float, float, float, float, float, float, float, float, float, float, int)}

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(self, imageData, detections_array):
        detections = np.array(detections_array)
        print(type(detections))
        print (detections[0])
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


# if __name__ == "__main__":
#     astRejector = AsteroidRejector()
#
#     det_list_dtypes = {"names": ("det_num", "frame_num", "sexnum", "time", "ra", "dec", "x", "y", "magnitude", "fwhm", "elong", "theta", "rmse", "deltamu", "rejected"),
#                        "formats": (int, int, int, float, float, float, float, float, float, float, float, float, float, float, float, int)}
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
