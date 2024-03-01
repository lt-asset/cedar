import importlib
import pickle
from rules.equiv_util import get_func_ptr, load_argument_file, load_input_file
from rules.rule_3_tensorflow_script import test_rule_implement_2d_with_3d
import numpy as np

output_path = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00/rule_output/tensorflow/tensorflow-09-20-2022-23-59-00/rule_3/tf.keras.layers.Conv2D-tf.keras.layers.Conv3D/13.output"
input_index = 13
api_config = "tf.keras.layers.Conv2D-tf.keras.layers.Conv3D"
api_name_2d, api_name_3d = api_config.split('-')

# input_path = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00/generated_input/args/tensorflow/tensorflow-09-20-2022-23-59-00/tf.keras.layers.Conv2D/e0bedca5efd90081b3a6b51a488ab7a1e1b34e86.p"
# with open(input_path, "rb") as f:
#     input_data = pickle.load(f)
in_dir = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00"
lib = "tensorflow"
version = "tensorflow-09-20-2022-23-59-00"
api_name = "tf.keras.layers.Conv2D"
argument = load_argument_file(in_dir, lib, version, api_name_2d, input_index)
print(argument)

input_data = load_input_file(in_dir, input_index)
print(input_data)
print(input_data.shape)
# input_data = np.random.rand(75, 16, 53, 2)
log_file = "./log.txt"

# get function pointers
package = "tensorflow"
mod = importlib.import_module(package)
target_fun_2d = get_func_ptr(mod, api_name_2d)
mod = importlib.import_module(package)
target_fun_3d = get_func_ptr(mod, api_name_3d)

# run test
[output_1, output_2] = test_rule_implement_2d_with_3d(input_data, argument, target_fun_2d, target_fun_3d, log_file)
print(output_1, output_2)
print(np.allclose(output_1, output_2, atol=1e-2))
