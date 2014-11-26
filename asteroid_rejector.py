#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor

from sys import stdin
from sys import stdout
from sys import stderr

import numpy as np
from io import StringIO   # StringIO behaves like a file object


class AsteroidRejector:

    def __init__(self):
        stderr.write("init is currently empty\n")

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(imageData, detections):
        stderr.write("training_data not yet implemented\n")

    # Method:	testingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int testingData(int[] imageData, String[] detections)
    def testing_data(imageData=[], detections=[]):
        stderr.write("testing_data not yet implemented\n")

    # Method:	getAnswer
    # Parameters:
    # Returns:	int[]
    # Method signature:	int[] getAnswer()
    def get_answer():
        stderr.write("get_answer not yet implemented\n")


if __name__ == "__main__":
    astRejector = AsteroidRejector()

    det_list_dtypes = {"names": ("det_num", "frame_num", "sexnum", "time", "ra", "dec", "x", "y", "magnitude", "fwhm", "elong", "theta", "rmse", "deltamu", "rejected"),
                       "formats": (int, int, int, float, float, float, float, float, float, float, float, float, float, float, float, int)}

    for i in range(1000):
        N = int(stdin.readline())
        imageData = []
        for j in range(N):
            imageData.append(int(stdin.readline()))
        imageData = np.array(imageData)

        M = int(stdin.readline())
        detect_str = stdin.readline()
        detections = np.loadtxt(StringIO(detect_str), dtype=det_list_dtypes)

        result = astRejector.training_data(imageData, detections)
        stdout.write(result)

    for i in range(200):
        N = int(stdin.readline())
        imageData = []
        for j in range(N):
            imageData.append(int(stdin.readline()))
        imageData = np.array(imageData)

        M = int(stdin.readline())
        detect_str = stdin.readline()
        detections = np.loadtxt(StringIO(detect_str), dtype=det_list_dtypes)

        result = astRejector.testing_data(imageData, detections)
        stdout.write(result)

    results = astRejector.get_answer
    stdout.write(len(results))
    for i in range(len(results)):
        stdout.write(results[i])
