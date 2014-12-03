#!//anaconda/bin/python
# tests the AsteroidRejector

import argparse

# boolean
debug = true
# boolean
visualize = false
# String
execCommand = null
# String
trainFile = null
# String
testFile = null
# String
folder = ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process test input.')
    parser.add_argument("-train", "--train_file")
    parser.add_argument("-test", "--test_file")
    parser.add_argument("-exec", "--exec_command")
    parser.add_argument("-silent", "--silent_debug", nargs='0')
    parser.add_argument("-folder", "--folder_name")
    parser.add_argument("-vis", "--visualize", nargs='0')
    args = parser.parse_args()

    trainFile = args.train_file
    testFile = args.test_file
    folder = args.folder
    execCommand = args.exec_command
    if args.visualize:
        visualize = true
    if args.silent_debug:
        debug = false


class AsteroidRejectTester:


    def printMessage(s):
        if (debug):
            print(s)

    # String
    _ = File.separator

    # Score a testcase, given detections and rejections and user answers
    #               int[]    Set<Integer>    Set<Integer>
    def scoreAnswer(userAns, modelAnsDetect, modelAnsReject):
        score = 0.0
        total = 0
        correct = 0
        userAnsUsed = set([])
        for i in range(userAns.length):
            total += 1.0
            id = userAns[i]
            if not modelAnsDetect.contains(id) and not modelAnsReject.contains(id):
                printMessage("Unique ID " + id + " not valid.")
                return 0.0

            if userAnsUsed.contains(id):
                printMessage("Unique ID " + id + " already used.")
                return 0.0

            userAnsUsed.add(id)

            if modelAnsDetect.contains(id):
                correct += 1.0
                printMessage("1")
                score += (1000000.0 / modelAnsDetect.size()) * (correct / total)

            printMessage("0")

        return score

    #              ArrayList<int>  int     String
    def visualize(raw,             offset, fileName):

        W = (64+10)*4-10
        BufferedImage bi = new BufferedImage(W, 64, 1)
        Graphics2D g = (Graphics2D)bi.getGraphics()
        for y in range(64):
            for x in range(W):
                bi.setRGB(x, y, 0xffffff)
            for i in range(4):
                int off = offset + i*64*64
                int imin = 1 << 20
                int imax = -imin
                # Find min and max
                for j in range(4096):
                    int r = raw.get(j+off)
                    if (r > 65500):
                        continue
                    imin = Math.min(imin, r)
                    imax = Math.max(imax, r)

                double dmax = (double)(imax) / 256.0
                double dmin = (double)(imin) / 256.0
                if (dmax*0.5-dmin > 10):
                    dmax *= 0.5

                if (dmax-dmin < 0.0001):
                    dmax += 0.1

                double linearF = 255.0 / (dmax - dmin)
                double log10 = Math.log(10.0)
                double logF = 255.0 / (Math.log(255.0) / log10)
                for y in range(64):
                    for x in range(64):
                        int ival = raw.get(off++)
                        double dval = (double)(ival) / 256.0
                        if (dval < dmin):
                            ival = 0
                        elif (dval > dmax):
                            ival = 255
                        else:
                            dval = Math.max(0.0, Math.min(dval-dmin, dmax - dmin))
                            double d = ((Math.log(dval * linearF)) / log10) * logF
                            ival = (int)(d)

                        if (ival < 0):
                            ival = 0
                        if (ival > 255):
                            ival = 255
                        int cr = ival
                        int cg = ival
                        int cb = ival
                        int rgb = cr + (cg << 8) + (cb << 16)
                        bi.setRGB(x+(i*74), y, rgb)
            ImageIO.write(bi, "PNG", new File(fileName))

    #                String    ArrayList<int>
    def loadRawImage(filename, raw):
        ObjectInputStream fi = new ObjectInputStream(new FileInputStream(filename))
        byte[] rawbytes = (byte[]) fi.readObject()
        for in range(0, rawbytes.length, 2):
            v = (int)(rawbytes[i] & 0xFF)
            v |= (int)(rawbytes[i+1] & 0xFF) << 8
            raw.add(v)
        # printMessage(filename + " loaded. Size = " + raw.size())

    def doExec():

        # launch solution
        printMessage("Executing your solution: " + execCommand + ".")
        Process solution = Runtime.getRuntime().exec(execCommand)

        BufferedReader reader = new BufferedReader(new InputStreamReader(solution.getInputStream()))
        PrintWriter writer = new PrintWriter(solution.getOutputStream())
        new ErrorStreamRedirector(solution.getErrorStream()).start()

        # read training file
        printMessage("Training...")
        det_id = 0
        num_train_rjct = 0
        BufferedReader br = new BufferedReader(new FileReader(trainFile))
        while (true) {
            String s = br.readLine()
            # printMessage(s)
            if (s == null):
                break
            # load raw image data
            rawTraining = []
            loadRawImage(folder + s + ".raw", rawTraining)
            # load detection data
            detTraining = []
            BufferedReader brdet = new BufferedReader(new FileReader(folder + s + ".det"))
            cnt = 0
            trainAns = set([])
            while (true):
                String row = brdet.readLine()
                if (row == null):
                    break

                row = det_id + " " + row
                if (row.charAt(row.length()-1) == '1'):
                    num_train_rjct++
                    trainAns.add(det_id)

                detTraining.add(row)
                cnt++
                if ((cnt % 4) == 0):
                    det_id++

            brdet.close()
            # printMessage(folder + s + ".det loaded. Rows = " + detTraining.size())

            if (visualize):
                for i in range(rawTraining.size()/(4*64*64)):
                    int case_num = det_id - n + i
                    String fileName = case_num + ".png"
                    if (trainAns.contains(case_num)):
                        fileName = "R_" + fileName
                    else:
                        fileName = "D_" + fileName
                    visualize(rawTraining, i*4*64*64, fileName)

            # call trainingData(imageData, detections)
            int[] imageData_train = new int[rawTraining.size()]
            for i in range(rawTraining.size()):
                imageData_train[i] = rawTraining.get(i)

            String[] detections_train = new String[detTraining.size()]
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
            String trainResp = reader.readLine()
        br.close()

        # read testing file
        printMessage("Testing...")
        modelAnsReject = set([])
        modelAnsDetect = set([])
            BufferedReader br = new BufferedReader(new FileReader(testFile))
            while (true) {
                String s = br.readLine()
                # printMessage(s)
                if (s == null):
                    break

                # load raw image data
                rawTest = []
                loadRawImage(folder + s + ".raw", rawTest)
                # load detection data
                detTest = []
                BufferedReader brdet = new BufferedReader(new FileReader(folder + s + ".det"))
                int cnt = 0
                while (true):
                    String row = brdet.readLine()
                    if (row == null) {
                        break
                    }
                    row = det_id + " " + row
                    if (row.charAt(row.length()-1) == '1'):
                        modelAnsReject.add(det_id)
                    else:
                        modelAnsDetect.add(det_id)

                    # remove truth
                    row = row.substring(0, row.length()-2)
                    detTest.add(row)
                    cnt++
                    if ((cnt % 4) == 0):
                        det_id++

                brdet.close()

                if (visualize):
                    for i in range(rawTest.size()/(4*64*64)):
                        int case_num = det_id - n + i
                        String fileName = case_num + ".png"
                        if (modelAnsReject.contains(case_num)):
                            fileName = "R_" + fileName
                        else:
                            fileName = "D_" + fileName
                        visualize(rawTest, i*4*64*64, fileName)



                # call testData(imageData, detections)
                int[] imageData_test = new int[rawTest.size()]
                for i in range(rawTest.size()):
                    imageData_test[i] = rawTest.get(i)
                String[] detections_test = new String[detTest.size()]
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
                String testResp = reader.readLine()

            }
            br.close()


        # get response from solution
        String cmd = reader.readLine()
        int n = Integer.parseInt(cmd)
        if (n != modelAnsReject.size()+modelAnsDetect.size()):
            printMessage("Invalid number of detections in return. " + (modelAnsReject.size()+modelAnsDetect.size()) + " expected, but " + n + " in list.")
            printMessage("Score = 0")

        int[] userAns = new int[n]
        for i in range(n):
            String val = reader.readLine()
            userAns[i] = Integer.parseInt(val)

        # call scoring function
        double score = scoreAnswer(userAns, modelAnsDetect, modelAnsReject)
        printMessage("Score = " + score)



    def main(String[] args):
       for i in range(args.length):
            if (args[i].equals("-train")):
                trainFile = args[++i]
            elif (args[i].equals("-test")):
                testFile = args[++i]
            elif (args[i].equals("-exec")):
                execCommand = args[++i]
            elif (args[i].equals("-silent")):
                debug = false
            elif (args[i].equals("-folder")):
                folder = args[++i]
            elif (args[i].equals("-vis")):
                visualize = true
            else:
                print("WARNING: unknown argument " + args[i] + ".")
        try:
            if (trainFile != null and testFile != null and execCommand != null):
                new AsteroidRejectTester().doExec()
            else:
                System.out.println("WARNING: nothing to do for this combination of arguments.")
        except Exception, e:
            System.out.println("FAILURE: " + e.getMessage())
            e.printStackTrace()


class ErrorStreamRedirector:
    public BufferedReader reader

    public ErrorStreamRedirector(InputStream is):
        reader = new BufferedReader(new InputStreamReader(is))


    def run():
        while (true):
            String s
            try {
                s = reader.readLine()
            except Exception, e:
                # e.printStackTrace()
                return
            }
            if s == null:
                break

            System.out.println(s)
