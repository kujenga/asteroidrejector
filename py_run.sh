# a script to automatically run the test program

# customizable arguments
if [ '-d ~/Documents' ]; then
  DATA_FOLDER='./offline_training/'
else
  DATA_FOLDER='/mnt/idms/AIT_Aaron/offline_training/'
fi

TRAIN_FILE='./example_data/example_train.txt'
TEST_FILE='./example_data/example_test.txt'

# command supplied by the competition
python3 reject_tester.py -folder $DATA_FOLDER -train $TRAIN_FILE -test $TEST_FILE -exec 'python3 asteroid_rejector.py' # -debug -vis
