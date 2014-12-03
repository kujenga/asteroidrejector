# a script to automatically run the test program

# customizable arguments
DATA_FOLDER='./offline_training/'
TRAIN_FILE='./example_data/example_train.txt'
TEST_FILE='./example_data/example_test.txt'

# command supplied by the competition
python asteroid_reject_tester.py -folder $DATA_FOLDER -train $TRAIN_FILE -test $TEST_FILE -exec 'python asteroid_rejector.py' # -vis
