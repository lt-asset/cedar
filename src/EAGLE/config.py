# the directory where data is stored, including generated input and output files
DATA_DIR = "/home/workdir/"

# specifics of done file
TEST_DONE_COLS = ['rule', 'lib', 'version', 'api', 'input_index', 'done']
TEST_DONE_FILE = "test_done.csv"

# number of arguments generated
NUM_OF_ARGS = 50
# number of inputs generated
NUM_OF_INPUT = 50

TF_NAME = "tensorflow"
PT_NAME = "pytorch"

# the max value for matrix input generation
MAX_MATRIX_VALUE = 100

TIMEOUT = 30

# threshold for the inconsistency
RTOL = 1e-05
ATOL = 1e-02