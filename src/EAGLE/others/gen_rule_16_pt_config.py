import pickle
import os
import random
import sys

import torch
import torchvision
import numpy as np

model_list = [
    torchvision.models.resnet18,
    torchvision.models.alexnet,
    torchvision.models.vgg16,
    torchvision.models.squeezenet1_0,
    torchvision.models.densenet161,
    torchvision.models.inception_v3,
    torchvision.models.googlenet,
    torchvision.models.shufflenet_v2_x1_0,
    torchvision.models.mobilenet_v2,
    torchvision.models.resnext50_32x4d,
    torchvision.models.wide_resnet50_2,
    torchvision.models.mnasnet1_0,
]


def save_model_and_inputs(model_save_dir):
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)
    for index in range(len(model_list)):
        if index == 5:
            input_shape = (3, 299, 299)
        else:
            input_shape = (3, 224, 224)
        print(input_shape)
        if len(input_shape) == 3:
            dim0, dim1, dim2 = input_shape
        elif len(input_shape) == 4:
            _, dim0, dim1, dim2 = input_shape
        else:
            print(input_shape)
            raise Exception("Unkown input shape")

        x_list = np.random.randn(10, dim0, dim1, dim2)
        y_list = np.random.randint(0, 1000, size=10)
        input_file = [x_list, y_list]

        input_save_path = os.path.join(model_save_dir, "input_pt_{}".format(index))
        with open(input_save_path, "wb") as f:
            pickle.dump(input_file, f)



model_file_list = [
    "torchvision.models.resnet18",
    "torchvision.models.alexnet",
    "torchvision.models.vgg16",
    "torchvision.models.squeezenet1_0",
    "torchvision.models.densenet161",
    "torchvision.models.inception_v3",
    "torchvision.models.googlenet",
    "torchvision.models.shufflenet_v2_x1_0",
    "torchvision.models.mobilenet_v2",
    "torchvision.models.resnext50_32x4d",
    "torchvision.models.wide_resnet50_2",
    "torchvision.models.mnasnet1_0",
]

input_file_list = [
    "input_pt_0",
    "input_pt_1",
    "input_pt_2",
    "input_pt_3",
    "input_pt_4",
    "input_pt_5",
    "input_pt_6",
    "input_pt_7",
    "input_pt_8",
    "input_pt_9",
    "input_pt_10",
    "input_pt_11",
]


save_load_mode = [
    "model",
    "state_dict",
]

def random_generate_config():
    with open("/mnt/tmp/pt1.6_rule_18", "w") as f:
        for i in range(len(model_file_list)):
            for mode in save_load_mode:
                model_name = model_file_list[i]
                input_file = os.path.join(model_save_dir, input_file_list[i])

                line = model_name + '-' \
                        + input_file + '- ' \
                        + mode + "\n"
                f.write(line)


if __name__ == "__main__":
    in_dir = sys.argv[1]
    model_save_dir = os.path.join(in_dir, "generated_input/saved_model")
    save_model_and_inputs(model_save_dir)
    # random_generate_config()
