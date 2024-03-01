import importlib
import pickle
import traceback
from rules.equiv_util import get_func_ptr, load_argument_file, load_input_file
from rules.rule_9_tensorflow_script import test_rule_image_norm
import numpy as np

in_dir = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00"
lib = "tensorflow"
version = "tensorflow-09-20-2022-23-59-00"

output_path = "/home/workdir/tensorflow/tensorflow-09-20-2022-23-59-00/rule_output/tensorflow/tensorflow-09-20-2022-23-59-00/rule_9/tf.image.convert_image_dtype/0.output"
api_name = output_path.split('/')[-2]
input_index = int(output_path.split('/')[-1].split('.')[0])

input_index_list = range(50)
# input_index_list =[9, 29, 45, 46, 47]
# input_index_list =[50]

for input_index in input_index_list:
    try:
        argument = load_argument_file(in_dir, lib, version, api_name, input_index)
        # print(argument)

        log_file = "./log.txt"

        # get function pointers
        package = "tensorflow"
        mod = importlib.import_module(package)
        fun = get_func_ptr(mod, api_name)

        if "image" in argument.keys():
            image_key = "image"
        elif "images" in argument.keys():
            image_key = "images"
        elif "input" in argument.keys():
            image_key = "input"
        else:
            raise Exception
        argument[image_key] = np.clip(argument[image_key], 0.0, 255.0)
        argument[image_key] = argument[image_key].astype(np.uint8)
        input = argument[image_key]
        # print(input)

        # run test
        [output_1, output_2] = test_rule_image_norm(argument, fun, log_file)
        # print(output_1, output_2)
        print(input_index, ": ", np.allclose(output_1, output_2, atol=1e-2))
        # print(input_index, ": ", np.allclose(output_1, output_2*255, atol=1e-2))

        # per_image_standardization
        # diff = np.abs(output_1 - output_2)
        # max_diff_index = np.unravel_index(np.argmax(diff, axis=None), diff.shape)
        # print("max diff: ", diff[max_diff_index])
        # print("max diff index: ", max_diff_index)
        # print(input[max_diff_index])
        # print(output_1[max_diff_index])
        # print(output_2[max_diff_index])

        # image = input[max_diff_index[:-3]]
        # image = image/255.0
        # # image = image.astype(np.float32)
        # mean = np.mean(image)
        # std = np.std(image)
        # num_pixel = np.prod(image.shape)
        # adjusted_stddev = max(std, 1.0 / np.sqrt(num_pixel))
        # print(std, 1.0 / np.sqrt(num_pixel))
        # output_np = (image - mean) / adjusted_stddev
        # print(output_np[max_diff_index[-3:]])

    except:
        print(input_index, ": ", "error")
        # print(traceback.format_exc())
        pass
