import importlib
import pickle
import traceback
from rules.equiv_util import get_func_ptr, load_argument_file, load_input_file
from rules.rule_12_tensorflow_script import test_rule_datatype
import numpy as np

in_dir = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00"
lib = "tensorflow"
version = "tensorflow-09-20-2022-23-59-00"

output_path = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00/rule_output/tensorflow/tensorflow-09-20-2022-23-59-00/rule_12/tf.nn.log_softmax-logits-tf.float32-tf.float64/3.output"
api_config = output_path.split('/')[-2]
input_index = int(output_path.split('/')[-1].split('.')[0])

input_index_list = range(50)
# input_index_list =[9, 29, 45, 46, 47]
input_index_list =[3]

for input_index in input_index_list:
    try:
        preprocess_line = api_config.split("-")
        api_name = preprocess_line[0]
        arg_key = preprocess_line[1:-2]
        src_dtype_name = preprocess_line[-2]
        dst_dtype_name = preprocess_line[-1]

        argument = load_argument_file(in_dir, lib, version, api_name, input_index)
        log_file = "log.txt"
        print(argument)

        # get function pointers
        package = "tensorflow"
        mod = importlib.import_module(package)
        target_func = get_func_ptr(mod, api_name)
        src_dtype = get_func_ptr(mod, src_dtype_name)
        dst_dtype = get_func_ptr(mod, dst_dtype_name)

        # run test
        [output_1, output_2] = test_rule_datatype(argument, target_func, arg_key, src_dtype, dst_dtype, log_file)

        print(output_1, output_2)
        print(input_index, ": ", np.allclose(output_1, output_2, atol=1e-2))
        # print(input_index, ": ", np.allclose(output_1, output_2*255, atol=1e-2))

    except:
        print(input_index, ": ", "error")
        pass
