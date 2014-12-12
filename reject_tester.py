#!//anaconda/bin/python
# tests the AsteroidRejector

import argparse
# from PIL import Image
# import math

import os

from asteroid_rejector import AsteroidRejector

# # boolean
# debug = true
# # boolean
# visualize = false
# # String
# execCommand = null
# # String
# trainFile = null
# # String
# testFile = null
# # String
# folder = ""


class RejectTester:

    def __init__(self, trainFile, testFile, execCommand, debug=True, visualize=False):
        print("initializing")
        self.trainFile = trainFile
        self.testFile = testFile
        self.execCommand = execCommand
        self.debug = debug
        self.visualize = visualize

    def printMessage(self, s):
        if (self.debug):
            print(s)

    # Score a testcase, given detections and rejections and user answers
    #                     int[]    Set<Integer>    Set<Integer>
    def scoreAnswer(self, userAns, modelAnsDetect, modelAnsReject):
        print("\nScoring")

        score = 0.0
        total = 0.0
        correct = 0.0
        userAnsUsed = set()
        for i, val_id in enumerate(userAns):
            self.printMessage("scoring {}: {}".format(i, val_id))
            total += 1.0
            if (val_id not in modelAnsDetect) and val_id not in modelAnsReject:
                self.printMessage("Unique ID {} not valid.".format(val_id))
                return 0.0

            if val_id in userAnsUsed:
                self.printMessage("Unique ID {} already used.".format(val_id))
                return 0.0

            userAnsUsed.add(val_id)

            if val_id in modelAnsDetect:
                correct += 1.0
                self.printMessage("1")
                score += (1000000.0 / len(modelAnsDetect)) * (correct / total)

            self.printMessage("0")

        return score

    #                      int[]  int     String
    def visualizeImg(self, raw,   offset, fileName):
        pass
        # W = (64+10)*4-10
        # bi = Image.new('RGB', (W, 64))
        # # g = (Graphics2D)bi.getGraphics()
        # for y in range(64):
        #     for x in range(W):
        #         bi.putpixel((x, y), 0xffffff)
        # for i in range(4):
        #     off = offset + i*64*64
        #     imin = 1 << 20
        #     imax = -imin
        #     # Find min and max
        #     for j in range(4096):
        #         r = raw[j+off]
        #         if (r > 65500):
        #             continue
        #         imin = min(imin, r)
        #         imax = max(imax, r)
        
        #     dmax = float((imax) / 256.0)
        #     dmin = float((imin) / 256.0)
        #     if (dmax*0.5-dmin > 10):
        #         dmax *= 0.5
        
        #     if (dmax-dmin < 0.0001):
        #         dmax += 0.1
        
        #     linearF = 255.0 / (dmax - dmin)
        #     log10 = math.log(10.0)
        #     logF = 255.0 / (math.log(255.0) / log10)
        #     for y in range(64):
        #         for x in range(64):
        #             ival = raw[off]
        #             off += 1
        #             dval = float((ival) / 256.0)
        #             if (dval < dmin):
        #                 ival = 0
        #             elif (dval > dmax):
        #                 ival = 255
        #             else:
        #                 dval = max(0.0, min(dval-dmin, dmax - dmin))
        #                 d = 0.0
        #                 if dval * linearF != 0.0:
        #                     d = ((math.log(dval * linearF)) / log10) * logF
        #                 ival = int(d)
        #             if (ival < 0):
        #                 ival = 0
        #             if (ival > 255):
        #                 ival = 255
        
        #             bi.putpixel((x+(i*74), y), (ival, ival, ival))
        # bi.save(fileName)

    #                      String    int[]
    def loadRawImage(self, filename, raw):
        with open(filename, 'rb') as f:
            f.seek(27)
            while True:
                byte_s = f.read(2)
                if not byte_s or len(byte_s) < 2:
                    break
                v = int(byte_s[0] & 0xFF)
                v |= int(byte_s[1] & 0xFF) << 8
                raw.append(v)
        self.printMessage(filename + " loaded. Size = " + str(len(raw)))

    def trainRejector(self, ast_rejector):
        # read training file
        print("\nTraining")
        det_id = 0
        num_train_rjct = 0
        # BufferedReader br = new BufferedReader(new FileReader(trainFile))
        for s in open(trainFile, 'r'):
            # self.printMessage(s)
            if (not s):
                break
            s = s.rstrip()
            # load raw image data
            rawTraining = []
            self.loadRawImage(folder + s + ".raw", rawTraining)
            # load detection data
            detTraining = []
            brdet = open(folder + s + ".det")
            cnt = 0
            trainAns = []
            while (True):
                row = brdet.readline()
                if (not row):
                    break

                row = str(det_id) + " " + row
                if (row[-2] == '1'):
                    num_train_rjct += 1
                    trainAns.append(det_id)

                detTraining.append(row)
                cnt += 1
                if ((cnt % 4) == 0):
                    det_id += 1

            brdet.close()
            trainAns = set(trainAns)  # convert the built list of rejected files to a set

            self.printMessage(folder + s + ".det loaded. Rows = " + str(len(detTraining)))

            if (self.visualize):
                n = int(len(rawTraining)/(4*64*64))
                for i in range(int(len(rawTraining)/(4*64*64))):
                    case_num = det_id - n + i
                    fileName = str(case_num) + ".png"
                    if (case_num in trainAns):
                        fileName = "R_" + fileName
                    else:
                        fileName = "D_" + fileName
                    self.visualizeImg(rawTraining, i*4*64*64, fileName)

            # call trainingData(imageData, detections)
            ast_rejector.training_data(rawTraining, detTraining)

    def testRejector(self, ast_rejector):
        # read testing file
        print("\nTesting")
        det_id = 0
        modelAnsReject = set()
        modelAnsDetect = set()
        for s in open(testFile):
            # self.printMessage(s)
            if (not s):
                break
            s = s.rstrip()
            # load raw image data
            rawTest = []
            self.loadRawImage(folder + s + ".raw", rawTest)
            # load detection data
            detTest = []
            brdet = open(folder + s + ".det")
            cnt = 0
            while (True):
                row = brdet.readline()
                if (not row):
                    break
                row = str(det_id) + " " + row
                if (row[-2] == '1'):
                    modelAnsReject.add(det_id)
                else:
                    modelAnsDetect.add(det_id)

                # remove truth
                # row = row[:-2]
                detTest.append(row)
                cnt += 1
                if ((cnt % 4) == 0):
                    det_id += 1
            brdet.close()

            self.printMessage(folder + s + ".det loaded. Rows = " + str(len(detTest)))

            if (self.visualize):
                n = len(rawTest)/(4*64*64)
                for i in range(len(rawTest)/(4*64*64)):
                    case_num = det_id - n + i
                    fileName = str(case_num) + ".png"
                    if case_num in modelAnsReject:
                        fileName = "R_" + fileName
                    else:
                        fileName = "D_" + fileName
                    self.visualize(rawTest, i*4*64*64, fileName)
            # pass the testing data to the asteroid_rejector
            if len(rawTest) != len(detTest)*64*64:
                print("ERROR: ", len(rawTest)/(64*64), " vs ", len(detTest))
                continue

            ast_rejector.testing_data(rawTest, detTest)
        return modelAnsReject, modelAnsDetect

    def answerRejector(self, ast_rejector):
        print("\nRetrieving Answer")
        return ast_rejector.get_answer()

    def doExec(self):
        self.printMessage("Executing your solution: " + self.execCommand + ".")
        # create solution class
        ast_rejector = AsteroidRejector()

        # train the asteroid rejector
        self.trainRejector(ast_rejector)

        modelAnsReject, modelAnsDetect = self.testRejector(ast_rejector)

        # get response from solution
        userAns = list(self.answerRejector(ast_rejector))

        n = len(userAns)
        if (n != len(modelAnsReject) + len(modelAnsDetect)):
            self.printMessage("Invalid number of detections. {}  expected, but {} in list.".format(len(modelAnsReject) + len(modelAnsDetect), n))
            self.printMessage("Score = 0")

        # call scoring function
        score = self.scoreAnswer(userAns, modelAnsDetect, modelAnsReject)
        print("Score = ", score)
        os.system('say "reject tester complete"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process test input.')
    parser.add_argument("-train", "--train_file")
    parser.add_argument("-test", "--test_file")
    parser.add_argument("-exec", "--exec_command")
    parser.add_argument("-debug", "--debug_messages", action='store_true')
    parser.add_argument("-folder", "--folder_name")
    parser.add_argument("-vis", "--visualize", action='store_true')
    args = parser.parse_args()

    trainFile = args.train_file
    testFile = args.test_file
    folder = args.folder_name
    execCommand = args.exec_command
    vis = args.visualize
    dbg = args.debug_messages

    try:
        if (trainFile and testFile and execCommand):
            art = RejectTester(trainFile, testFile, execCommand, visualize=vis, debug=dbg)
            art.doExec()
        else:
            print("WARNING: nothing to do for this combination of arguments.")
    except Exception as e:
        print(e)
