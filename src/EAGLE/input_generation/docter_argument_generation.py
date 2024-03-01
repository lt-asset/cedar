import os
import subprocess
from timeit import default_timer as timer

from config import TF_NAME, PT_NAME


def generate_single_api_argument(data_dir, src_dir, lib, version, api_name, max_num):
    # this function call dl-fuzzer's driver file to generate inputs
    doctor_src_dir = src_dir

    eagle_src_dir = os.path.join(src_dir, "EAGLE/")

    fuzzer_driver = os.path.join(doctor_src_dir, "fuzzer/fuzzer-driver.py")

    if lib == TF_NAME:
        constraint_dir = os.path.join(eagle_src_dir, "api_constraints/tf_constr", "23")
    elif lib == PT_NAME:
        constraint_dir = os.path.join(eagle_src_dir, "api_constraints/pt_constr", "19")

    start_time = timer()

    outpath = os.path.join(data_dir, 'args', lib, version, api_name)
    os.makedirs(outpath, exist_ok=True)

    logpath = os.path.join(outpath, 'docter.log')

    # construct the command to call the driver file
    command = "python " + fuzzer_driver + " "

    command += os.path.join(constraint_dir, "{}.yaml".format(api_name)) + " "

    if lib == TF_NAME:
        command += os.path.join(doctor_src_dir, "tensorflow/tensorflow_dtypes.yml") + " "
    elif lib == PT_NAME:
        command += os.path.join(doctor_src_dir, "pytorch/pytorch_dtypes.yml") + " "
        if "torchvision." not in api_name:
            command += "--data_construct=tensor "
    else:
        raise Exception("Unkown package!")

    command += "--workdir={}".format(outpath) + " "

    command += "--conform --save --mutate_p=0 --fuzz_optional_p=0.6 --max_iter=" + str(max_num) + " "

    command += "--gen_script --timeout=10 > {}".format(logpath)

    print(command)

    subprocess.call(command, shell=True)

    end_time = timer()

    return end_time - start_time