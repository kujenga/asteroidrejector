#!//anaconda/bin/python
# Asteroid Data Hunter project

# Aaron Taylor


class AsteroidRejector:

    def __init__(self):
        print("init is currently empty")

    # Class:	AsteroidRejector
    # Method:	trainingData
    # Parameters:	int[], String[]
    # Returns:	int
    # Method signature:	int trainingData(int[] imageData, String[] detections)
    def training_data(imageData=[], detections=[]):
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

    for i in range(1000):
        N = readLine()
        imageData = []
        for j in range(N):
            imageData[j] = readInt()
        M = readLine()
        detections = []
        for j in range(M):
            detections[j] = readLine()
        result = astRejector.training_data(imageData, detections)
        print(result)

    for i in range(200):
        N = parseInt(readLine())
        imageData = []
        for j in range(N):
            imageData[j] = readInt()
        M = parseInt(readLine())
        detections = []
        for j in range(M):
            detections[j] = readLine()
        result = astRejector.testing_data(imageData, detections)
        print(result)

    results = astRejector.get_answer
    print(len(results))
    for i in range(len(results)):
        print(results[i])
