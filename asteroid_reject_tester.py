#!//anaconda/bin/python
# tests the AsteroidRejector

import argparse

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


class AsteroidRejectTester:

    def __init__(self, trainFile, testFile, execCommand, debug=True):
        print("initializing")
        self.trainFile = trainFile
        self.testFile = testFile
        self.execCommand = execCommand
        self.debug = debug

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

    #              ArrayList<int>  int     String
    # def visualize(raw,             offset, fileName):
    #
    #     W = (64+10)*4-10
    #     BufferedImage bi = BufferedImage(W, 64, 1)
    #     Graphics2D g = (Graphics2D)bi.getGraphics()
    #     for y in range(64):
    #         for x in range(W):
    #             bi.setRGB(x, y, 0xffffff)
    #         for i in range(4):
    #             int off = offset + i*64*64
    #             int imin = 1 << 20
    #             int imax = -imin
    #             # Find min and max
    #             for j in range(4096):
    #                 int r = raw.get(j+off)
    #                 if (r > 65500):
    #                     continue
    #                 imin = Math.min(imin, r)
    #                 imax = Math.max(imax, r)
    #
    #             double dmax = (double)(imax) / 256.0
    #             double dmin = (double)(imin) / 256.0
    #             if (dmax*0.5-dmin > 10):
    #                 dmax *= 0.5
    #
    #             if (dmax-dmin < 0.0001):
    #                 dmax += 0.1
    #
    #             double linearF = 255.0 / (dmax - dmin)
    #             double log10 = Math.log(10.0)
    #             double logF = 255.0 / (Math.log(255.0) / log10)
    #             for y in range(64):
    #                 for x in range(64):
    #                     int ival = raw.get(off++)
    #                     double dval = (double)(ival) / 256.0
    #                     if (dval < dmin):
    #                         ival = 0
    #                     elif (dval > dmax):
    #                         ival = 255
    #                     else:
    #                         dval = Math.max(0.0, Math.min(dval-dmin, dmax - dmin))
    #                         double d = ((Math.log(dval * linearF)) / log10) * logF
    #                         ival = (int)(d)
    #
    #                     if (ival < 0):
    #                         ival = 0
    #                     if (ival > 255):
    #                         ival = 255
    #                     int cr = ival
    #                     int cg = ival
    #                     int cb = ival
    #                     int rgb = cr + (cg << 8) + (cb << 16)
    #                     bi.setRGB(x+(i*74), y, rgb)
    #         ImageIO.write(bi, "PNG", new File(fileName))

    #                String    ArrayList<int>
    def loadRawImage(filename, raw):
        with open(filename, 'rb') as f:
            while 1:
                byte_s = f.read(12)
                if not byte_s:
                    break
                byte = byte_s[0]
                v = (int)(rawbytes[i] & 0xFF)
                v |= (int)(rawbytes[i+1] & 0xFF) << 8
                raw.append(v)
        print(filename + " loaded. Size = " + str(len(raw)))

    def doExec(self):

        # launch solution
        self.printMessage("Executing your solution: " + self.execCommand + ".")

        ast_rejector = AsteroidRejector()

        # solution = Popen(execCommand.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
        # stdout_data = solution.communicate(input='data_to_write')[0]

        # reader = new BufferedReader(InputStreamReader(solution.getInputStream()))
        # PrintWriter writer = new PrintWriter(solution.getOutputStream())
        # new ErrorStreamRedirector(solution.getErrorStream()).start()

        # read training file
        self.printMessage("Training...")
        det_id = 0
        num_train_rjct = 0
        # BufferedReader br = new BufferedReader(new FileReader(trainFile))
        for s in open(trainFile, 'r'):
            # self.printMessage(s)
            if (s == null):
                break
            # load raw image data
            rawTraining = []
            loadRawImage(folder + s + ".raw", rawTraining)
            # load detection data
            detTraining = []
            brdet = open(folder + s + ".det")
            cnt = 0
            trainAns = set([])
            while (true):
                row = brdet.readline()
                if (row == null):
                    break

                row = det_id + " " + row
                if (row.charAt(row.length()-1) == '1'):
                    num_train_rjct += 1
                    trainAns.add(det_id)

                detTraining.add(row)
                cnt += 1
                if ((cnt % 4) == 0):
                    det_id += 1

            brdet.close()
            # self.printMessage(folder + s + ".det loaded. Rows = " + detTraining.size())

            if (visualize):
                for i in range(rawTraining.size()/(4*64*64)):
                    case_num = det_id - n + i
                    fileName = case_num + ".png"
                    if (trainAns.contains(case_num)):
                        fileName = "R_" + fileName
                    else:
                        fileName = "D_" + fileName
                    visualize(rawTraining, i*4*64*64, fileName)

            # call trainingData(imageData, detections)
            imageData_train = [0]*len(rawTraining)
            for i in range(len(rawTraining)):
                imageData_train[i] = rawTraining.get(i)

            detections_train = [""]*len(detTraining)
            detTraining.toArray(detections_train)

            writer.println(imageData_train.length)
            for v in imageData_train:
                writer.println(v)

            writer.flush()

            writer.println(detections_train.length)
            for v in detections_train:
                writer.println(v)

            writer.flush()

            # get response from solution
            trainResp = reader.readline()
        br.close()

        # read testing file
        self.printMessage("Testing...")
        modelAnsReject = set([])
        modelAnsDetect = set([])
        for s in open(testFile):
            # self.printMessage(s)
            if (s == null):
                break

            # load raw image data
            rawTest = []
            loadRawImage(folder + s + ".raw", rawTest)
            # load detection data
            detTest = []
            brdet = open(folder + s + ".det", 'w')
            cnt = 0
            while (true):
                row = brdet.readline()
                if (row == null):
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

            if (visualize):
                for i in range(rawTest.size()/(4*64*64)):
                    case_num = det_id - n + i
                    fileName = case_num + ".png"
                    if (modelAnsReject.contains(case_num)):
                        fileName = "R_" + fileName
                    else:
                        fileName = "D_" + fileName
                    visualize(rawTest, i*4*64*64, fileName)

            # call testData(imageData, detections)
            imageData_test = [0]*len(rawTest)
            for i in range(rawTest.size()):
                imageData_test[i] = rawTest.get(i)
            detections_test = [""]*len(detTest)
            detTest.toArray(detections_test)

            writer.println(imageData_test.length)
            for v in imageData_test:
                writer.println(v)

            writer.flush()

            writer.println(detections_test.length)
            for v in detections_test:
                writer.println(v)

            writer.flush()

            # get response from solution
            testResp = reader.readline()

        # # get response from solution
        # cmd = reader.readLine()
        # n = Integer.parseInt(cmd)
        # if (n != modelAnsReject.size()+modelAnsDetect.size()):
        #     self.printMessage("Invalid number of detections in return. " + (modelAnsReject.size()+modelAnsDetect.size()) + " expected, but " + n + " in list.")
        #     self.printMessage("Score = 0")
        #
        # int[] userAns = new int[n]
        # for i in range(n):
        #     String val = reader.readLine()
        #     userAns[i] = Integer.parseInt(val)
        #
        # # call scoring function
        # double score = scoreAnswer(userAns, modelAnsDetect, modelAnsReject)
        # self.printMessage("Score = " + score)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process test input.')
    parser.add_argument("-train", "--train_file")
    parser.add_argument("-test", "--test_file")
    parser.add_argument("-exec", "--exec_command")
    parser.add_argument("-silent", "--silent_debug")
    parser.add_argument("-folder", "--folder_name")
    parser.add_argument("-vis", "--visualize")
    args = parser.parse_args()

    trainFile = args.train_file
    testFile = args.test_file
    folder = args.folder_name
    execCommand = args.exec_command
    if args.visualize:
        visualize = True
    if args.silent_debug:
        debug = False

    try:
        if (trainFile and testFile and execCommand):
            art = AsteroidRejectTester(trainFile, testFile, execCommand)
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
