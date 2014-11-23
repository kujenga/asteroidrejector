# a script to automatically run the test program

DATA_FOLDER='offline_training'
TRAIN_FILE=''
TEST_FILE=''

EXEC_COMMAND='python asteroid_rejector.py'

java -jar tester.jar -folder $DATA_FOLDER -train $TRAIN_FILE -test $TEST_FILE -exec $EXEC_COMMAND -vis
