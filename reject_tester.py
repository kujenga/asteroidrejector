#!//anaconda/bin/python
# tests the AsteroidRejector

import argparse
from PIL import Image
import math

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
    #               int[]    Set<Integer>    Set<Integer>
    def scoreAnswer(self, userAns, modelAnsDetect, modelAnsReject):
        score = 0.0
        total = 0
        correct = 0
        userAnsUsed = set([])
        for i in range(userAns.length):
            total += 1.0
            id = userAns[i]
            if not modelAnsDetect.contains(id) and not modelAnsReject.contains(id):
                self.printMessage("Unique ID " + id + " not valid.")
                return 0.0

            if userAnsUsed.contains(id):
                self.printMessage("Unique ID " + id + " already used.")
                return 0.0

            userAnsUsed.add(id)

            if modelAnsDetect.contains(id):
                correct += 1.0
                self.printMessage("1")
                score += (1000000.0 / modelAnsDetect.size()) * (correct / total)

            self.printMessage("0")

        return score

    #                      int[]  int     String
    def visualizeImg(self, raw,   offset, fileName):
        W = (64+10)*4-10
        bi = Image.new('RGB', (W, 64))
        # g = (Graphics2D)bi.getGraphics()
        for y in range(64):
            for x in range(W):
                bi.putpixel((x, y), 0xffffff)
        for i in range(4):
            off = offset + i*64*64
            imin = 1 << 20
            imax = -imin
            # Find min and max
            for j in range(4096):
                r = raw[j+off]
                if (r > 65500):
                    continue
                imin = min(imin, r)
                imax = max(imax, r)

            dmax = float((imax) / 256.0)
            dmin = float((imin) / 256.0)
            if (dmax*0.5-dmin > 10):
                dmax *= 0.5

            if (dmax-dmin < 0.0001):
                dmax += 0.1

            linearF = 255.0 / (dmax - dmin)
            log10 = math.log(10.0)
            logF = 255.0 / (math.log(255.0) / log10)
            for y in range(64):
                for x in range(64):
                    ival = raw[off]
                    off += 1
                    dval = float((ival) / 256.0)
                    if (dval < dmin):
                        ival = 0
                    elif (dval > dmax):
                        ival = 255
                    else:
                        dval = max(0.0, min(dval-dmin, dmax - dmin))
                        d = 0.0
                        if dval * linearF != 0.0:
                            d = ((math.log(dval * linearF)) / log10) * logF
                        ival = int(d)
                    if (ival < 0):
                        ival = 0
                    if (ival > 255):
                        ival = 255

                    bi.putpixel((x+(i*74), y), (ival, ival, ival))
        bi.save(fileName)

    #                String    ArrayList<int>
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
        print(filename + " loaded. Size = " + str(len(raw)))

    def trainRejector(self, ast_rejector):
        # read training file
        self.printMessage("Training...")
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
        self.printMessage("Testing...")
        det_id = 0
        modelAnsReject = set([])
        modelAnsDetect = set([])
        for s in open(testFile):
            # self.printMessage(s)
            if (not s):
                break

            # load raw image data
            rawTest = []
            self.loadRawImage(folder + s + ".raw", rawTest)
            # load detection data
            detTest = []
            brdet = open(folder + s + ".det", 'w')
            cnt = 0
            while (True):
                row = brdet.readline()
                if (not row):
                    break
                row = det_id + " " + row
                if (row.charAt(row.length()-1) == '1'):
                    modelAnsReject.add(det_id)
                else:
                    modelAnsDetect.add(det_id)

                # remove truth
                row = row.substring(0, row.length()-2)
                detTest.add(row)
                cnt += 1
                if ((cnt % 4) == 0):
                    det_id += 1
            brdet.close()

            if (self.visualize):
                n = len(rawTest)/(4*64*64)
                for i in range(len(rawTest)/(4*64*64)):
                    case_num = det_id - n + i
                    fileName = case_num + ".png"
                    if (modelAnsReject.contains(case_num)):
                        fileName = "R_" + fileName
                    else:
                        fileName = "D_" + fileName
                    self.visualize(rawTest, i*4*64*64, fileName)

            ast_rejector.training_data(rawTest, detTest)

    def doExec(self):
        self.printMessage("Executing your solution: " + self.execCommand + ".")
        # create solution class
        ast_rejector = AsteroidRejector()

        # train the asteroid rejector
        self.trainRejector(ast_rejector)

        self.testRejector(ast_rejector)

        # get response from solution
        # cmd = reader.readLine()
        # n = int(cmd)
        # if (n != modelAnsReject.size() + modelAnsDetect.size()):
        #     self.printMessage("Invalid number of detections in return. " + (modelAnsReject.size()+modelAnsDetect.size()) + " expected, but " + n + " in list.")
        #     self.printMessage("Score = 0")
        #
        # userAns = [0]*n
        # for i in range(n):
        #     val = reader.readline()
        #     userAns[i] = int(val)
        #
        # # call scoring function
        # score = self.scoreAnswer(userAns, modelAnsDetect, modelAnsReject)
        # self.printMessage("Score = " + score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process test input.')
    parser.add_argument("-train", "--train_file")
    parser.add_argument("-test", "--test_file")
    parser.add_argument("-exec", "--exec_command")
    parser.add_argument("-silent", "--silent_debug", action='store_true')
    parser.add_argument("-folder", "--folder_name")
    parser.add_argument("-vis", "--visualize", action='store_true')
    args = parser.parse_args()

    trainFile = args.train_file
    testFile = args.test_file
    folder = args.folder_name
    execCommand = args.exec_command
    vis = args.visualize
    silent = args.silent_debug

    try:
        if (trainFile and testFile and execCommand):
            art = RejectTester(trainFile, testFile, execCommand, visualize=vis)
            art.doExec()
        else:
            print("WARNING: nothing to do for this combination of arguments.")
    except Exception as e:
        print(e)

# class ErrorStreamRedirector:
#     public BufferedReader reader
#
#     public ErrorStreamRedirector(InputStream is):
#         reader = new BufferedReader(new InputStreamReader(is))
#
#
#     def run():
#         while (true):
#             String s
#             try {
#                 s = reader.readLine()
#             except Exception, e:
#                 # e.printStackTrace()
#                 return
#             }
#             if s == null:
#                 break
#
#             System.out.println(s)
