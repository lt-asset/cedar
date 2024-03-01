import os
import pickle
import numpy as np
import subprocess
import argparse
import traceback
import csv
from rules.equiv_util import get_argument_file_path

import running_utils
from config import DATA_DIR, NUM_OF_INPUT, TEST_DONE_COLS, TEST_DONE_FILE, RTOL, ATOL, TF_NAME, PT_NAME

def get_index(file_name):
    return int(file_name.split('/')[-1].split('.')[0])

def main():
    # this file is used to compare the results of the testing rules
    parser = argparse.ArgumentParser()
    parser.add_argument("lib", choices=['tensorflow', 'pytorch'])
    parser.add_argument("version", type=str)
    args = parser.parse_args()
    config = vars(args)

    lib = config['lib']
    version = config['version']

    in_dir = DATA_DIR
    results_dir = os.path.join(DATA_DIR, "rule_output")

    tf_api_list = running_utils.load_list(os.path.join('input_generation', 'input_gen_tensorflow_api_list.txt'))
    pt_api_list = running_utils.load_list(os.path.join('input_generation', 'input_gen_pytorch_api_list.txt'))

    apis_map = {
        TF_NAME: tf_api_list,
        PT_NAME: pt_api_list
    }

    eagle_save_list = []
    doctor_save_list = []
    input_save_list = []

    input_rule_list = [
        "rule_2", 
        "rule_3", 
        "rule_4",
        "rule_5",
        "rule_6",
        "rule_7", 
        "rule_9",  
        "rule_10",
        "rule_11",
        "rule_14"
    ]

    csv_file_path = os.path.join(DATA_DIR, "{}_{}_output_file.csv".format(lib, version))
    with open(csv_file_path, mode='r') as csv_file:
        csvreader = csv.reader(csv_file)
        next(csvreader)
        for row in csvreader:
            try:
                print(row)
                rule = row[0]
                api_name = row[1]
                linf = row[2]
                output_file_name = row[3]
                print(get_index(output_file_name))
                if rule not in ["rule_15", "rule_16"]:
                    if api_name in apis_map[lib]:
                        eagle_save_list.append(get_argument_file_path(in_dir, lib, version, api_name, get_index(output_file_name)))
                    else:
                        doctor_save_list.append(get_argument_file_path(in_dir, lib, version, api_name, get_index(output_file_name)))
                    if rule in input_rule_list:
                        input_dir = os.path.join(in_dir, 'generated_input/input')
                        input_file = os.path.join(input_dir, "%d.npy" % get_index(output_file_name))
                        if input_file not in input_save_list:
                            input_save_list.append(input_file)
            except Exception as e:
                print(e)
                traceback.print_exc()
                pass

    with open(os.path.join(DATA_DIR, "doctor_save_list.txt"), "w") as f:
        for item in doctor_save_list:
            f.write("%s\n" % item)

    clean_eagle_input_list(in_dir, lib, version, apis_map[lib], eagle_save_list)

    clean_inputs(in_dir, input_save_list)

def clean_eagle_input_list(in_dir, lib, version, api_list, save_list):
    for api_name in api_list:
        for i in range(1000):
            try:
                args_dir = os.path.join(in_dir, 'generated_input/args', lib, version, api_name)

                argument_list_file = os.path.join(args_dir, 'gen_order')
                argument_filename = running_utils.get_arg_file_name(argument_list_file, i)
                file_name = os.path.join(args_dir, argument_filename)
                print(file_name)
                if file_name not in save_list:
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    python_file_name = file_name + "y"
                    if os.path.exists(python_file_name):
                        os.remove(python_file_name)
                    error_file_name = file_name[:-1] + "e"
                    if os.path.exists(error_file_name):
                        os.remove(error_file_name)
            except:
                pass

def clean_inputs(in_dir, save_list):
    for i in range(NUM_OF_INPUT):
        try:
            input_dir = os.path.join(in_dir, 'generated_input/input')
            input_file = os.path.join(input_dir, "%d.npy" % i)
            if input_file not in save_list and os.path.exists(input_file):
                os.remove(input_file)
        except:
                pass
    

if __name__ == "__main__":
    main()
