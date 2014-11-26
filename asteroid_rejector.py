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
        print("init is currently empty")

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(imageData, detections):
        print("training_data not yet implemented")

    # Method:	testingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int testingData(int[] imageData, String[] detections)
    def testing_data(imageData=[], detections=[]):
        print("testing_data not yet implemented")

    # Method:	getAnswer
    # Parameters:
    # Returns:	int[]
    # Method signature:	int[] getAnswer()
    def get_answer():
        print("get_answer not yet implemented")


if __name__ == "__main__":
    astRejector = AsteroidRejector()

    det_list_dtypes = {"names": ("det_num", "frame_num", "sexnum", "time", "ra", "dec", "x", "y", "magnitude", "fwhm", "elong", "theta", "rmse", "deltamu", "rejected"),
                       "formats": (int, int, int, float, float, float, float, float, float, float, float, float, float, float, float, int)}

    for i in range(1000):
        N = int(stdin.readline())
        stderr.write("N:"+str(N)+'\n')
        imageData = []
        for j in range(N):
            imageData.append(int(stdin.readline()))
        imageData = np.array(imageData)
        stderr.write(str(imageData.shape))

        M = int(stdin.readline())
        stderr.write("M:"+str(M)+'\n')
        detect_str = stdin.readline()
        stderr.write(detect_str)
        detections = np.loadtxt(StringIO(detect_str), dtype=det_list_dtypes)
        stderr.write("dets:"+str(detections.shape))

        result = astRejector.training_data(imageData, detections)
        stdout.write(result)

    for i in range(200):
        N = int(stdin.readline())
        imageData = []
        for j in range(N):
            imageData[j] = stdin.readline().split()
        M = int(stdin.readline())
        detections = []
        for j in range(M):
            detections[j] = stdin.readline()
        result = astRejector.testing_data(imageData, detections)
        stdout.write(result)

    results = astRejector.get_answer
    stdout.write(len(results))
    for i in range(len(results)):
        stdout.write(results[i])
