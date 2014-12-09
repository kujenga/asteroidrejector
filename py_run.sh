# a script to automatically run the test program

# customizable arguments
if [ '-d ~/Documents' ]; then
  DATA_FOLDER='./offline_training/'
  TRAIN_FILE='./example_data/tiny_train.txt'
  TEST_FILE='./example_data/tiny_test.txt'
else
  DATA_FOLDER='/mnt/idms/AIT_Aaron/offline_training/'
  TRAIN_FILE='./example_data/tiny_train.txt'
  TEST_FILE='./example_data/tiny_test.txt'
fi

# command supplied by the competition
python3 reject_tester.py -folder $DATA_FOLDER -train $TRAIN_FILE -test $TEST_FILE -exec 'python3 asteroid_rejector.py' # -debug -vis
