import random
import numpy as np
# random.seed(2)
# np.random.seed(2)


import argparse
import os

import util
from constant import DEFAULT_MAX_ITER, DEFAULT_MAX_TIME
from fuzzer import Fuzzer
from fuzzer_config import FuzzerConfig


def check_run_limit(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("%s is not a valid argument" % value)
    if ivalue < -1:
        raise argparse.ArgumentTypeError("%s is an invalid value, must be >= -1" % value)
    return ivalue

def convert_to_int(value):
    return int(value)

def decide_max(args):
    # suspending max_time as timeout may cause pipe error for multiprocessing
    if args.max_time != 0:
        util.error('--max_time is suspended, please use --max_iter instead')
    if args.max_iter == 0 and args.max_time == 0:
        util.warning('both --max_iter and --max_time are 0, will use default')
        args.max_iter = DEFAULT_MAX_ITER
    elif args.max_iter != 0 and args.max_time != 0:
        args.max_time = 0
    return


def check_dir_exist(d):
    d = os.path.abspath(d)
    if not os.path.isdir(d):
        raise argparse.ArgumentTypeError("%s is not a valid work directory" % d)
    return d


def check_positive(value):
    fvalue = float(value)
    if fvalue > 0:
        return fvalue
    else:
        raise argparse.ArgumentTypeError("%s is not a positive number" % value)


def check_positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue



def check_rate(rate):
    irate = float(rate)
    if irate>1 or irate<0:
        raise argparse.ArgumentTypeError("%s is not a float between 0 and 1" % rate)
    return irate
        
def save_config(config_data):
    util.save_yaml(config_data['workdir']+'/fuzzing_config',config_data)

# def check_adapt_option(choice):
#     if choice != 'prev_ok' and choice != 'permute':
#         raise argparse.ArgumentTypeError("%s is not a valid option")
#     return choice


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_config', help='The configuration file for the target function under test')
    parser.add_argument('dtype_config', help='The configuration file to specify the valid data types')
    parser.add_argument('--data_construct', type=str, help='Optional constructor function for building the input')
    parser.add_argument('--fuzz_optional_p', type= check_rate, default=1,
                        help='Optional: probablity to include each optional parameters. default:1')
    parser.add_argument('--model_test', default=False, action='store_true',
                        help='Flag indicating whether to generate input for the layer APIs. Defualt: False')
    parser.add_argument('--check_nan', default=False, action='store_true',
                        help='Flag indicating whether to report NaN errors of the layer API inference.  Defualt: False')

    parser.add_argument('--mutate_p', type= check_rate, default=0,
                        help='Optional: probablity to mutate each parameter to one of the boundary cases. Default: 0')
    parser.add_argument('--guided_mutate',  default=False, action='store_true',
                        help='Optional: Whether to use guided mutation to maximize mutation operation coverage. Default: False')

    parser.add_argument('--special_value', default=False, action='store_true',
                    help='Flag indicating whether to include special values (e.g. inf, nan) in mutation. Default: False')

    parser.add_argument('--gen_script', default=False, action='store_true',
                        help='Flag to specify whether to generate a python script for the testing')
    parser.add_argument('--save', default=False, action='store_true',
                        help='Flag to specify whether to save all related input and python script even it is not related to crash.')
    parser.add_argument('--save_cnt', default=-1, type=convert_to_int, 
                        help='Only save the first <save_cnt> valid inputs while save=False. When it is negative, ignored.')
    parser.add_argument('--ignore', default=False, action='store_true',
                        help='If specified, the fuzzer ignores the given constraints')
    parser.add_argument('--max_iter', type=check_run_limit, default=0,
                        help='The maximum number of iterations the fuzzer runs; if -1, fuzzer runs indefinitely; '
                             'default %d iterations; this argument overrules --max_time' % DEFAULT_MAX_ITER)
    parser.add_argument('--max_time', type=check_run_limit, default=0,
                        help='The maximum time in seconds the fuzzer runs; if -1, fuzzer runs indefinitely; '
                             'default %d seconds' % DEFAULT_MAX_TIME)
    parser.add_argument('--conform', default=False, action='store_true',
                        help='Flag whether the fuzzer should conform (otherwise violate) the given constraints')
    parser.add_argument('--timeout', default=5, type=check_positive,
                        help='Timeout limit for each testing run, default to 5 sec')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='Verbose flag whether to block output during testing phase')
    parser.add_argument('--workdir', type=check_dir_exist,
                        help='Work directory to store the suspicious inputs;'
                             'if none provided, will store in current workdir')

    args = parser.parse_args()
    # util.DEBUG("Global seed random.seed=%s, np.random.seed=%s" %())
    decide_max(args)  # make sure only one of max_iter or max_time is used
    # args.target_config = target_config
    # args.dtype_config = dtype_config

    configs = vars(args)  # return dict object of args
    save_config(configs)    # save config 

    # read the config files
    configs['target_config'] = util.read_yaml(os.path.abspath(args.target_config))
    configs['dtype_config'] = util.read_yaml(os.path.abspath(args.dtype_config))

    fuzzer_config = FuzzerConfig(configs)

    fuzzer = Fuzzer(fuzzer_config, args.data_construct)

    
    fuzzer.run(obey=args.conform, max_iter=args.max_iter, max_time=args.max_time, gen_script=args.gen_script)

  


if __name__ == '__main__':
    main()
