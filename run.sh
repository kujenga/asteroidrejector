# a script to automatically run the test program

# customizable arguments
DATA_FOLDER='./offline_training/'
TRAIN_FILE='./example_data/example_train.txt'
TEST_FILE='./example_data/example_test.txt'

EXEC_COMMAND='python ./asteroid_rejector.py'

# command supplied by the competition
java -jar tester.jar -folder $DATA_FOLDER -train $TRAIN_FILE -test $TEST_FILE -exec $EXEC_COMMAND -vis
